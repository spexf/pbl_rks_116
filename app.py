from flask import Flask, render_template, request,jsonify, json, Response
from module import cipher
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('pages/home.html')

@app.route('/page')
def routingPage():
    requests = request.args.to_dict()
    # return requests
    if requests == {}:
        return render_template('err/404.html')
    else:
        if requests['cipher'] == 'caesar':
            return render_template('pages/caesar.html')
        elif requests['cipher'] == 'vigenere':
            return render_template('pages/vigenere.html')
        else:
            return render_template('err/404.html')
            
    
@app.route('/api/caesar/enc', methods=['POST'])
def caesarEnc ():
    requests = request.args.to_dict()
    caesar = cipher.Caesar()
    return jsonify(
        status=200,
        data=caesar.encrypt(requests['plain'],requests['key'])
    )
    # return Response(status=200, body=1)

if __name__ == "__main__":
    app.run(debug=True)