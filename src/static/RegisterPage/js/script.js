// Variables
let usernameCheck = false;
let emailCheck = false;
let passwordCheck = false;

// Check If Username is in use
let usernameTimeout;
$('#username').on('input', (event) => {
    clearTimeout(usernameTimeout);
    usernameTimeout = setTimeout(() => {
        $.ajax({
            url: usernameCheckUrl,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrfmiddlewaretoken,
                username: $("#username").val()
            },
            success: (response) => {
                if(response.available) {
                    if($("#username").val().trim() == "") {
                        $('#username_message').text("");
                        usernameCheck = false;
                    }
                    else {
                        $('#username_message').text("Username is available.");
                        $('#username_message').css('color', 'green');
                        usernameCheck = true;
                    }
                }
                else{
                    $('#username_message').text("Username is already taken.");
                    $('#username_message').css('color', 'red');
                    usernameCheck = false;
                }
            }
        })
        checkIfButtonIsValid();
    }, 500);
})

// Check If Email is in use
let checkEmailTimeout;
$('#email_id').on('input', (event) => {
    clearTimeout(checkEmailTimeout);
    checkEmailTimeout = setTimeout(() => {
        $.ajax({
            url: emailCheckUrl,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrfmiddlewaretoken,
                email_id: $("#email_id").val()
            },
            success: (response) => {
                if(!response.available) {
                    $('#email_message').text("Email is already in use.");
                    $('#email_message').css('color', 'red');
                    emailCheck = false;
                }
                else {
                    $('#email_message').text("");
                    emailCheck = true;
                }
            }
        })
        checkIfButtonIsValid();
    }, 500);
})

//Check password one
let passwordTimeout;
$("#password").on('input', (event) => {
    let password_str = $("#password").val().trim();
    clearTimeout(passwordTimeout);
    passwordTimeout = setTimeout(() => {
        if(password_str != "") {
            
            // Special Characters
            let specialCharacterExist = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/.test(password_str) ? true : false;
            
            // Numbers
            let numberExist = /\d/.test(password_str) ? true : false;

            //Captial Letter
            let capitalLetterExist = /[A-Z]/.test(password_str) ? true : false;

            if(specialCharacterExist && numberExist && capitalLetterExist && password_str.length > 6) {
                $("#password_message").text("");
                passwordCheck = true;
            }
            else {
                $("#password_message").text("Password need to be greater than 5 letters and must have `Capital Letter`, `Special Character` and `Numbers` in it.");
                $("#password_message").css('color', 'red');
                passwordCheck = true;
            }

        }
        else {
            $("#password_message").text("");
        }
        checkPasswordValid();
        checkIfButtonIsValid();
    }, 500);
})

// Check if the re-password is the same
let re_passwordTimeout;
$("#re-password").on('input', (event) => {
    clearTimeout(re_passwordTimeout);
    re_passwordTimeout = setTimeout(() => {
        checkPasswordValid();
        checkIfButtonIsValid();
    }, 500);
})

function checkIfButtonIsValid() {
    if(usernameCheck && emailCheck && passwordCheck) {
        $("#register").prop('disabled', false);
    }
    else $("#register").prop('disabled', true);
}

function checkPasswordValid() {
    if($("#password").val().trim() == $("#re-password").val().trim() && $('#password').val().trim() != "") {
        $("#password_message").text("")
        passwordCheck = true;
    }
    else {
        passwordCheck = false;
        if($("#password").val().trim() != "" && $('#re-password').val().trim() != "") {
            $("#password_message").text("Password does not match")
            $('#password_message').css('color', 'red')
        }
    }
}

// Log In Button
$('#logInButton').on('click', (event) => {
    event.preventDefault()
    window.location.href = "/login/"
});

//Register Button
$("#register").on('click', (event) => {
    event.preventDefault();
    $.ajax({
        url: registerButtonUrl,
        type: 'GET',
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            username: $("#username").val(),
            email_id: $("#email_id").val(),
            password: $("#password").val()
        },
        beforeSend: () => {
            $('.spinner').show();
        },
        success: (response) => {
            if(response.success) {
                $.cookie('session_id', response.session_id, { path: '/'});
                window.location.href = "/register/verify"
            }
            else {
                $('#success_message').text(response.message);
                $('#success_message').css('color', 'red');
            }
        },
        complete: () => {
            $('.spinner').hide();
        }
    })
});