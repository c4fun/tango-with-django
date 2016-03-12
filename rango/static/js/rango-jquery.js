$(document).ready(function(){
    // JQuery code to be added in here
    $("#about-btn").click(function(){
        message_string = $("#msg").html();
        message_string += "Added content.";
        $("#msg").html(message_string);
    });

    $("#about-btn").addClass('btn btn-primary')

});