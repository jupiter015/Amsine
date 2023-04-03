$(document).ready(() => {

    var current_question = 0

    // Clicking anywhere on document closing submenu
    $(document).on('click', (event) => {
        if($(event.target).closest('#user_tab_button').length == 0 && $(event.target).closest('#submenu').length == 0) {
            $('#submenu').css('display', 'none')
        }
    })
    
    // User Submenu
    $('#user_tab_button').on('click', (event) => {
        $('#user_tab_message_popup').removeClass('show').css('display', 'none')
        if($('#submenu').css('display') == "none")
            $('#submenu').css('display', 'flex')
        else 
            $('#submenu').css('display', 'none')
    })
    
    // Log Out Submenu Function
    $("#log_out_user_submenu").on('click', (event) => {
        $.ajax({
            url: logOutUrl,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrfmiddlewaretoken
            },
            success: (response) => {
                location.reload();
            }
        })
    })
    
    // Profile Submenu Function
    $('#profile_user_submenu').on('click', (event) => {
        window.location.href = '/profile/'
    })
    
    // // Check if user profile is customized
    // $.ajax({
    //     url: checkIfUserProfileCustomizedUrl,
    //     type: 'GET',
    //     data: {
    //         'csrfmiddlewaretoken': csrfmiddlewaretoken
    //     },
    //     success: (response) => {
    //         if(!response.complete) {
    //             setTimeout(() => {
    //                 $('#submenu').css('display', 'none')
    //                 $('#user_tab_message_popup').text("You still haven't completed personalizing your account. Complete it to get personalized learning experience and unlock more features.")
    //                 $('#user_tab_message_popup').addClass('show').css('display', 'block')
    //             }, 2000)
    //             setTimeout(() => $('#user_tab_message_popup').removeClass('show').css('display', 'none'), 15000)
    //         }
    //         else $('#user_tab_message_popup').css('display', 'none')
    //     }
    // })

    // Get next question html
    $('#game_html_loader').on('click', '.next_button', (event) => {
        $.ajax({
            url: loadNextQuestionUrl,
            type: 'GET',
            data: {
                'csrfmiddlewaretoken': csrfmiddlewaretoken,
                'lessonNum': lessonNum,
                'chapterNum': chapterNum,
                'chapter_type': chapter_type,
                'language_name': language_name,
                'current_question': current_question
            },
            beforeSend: () => {
                $('#spinner_container').css('display', 'flex')
            },
            success: (response) => {
                $('#game_html_loader').html(response.html)
                current_question += 1
                if(current_question < 7)
                    $('#game_header h3').html(current_question + "/6")
                else
                    $('#game_header h3').html("END")
            },
            complete: () => {
                $('#spinner_container').css('display', 'none')
            }
        })
    })
})