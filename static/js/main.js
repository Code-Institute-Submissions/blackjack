
$(document).ready(function() {
    
    // changes the number of text inputs on the fly.  
    $( "#players" ).change(function() {
        set_players($("#players")); // passing in item $("#players") into the function
    })



    $(document).ready(function(){
      // Add smooth scrolling to all links
      $("a").on('click', function(event) {
    
        // Make sure this.hash has a value before overriding default behavior
        if (this.hash !== "") {
          // Prevent default anchor click behavior
          event.preventDefault();
    
          // Store hash
          var hash = this.hash;
    
          // Using jQuery's animate() method to add smooth page scroll
          // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
          $('html, body').animate({
            scrollTop: $(hash).offset().top
          }, 800, function(){
       
            // Add hash (#) to URL when done scrolling (default click behavior)
            window.location.hash = hash;
          });
        } // End if
      });
    });




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
       $(".extend").html(`<label class="ml-3">Player 3: &nbsp<input class="form-control-sm" type="text" name="username" placeholder=" Yoni" value="logan"/></label><br>`)
    } else if (count === "4") {
        $(".extend").html(`<label class="ml-3">Player 3: &nbsp<input class="form-control-sm" type="text" name="username" placeholder=" Yoni" value="logan"/></label><br><label class="ml-4">Player 4: &nbsp<input class="form-control-sm" type="text" name="username" placeholder=" Damian" value="joe"/></label><br>`)
    } else {
        $(".extend").html(``)
    }
}

 
 
 