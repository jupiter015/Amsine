
$(document).ready(() => {
     
    let interval;
    let intervalIsOn = false;

    $('#bio').on('input', (event) => {
        $('#save_button').show()
    })
    
    $('#save_button').on('click', (event) => {
        event.preventDefault()
        updateProfileDetailsFunc()
    })
    
    // //Opening Select Menu - learning_language
    // $('#language_learning_update_button').on('click', (event) => {
    //     $('#select_menu_screen').fadeIn();
    //     $('#select_menu').fadeIn();
    
    //     $.ajax({
    //         url: getUserLanguageDetails,
    //         type: 'GET',
    //         data: {
    //             'csrfmiddlewaretoken': csrfmiddlewaretoken
    //         },
    //         beforeSend: () => {
    //             $('#select_menu_spinner_container .spinner').show()
    //         },
    //         success: (response) => {
    //             let keys = Object.keys(response);
    //             let html_code = "";
    //             for(let i = 0; i < keys.length; i++) {
    //                 if(response[keys[i]].selected)
    //                     html_code += `<label for='${keys[i]}'>${keys[i]}:</label> <input type='checkbox' name='${keys[i]}' id='${keys[i]}' checked/><br>`;
    //                 else
    //                     html_code += `<label for='${keys[i]}'>${keys[i]}:</label> <input type='checkbox' name='${keys[i]}' id='${keys[i]}' /><br>`;
    //             }
    //             $('#select_items').html(html_code);
    //         },
    //         complete: () => {
    //             $('#select_menu_spinner_container .spinner').hide()
    //         }
    //     })
    // })
    
    // //Opening Select Menu - native_language_update_button
    // $('#native_language_update_button').on('click', (event) => {
    //     $('#select_menu_screen').fadeIn();
    //     $('#select_menu').fadeIn();
    // })
    
    //Opening Select Menu - interests_update_button
    $('#interests_update_button').on('click', (event) => {
        $('#select_menu_screen').fadeIn();
        $('#select_menu').fadeIn();
    
        $.ajax({
            url: getInterestsDetails,
            type: 'GET',
            data: {
                'csrfmiddlewaretoken': csrfmiddlewaretoken
            },
            beforeSend: () => {
                $('#select_menu_spinner_container').css('display', 'flex')
            },
            success: (response) => {
                let keys = Object.keys(response);
                let html_code = "";
                for(let i = 0; i < keys.length; i++) {
                    if(response[keys[i]].selected)
                        html_code += `<label for='${keys[i]}'>${keys[i]}:</label> <input type='checkbox' name='${keys[i]}' id='${keys[i]}' checked/><br>`;
                    else
                        html_code += `<label for='${keys[i]}'>${keys[i]}:</label> <input type='checkbox' name='${keys[i]}' id='${keys[i]}' /><br>`;
                }
                $('#select_items').html(html_code).attr('field', 'interests')
            },
            complete: () => {
                $('#select_menu_spinner_container').css('display', 'none')
            }
        });
    })
    
    // Closing Select Menu With inbuilt button and touching anywhere else
    $('#close_menu').on('click', (event) => {
        $('#select_menu_screen').fadeOut();
        $('#select_menu').fadeOut();
    });
    
    $('#select_menu_screen').on('click', (event) => {
        if($(event.target).closest('#select_menu').length == 0 ) {
            $('#select_menu_screen').fadeOut();
            $('#select_menu').fadeOut();
        }
    });
    
    // On Select Items Change
    $('#save_items').click(function() {
        let selected_items = []
        $('#select_items input[type="checkbox"]').each(function() {
            $('#interests').empty().append('<option disabled="" selected="" value="">-- Your Interests --</option>');
            if ($(this).is(':checked')) {
                selected_items.push($(this)[0].name)
            }  
        });
        if($('#select_items').attr('field') == 'interests') {
            $('#interests').empty().append('<option disabled="" selected="" value="">-- Your Interests --</option>');
            $.each(selected_items, function(index, value) {
                $('#interests').append('<option disabled value="' + value + '">' + value + '</option>');
            });
        }
        updateProfileDetailsFunc()
        $('#select_menu_screen').fadeOut();
        $('#select_menu').fadeOut();
    });
    
    
    function updateProfileDetailsFunc() {
        var interests = [];
        $('#interests option:not(:first)').each(function(){
        interests.push($(this).val());
        });
        $.ajax({
            url: updateProfileDetails,
            type: 'POST',
            contentType: 'application/json',
            headers: {
                "X-CSRFToken": csrfmiddlewaretoken
            },
            data: JSON.stringify({
                'bio': $('#bio').val(),
                'interests': interests
            }),
            beforeSend: () => {
                $('#select_menu_spinner_container').css('display', 'flex')
            },
            success: (response) => {
                if(response.success) {
                    $('#success_message').text("Successfully updated your profile.")
                    $('#success_message').css('color', 'green')
                    $('#save_button').hide()
                }
                else {
                    $('#success_message').text("Something went wrong..")
                    $('#success_message').css('color', 'red')
                }
            },
            complete: () => {
                $('#select_menu_spinner_container').css('display', 'none')
            }
        })
    }

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
