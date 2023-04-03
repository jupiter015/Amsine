$('#submit_interest').on('click', (event) => {
    event.preventDefault()

    var selectedCheckboxes = ""
    $('input[type="checkbox"]').each(function() {
        var checkboxValue = $(this).val();
        var isChecked = $(this).is(":checked");
        if(isChecked) 
            selectedCheckboxes = selectedCheckboxes + checkboxValue.toLowerCase() + ",";
    });
    selectedCheckboxes = selectedCheckboxes.substring(0, selectedCheckboxes.length-1)

    $.ajax({
        url: addInterestUrl,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'selectedCheckboxes': selectedCheckboxes
        },
        success: (response) => {
            if(response.success) {
                $('#interest_success_message').text("Successfully added the language to your account.");
                $('#interest_success_message').css("color", "green");
                window.location.href = "/"
            }
            else {
                $('#interest_success_message').text("Something went wrong...");
                $('#interest_success_message').css("color", "red");
            }
        }
    })

});