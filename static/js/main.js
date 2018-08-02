
$(document).ready(function() {

    // seems to be functional
    $("h1").click(function() {
        // console.log($(this).css("color"))
        if ($(this).css("color") === "rgb(255, 0, 0)") {
            // console.log("YES the value matches")
            $(this).css("color", "black")
        }
        else {
            $(this).css("color", "red")
        }
    })





})
