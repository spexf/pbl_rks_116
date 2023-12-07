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
                        text: `Welcome Back ${$('#username').val()}`,
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
})