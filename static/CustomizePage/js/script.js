$('.language_selector_button').on('click', function(event) {
    event.preventDefault()

    $.ajax({
        url: addLanguageLearning,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken':csrfmiddlewaretoken,
            'language_id':$(this).data('language_id')
        },
        success: (response) => {
            if(response.success) {
                $('#success_message').text("Successfully added the language to your account.");
                $('#success_message').css("color", "green");
                $.ajax({
                    url: getNativeLanguagePage,
                    type: 'GET',
                    dataType: 'html',
                    data: {
                        'csrfmiddlewaretoken':csrfmiddlewaretoken,
                    },
                    success: (response) => {
                        $('#customize_html_loader').html(response)
                        $('#top_bar_text p').text('What language do you speak ?')
                    }
                })
            }
            else {
                $('#success_message').text("Something went wrong...");
                $('#success_message').css("color", "red");
            }
        }
    })

})
