
$(document).ready(function() {
    
    // changes the number of text inputs on the fly.  
    $( "#players" ).change(function() {
        set_players($("#players")); // passing in item $("#players") into the function
    })
    
})

// console.log turned into a function for cleaner/shorter codes,  
// ease of use and faster progress.
function log(...args) {
    // prints however many parameters passed in
    console.log(...args)
}


// change the number of text inputs
function set_players(item) {
    
    // get item's current value
    var count = item.val();
    
    // logic to change number of text input based on the selection made by the user.
    if (count === "3") {
       $(".extend").html(`<label>Player 3: &nbsp<input class="form-control-sm" type="text" name="username" placeholder=" Yoni" value="logan"/></label><br>`)
    } else if (count === "4") {
        $(".extend").html(`<label>Player 3: &nbsp<input class="form-control-sm" type="text" name="username" placeholder=" Yoni" value="logan"/></label><br><label>Player 4: &nbsp<input class="form-control-sm" type="text" name="username" placeholder=" Damian" value="joe"/></label><br>`)
    } else {
        $(".extend").html(``)
    }
}

 
 
 