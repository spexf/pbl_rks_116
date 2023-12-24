$(document).ready(()=>{
    $('#signIn').on('click', ()=>{
        let username = $('#username').val()
        let password = $('#password').val()
        if (username == ''){
            return Swal.fire({
                title: "Can't Blank",
                text: `Username Field Must Be Filled`,
                icon: "error",
              }).then(()=>{
                $('#username').focus()
              });
        } else if (password == ''){
            return Swal.fire({
                title: "Can't Blank",
                text: `Password Field Must Be Filled`,
                icon: "error",
              }).then(()=>{
                $('#password').focus()
              });
        }

        $.ajax({
            url: `/api/auth/login`,
            type: 'POST',
            data: {
                username : $('#username').val(),
                password : $('#password').val()
            },
            success: (res)=>{
                if (res.access_token ) {
                    localStorage.setItem('access_token',res.access_token)
                    document.cookie=`access_token_cookie=${res.access_token}; path=/; expires=${new Date(res.expiredate) }`
                    return Swal.fire({
                        title: "Login Success",
                        text: `Welcome ${$('#username').val()}`,
                        icon: "success",
                      }).then(()=>{
                        window.location.href = '/'
                      });
                }
            },
            error: (err)=>{
                if (err.status == 403) {
                    return Swal.fire({
                        title: "Invalid Credentials",
                        text: "Username or Password maybe wrong :)",
                        icon: "error",
                      });
                } else {
                    return Swal.fire({
                        title: "Server Error",
                        text: "Server Could Not Response Your Request",
                        icon: "error",
                      });
                }
            }
        })
    })

    $('#signUp').on('click', ()=>{
      let username = $('#username').val()
      let password = $('#password').val()
      let email = $('#email').val()

      if (username == ''){
        return Swal.fire({
            title: "Can't Blank",
            text: `Username Field Must Be Filled`,
            icon: "error",
          }).then(()=>{
            $('#username').focus()
          });
    } else if (email == ''){
        return Swal.fire({
            title: "Can't Blank",
            text: `Email Field Must Be Filled`,
            icon: "error",
          }).then(()=>{
            $('#email').focus()
          });
    } else if (password == ''){
        return Swal.fire({
            title: "Can't Blank",
            text: `Password Field Must Be Filled`,
            icon: "error",
          }).then(()=>{
            $('#password').focus()
          });
    }

    $.ajax({
      url: `/api/auth/register`,
      type: 'POST',
      data: {
          username : $('#username').val(),
          password : $('#password').val(),
          email : $('#email').val(),
      },
      success: (res)=>{
          if (res.status == 200){

            return  Swal.fire({
              title: "Register Success",
              text: `You registered !`,
              icon: "success",
            }).then(()=>{
              window.location.href = '/auth/login'
            });
          } else {
            return Swal.fire({
              title: "Register Failed",
              text: "Unknown Error, Please Contact Admin",
              icon: "error"
            })
          }
      },
      error: (err)=>{
        console.log(err)
          if (err.status == 422) {
              return Swal.fire({
                  title: "Register Failed",
                  text: err.responseJSON.message,
                  icon: "error",
                });
          } else {
              return Swal.fire({
                  title: "Server Error",
                  text: "Server Could Not Response Your Request",
                  icon: "error",
                });
          }
      }
  })

    })
})