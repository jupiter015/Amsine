$(document).ready(() => {

    let interval;
    let intervalIsOn = false;

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
        window.location.href = 'profile/'
    })
    
    // Check if user profile is customized
    $.ajax({
        url: checkIfUserProfileCustomizedUrl,
        type: 'GET',
        data: {
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        },
        success: (response) => {
            if(!response.complete) {
                setTimeout(() => {
                    $('#submenu').css('display', 'none')
                    $('#user_tab_message_popup').text("You still haven't completed personalizing your account. Complete it to get personalized learning experience and unlock more features.")
                    $('#user_tab_message_popup').addClass('show').css('display', 'block')
                }, 2000)
                setTimeout(() => $('#user_tab_message_popup').removeClass('show').css('display', 'none'), 15000)
            }
            else $('#user_tab_message_popup').css('display', 'none')
        }
    })
    
    //Load Learning Container
    $.ajax({
        url:loadChaptersUrl,
        type:'GET',
        data: {
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'last_language_used': $('#learning_container').data('last_language_used')
        },
        beforeSend: () => {
            $('#learning_container .spinner_container').css('display', 'flex')
        },
        success: (response) => {
            $('#learning_html_load_container').html(response.html)
        },
        error: (xhr, status, error) => {
            $('#alert_container').css('display', 'flex')
            $('#alert_container p').text('Some Error Occured. Please Refresh.')
            $('#alert_container p').css('color', 'red')
        },
        complete: () => {
            $('#learning_container .spinner_container').css('display', 'none')
        }
    })

    // Clicking anywhere on document closing chat thing
    $(document).on('click', (event) => {
        if($('#chat_container').css('display') == 'block') {
            if($(event.target).closest('#chat_link_tab_button').length == 0 && $(event.target).closest('#chat_container').length == 0) {
                $('#chat_container').css('display', 'none')
                clearInterval(interval)
                intervalIsOn = false
            }
        }
    })

    $('#chat_link_tab_button').on('click', function() {
        if($('#chat_container').css('display') == 'block') {
            clearInterval(interval)
            intervalIsOn = false
            $('#chat_container').css('display', 'none')
        }
        else {
            $('#chat_container').css('display', 'block')
            
            // Check if the user is linked with someone
            $.ajax({
                url: checkIfLinkedUrl,
                type: 'GET',
                data: {
                    'csrfmiddlewaretoken': csrfmiddlewaretoken
                },
                beforeSend: () => {
                    $('#chat_spinner_container .spinner_container').css('display', 'flex')
                },
                success: (response) => {
                    if(response.isLinked) {
                        $('#chat_message_container #chat_status_message').html('')
                        if(!intervalIsOn) {
                            interval = setInterval(getChats, 1000)
                            intervalIsOn = true
                            setTimeout(() => {
                                $("#chats").scrollTop($("#chats").prop("scrollHeight"));
                            }, 1100)
                        }
                    }
                    else {
                        $('#chat_message_container #chat_status_message').html('You are not linked with anyone. Linking you up...')
                        // Link with a person and then load
                        $.ajax({
                            url: linkUserUrl,
                            type: 'POST',
                            data: {
                                'csrfmiddlewaretoken': csrfmiddlewaretoken
                            },
                            beforeSend: () => {
                                $('#chat_spinner_container .spinner_container').css('display', 'flex')
                            },
                            success: (response) => {
                                setTimeout(() => {
                                    if(response.success) {
                                        $('#chat_message_container #chat_status_message').html('')
                                        if(!intervalIsOn) {
                                            interval = setInterval(getChats, 1000)
                                            intervalIsOn = true
                                            setTimeout(() => {
                                                $("#chats").scrollTop($("#chats").prop("scrollHeight"));
                                            }, 1100)
                                        }
                                    }
                                    else {
                                        $('#chat_message_container #chat_status_message').html('Failed to find a user for you... Please try again later..')
                                    }
                                }, 2000)
                            },
                            complete: () => {
                                $('#chat_spinner_container .spinner_container').css('display', 'none')
                            }
                        })
                    }
                },
                complete: () => {
                    $('#chat_spinner_container .spinner_container').css('display', 'none')
                }
            })
        }
    })

    // Send messages
    $('#message_send_button').on('click', (event) => {
        if($('#message_send_container input').val().trim() != '') {
            $.ajax({
                url: sendMessageUrl,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrfmiddlewaretoken,
                    'message': $('#message_send_container input').val().trim()
                },
                success: (response) => {
                    $('#message_send_container input').val('')
                    $("#chats").scrollTop($("#chats").prop("scrollHeight"));
                }
            })
        }
    })

    function getChats() {
        // AJAX request to add chat html in chat_html_loader
        $.ajax({
            url: getChatsUrl,
            type: 'GET',
            data: {
                'csrfmiddlewaretoken': csrfmiddlewaretoken
            },
            beforeSend: () => {
                $('#chat_spinner_container .spinner_container').css('display', 'flex')
            },
            success: (response) => {
                if(response.html) {
                    let scrollPos = $("#chats").scrollTop()
                    $('#chat_html_loader').html(response.html)
                    $("#chats").scrollTop(scrollPos);
                }
                else 
                    $('#chat_message_container #chat_status_message').html('Failed to load chat..')
            },
            complete: () => {
                $('#chat_spinner_container .spinner_container').css('display', 'none')
            }
        })
    }


})