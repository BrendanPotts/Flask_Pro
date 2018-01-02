$(function() {
    $('#addCard').click(function() {

        $.ajax({
            url: '/addCard',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                window.location.href = "addCard";
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});