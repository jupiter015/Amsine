$("#verifyAuthCode").on('click', (event) => {
    event.preventDefault();

    $.ajax({
        url: checkAuthCodeUrl,
        type: 'GET',
        data: {
            'csrfmiddlewaretoken' : csrfmiddlewaretoken,
            auth_code: $('#auth_code').val()
        },
        beforeSend: () => {
            $('.spinner').show();
        },
        success: (response) => {
            if(response.success) {
                $('#auth_code_message').text('Right Auth COol');
                $('#auth_code_message').css('color', 'green');
                $.cookie('session_id', response.session_id, { path: '/'});
                $.cookie('user_id', response.user_id, { path: '/'});
                window.location.href = '/customize/';
            }
            else {
                $('#auth_code_message').text('Wrong Auth Code');
                $('#auth_code_message').css('color', 'red');
            }
        },
        complete: () => {
            $('.spinner').hide();
        }
    })

})