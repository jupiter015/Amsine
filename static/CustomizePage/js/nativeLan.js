$('.native_language_selector_button').on('click', (event) => {
    event.preventDefault()

    $.ajax({
        url: addNativeLanguageUrl,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'language_id': $(event.target).data('language_id')
        },
        success: (response) => {
            if(response.success) {
                $('#native_success_message').text("Successfully added the language to your account.");
                $('#native_success_message').css("color", "green");
                $.ajax({
                    url: getInterestPageUrl,
                    type: 'GET',
                    dataType: 'html',
                    data: {
                        'csrfmiddlewaretoken':csrfmiddlewaretoken,
                    },
                    success: (response) => {
                        $('#customize_html_loader').html(response)
                        $('#top_bar_text p').text('Choose your interest')
                        $('#search_bar').css('display', 'none')
                    }
                })
            }
            else {
                $('#native_success_message').text("Something went wrong...");
                $('#native_success_message').css("color", "red");
            }
        }
    })

});