//$("#shortenForm").submit(function(e) {
//
//    e.preventDefault(); // avoid to execute the actual submit of the form.
//
//    var form = $(this);
//    var actionUrl = form.attr('action');
//    console.log('12312312';)
//    $.ajax({
//        type: "POST",
//        url: actionUrl,
//        data: form.serialize(), // serializes the form's elements.
//        success: function(data)
//        {
//          alert(data); // show response from the php script.
//        }
//    });
//
//});
$('#originalURL').keypress(function(e) {
    if (e.which == 13) {
        console.log('Found <Enter> event, submit form');
    }
});

var $csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

$(function() {
    $("#shortenForm").submit(function(event) {
        event.preventDefault();
        $("#submitBtn").prop('disabled', true);
        $("#originalURL").prop('disabled', true);
        $("#loadSpin").show();
        //get the form data
        var formData = {
            original_url: $("input[name=original_url]").val(),
        };

        $.ajax({
            type: "POST",
            url: "/api/v1/data/shorten",
            data: formData,
            dataType: "json",
            headers: {
                "X-CSRFToken": $csrf_token
            },
            encode: true
        }).done(function(data) {
            $("#submitBtn").prop('disabled', false);
            $("#originalURL").prop('disabled', false);
            $("#loadSpin").hide();
            $("#containerResult").show()
            $("#resultShorten").html(window.location.origin + data['shorten']);
            $("#resultShorten").attr("href", window.location.origin + data['shorten']);
        });
    });
});


function copyLink() {
  navigator.clipboard.writeText($('#resultShorten').attr('href'));
  $("#copyBtn").html("Copied");
}
