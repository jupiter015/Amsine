$("#validateLogin").on('click', (event) => {
    event.preventDefault();
    let username = $("#username").val();
    let password = $("#password").val();
    let message = $("#message");

    if(username.trim() == "" || password.trim() == "") {
        message.text("Please enter all the fields down below");
        message.css('color', 'red');
    }
    else {
        message.text("Logging in..");
        message.css('color', 'blue');
        $.ajax({
            url: validate_url,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfmiddlewaretoken,
                'username': username,
                'password': password
            },
            success: (response) => {
                if(response.validation) {
                    message.text("Successfully logging in");
                    message.css('color', 'green');
                    $.cookie('user_id', response.user_id, { path: '/'});
                    $.cookie('session_id', response.session_id, { path: '/'});
                    window.location.href = "/"
                }
                else {
                    message.text("Wrong username or password");
                    message.css('color', 'red');
                }
            }
        })
    }
})

//Sign Up Button
$('#signUpButton').on('click', (event) => {
    event.preventDefault()
    window.location.href = "/register/"
})