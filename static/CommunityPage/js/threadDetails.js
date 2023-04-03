$(document).ready(() => {
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

    // Clicking on new post button
    $('#new_reply_button').on('click', (event) => {
        $('#add_new_reply_container').css('display', 'flex')
        $('#title').val("")
    })

    // Clicking anywhere while add_new_reply_container is showen, closes it
    $(document).on('click', (event) => {
        if($('#add_new_reply_container').css('display') == 'flex') {
            if($(event.target).closest('#add_new_reply_box').length == 0 && $(event.target).closest('#new_reply_button').length == 0) {
                $('#add_new_reply_container').css('display', 'none')
                getReplies()
            }
        }
    })

    // Toggle Add Reply button
    $('#reply').on('input', function() {
        if($(this).val().trim() != "") {
            $('#submit_reply').removeAttr('disabled')
        }
        else $('#submit_reply').attr('disabled', true)
    })

    // AJAX to add new reply :D
    $('#submit_reply').on('click', (event) => {
        if($('#reply').val().trim() != "") {
            $.ajax({
                url: addReplyUrl,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrfmiddlewaretoken,
                    'thread_uuid': thread_uuid,
                    'reply': $('#reply').val().trim()
                },
                success: (response) => {
                    $('#add_new_reply_container').css('display', 'none')
                    getReplies()
                }
            })
        }
    })

    // AJAX to delete thread
    $('#delete_thread').on('click', (event) => {
        $.ajax({
            url: deleteThreadUrl,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfmiddlewaretoken,
                'thread_uuid': thread_uuid
            },
            success: (response) => {
                if(response.success) {
                    window.location.href = '/community/'
                }
                console.log(response)
            }
        })
    })

    // Get Replies AJAX function
    function getReplies() {
        $.ajax({
            url: getRepliesUrl,
            type: 'GET',
            data: {
                'csrfmiddlewaretoken': csrfmiddlewaretoken,
                'thread_uuid': thread_uuid
            },
            beforeSend: () => {
                $('#spinner_container').css('display', 'flex')
            },
            success: (response) => {
                if(response.error_message) {
                    $('#error_div').css('display', 'flex')
                    $('#error_div p').text(response.error_message)
                }
                else {
                    $('#error_div').css('display', 'none')
                    $('#replies_html_loader').html(response.html)
                }
            },
            complete: () => {
                $('#spinner_container').css('display', 'none')
            }
        })
    }
    getReplies()

})