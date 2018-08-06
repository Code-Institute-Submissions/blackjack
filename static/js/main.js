
$(document).ready(function() {

    $(".adjust_players").click(function() {
        set_players();
    })

})


function log(...args) {
    console.log(...args)
}

function set_players() {
    
    // var htmlString = $("#players").html();
    var count = $("#players").val();
    log(count, typeof count)

    if (count === "3") {
       $(".extend").html(`<label>Player 3: <input type="text" name="username" placeholder=" Yoni"/></label><br>`)
    } else if (count === "4") {
        $(".extend").html(`<label>Player 3: <input type="text" name="username" placeholder=" Yoni"/></label><br><label>Player 4: <input type="text" name="username" placeholder=" Damian"/></label><br>`)
    } else {
        $(".extend").html(``)
    }
}

 $('.enableOnInput').prop('disabled', true);
 
 
 