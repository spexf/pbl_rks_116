from flask import Flask, render_template, request,jsonify, make_response, redirect,url_for
from datetime import datetime, timedelta
from module import cipher
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,JWTManager, set_refresh_cookies, set_access_cookies, create_refresh_token, unset_jwt_cookies
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from time import strftime

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'fd9f74595c05499287de366bcc1068d6'
app.config['JWT_TOKEN_LOCATION'] = ['cookies','headers']
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flask:flaskpbl116@localhost/pblRKS116'
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'

app.config['JWT_COOKIE_CSRF_PROTECT'] = False


jwt = JWTManager(app)
sql = SQLAlchemy(app)
class Users(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    username = sql.Column(sql.String(255), unique=True, nullable=False)
    password = sql.Column(sql.String(255), nullable=False)
    email = sql.Column(sql.String(255), nullable=False)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Histories(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    type_of_cipher = sql.Column(sql.String(255), nullable=False)
    methods = sql.Column(sql.Enum('enc','dec'), nullable=False)
    strings = sql.Column(sql.String(255), nullable=False)
    result = sql.Column(sql.String(255), nullable=False)
    used_key = sql.Column(sql.String(255), nullable=False)
    user_id = sql.Column(sql.Integer, nullable=False)
    created_at = sql.Column(sql.DateTime, nullable=False)
    

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return redirect(url_for('login'))

@app.route('/auth/login')
def login():
    return render_template('pages/login.html')

@app.route('/test')
@jwt_required()
def test():
    current_user = get_jwt_identity()
    data = sql.session.execute(text(f'SELECT * FROM users WHERE username="{current_user}"')).first()
    # print(data.username)
    return jsonify(200,str(data.id))

@app.route('/')
def index():
    return render_template('pages/home.html')

@app.route('/api/auth/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    check_duplicate = sql.session.execute(text(f'SELECT * FROM users where username="{username}"')).first()
    if check_duplicate != None:
        return make_response({'message': 'Register Failed, Username Has Registered !'}, 422)
    
    new_user = Users(username=username, email=email)
    new_user.set_password(password)
    sql.session.add(new_user)
    sql.session.commit()
    
    data = sql.session.execute(text(f'SELECT * FROM users where username="{username}"')).first()
    return jsonify(
        status=200,
        username=data.username,
        email=data.email
    )

@app.route('/api/auth/login',methods=['POST'])
def authLogin():
    username = request.form['username']
    password = request.form['password']
    data = Users.query.filter_by(username=username).first()
    if data == None:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})
    else:
        if data and data.check_password(password):
            
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            resp = jsonify({'login': True})

            set_access_cookies( resp,access_token)
            set_refresh_cookies(resp, refresh_token)

            return jsonify(access_token = access_token, expiredate=str(datetime.now() + timedelta(seconds=3600)))
        else:
            return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    res = jsonify({'logout': True})
    unset_jwt_cookies(res)
    return res, 200

@app.route('/page')
@jwt_required()
def routingPage():
    requests = request.args.to_dict()
    if requests == {}:
        return render_template('err/404.html')
    else:
        if requests['cipher'] == 'caesar':
            return render_template('pages/caesar.html')
        elif requests['cipher'] == 'vigenere':
            return render_template('pages/vigenere.html')
        else:
            return render_template('err/404.html')
            
@app.route('/api/caesar/dec', methods=['POST'])
@jwt_required()
def caesarEnc():
    current_user = get_jwt_identity()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now)
    requests = request.json
    caesar = cipher.Caesar()
    uid = Users.query.filter_by(username=current_user).first()
    result = caesar.decrypt(requests['plain'],requests['key'])
    new_histories = Histories(type_of_cipher='Caesar',methods='dec',strings=requests['plain'], result=result,used_key=requests['key'] ,user_id=uid.id, created_at=now)
    sql.session.add(new_histories)
    sql.session.commit()
    # sql.session.execute(text(f'INSERT INTO histories(type_of_cipher, methods, strings, result,used_key, user_id) VALUES ("caesar","enc","{string}", "{result}", "{key}",{uid.id} )'))
    
    return jsonify(
        status=200,
        data=result
    )
@app.route('/api/caesar/enc', methods=['POST'])
@jwt_required()
def caesarEnc():
    current_user = get_jwt_identity()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now)
    requests = request.json
    caesar = cipher.Caesar()
    uid = Users.query.filter_by(username=current_user).first()
    result = caesar.encrypt(requests['plain'],requests['key'])
    new_histories = Histories(type_of_cipher='Caesar',methods='enc',strings=requests['plain'], result=result,used_key=requests['key'] ,user_id=uid.id, created_at=now)
    sql.session.add(new_histories)
    sql.session.commit()
    # sql.session.execute(text(f'INSERT INTO histories(type_of_cipher, methods, strings, result,used_key, user_id) VALUES ("caesar","enc","{string}", "{result}", "{key}",{uid.id} )'))
    
    return jsonify(
        status=200,
        data=result
    )

@app.route('/api/vigenere/enc', methods=['POST'])
@jwt_required()
def vigenereEnc():
    current_user = get_jwt_identity()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(now)
    requests = request.json
    vigenere = cipher.Vigenere()
    uid = Users.query.filter_by(username=current_user).first()
    result = vigenere.encrypt(requests['plain'],requests['key'])
    new_histories = Histories(type_of_cipher='Vigenere',methods='enc',strings=requests['plain'], result=result,used_key=requests['key'] ,user_id=uid.id, created_at=now)
    sql.session.add(new_histories)
    sql.session.commit()
    
    return jsonify(
        status=200,
        data=result
    )
@app.route('/api/vigenere/dec', methods=['POST'])
@jwt_required()
def vigenereDec():
    current_user = get_jwt_identity()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(now)
    requests = request.json
    vigenere = cipher.Vigenere()
    uid = Users.query.filter_by(username=current_user).first()
    result = vigenere.decrypt(requests['plain'],requests['key'])
    new_histories = Histories(type_of_cipher='Vigenere',methods='dec',strings=requests['plain'], result=result,used_key=requests['key'] ,user_id=uid.id, created_at=now)
    sql.session.add(new_histories)
    sql.session.commit()
    
    return jsonify(
        status=200,
        data=result
    )
    
@app.route('/api/user/profile',methods=['POST'])
def getUserData():
    requests = request.args.to_dict()
    return jsonify(
        status=200,
        data='success'
    )
    
@app.route('/api/history',methods=['GET'])
@jwt_required()
def historyApi():
    current_user = get_jwt_identity()
    data = Users.query.filter_by(username=current_user).first()
    history_data = Histories.query.filter_by(user_id=int(data.id))
    retdata= dict()
    indexing = 1
    for i in history_data:
        jsonres = {"cipher":i.type_of_cipher, "plaintext":i.strings, "key":i.used_key, "result":i.result, "methods":i.methods, "time": i.created_at}
        retdata[int(indexing)] = jsonres
        indexing +=1
    return jsonify(retdata),200


@app.route('/profile',methods=['GET'])
@jwt_required()
def manageProfile():
    current_user = get_jwt_identity()
    data = Users.query.filter_by(username=current_user).first()
    history_data = Histories.query.filter_by(user_id=int('5'))
    for i in history_data:
        print(i.type_of_cipher)
    return f'halo {current_user}'

if __name__ == "__main__":
    app.run(debug=True)