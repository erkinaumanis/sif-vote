$(document).ready(function() {
  setInterval(function() {
    $.get("/update_votes", function(body) {

      for (var ticker in body) {
        if (body.hasOwnProperty(ticker)) {
          var action = body[ticker];
          var actionVoteTotal = 0;

          // Get vote totals
          for (var actionId in action) {
            if (action.hasOwnProperty(actionId)) {
              if ($(".table." + ticker + " #" + actionId + " .header").text() === " Don't Buy " && $(".table." + ticker + " #" + actionId + " .progress-bar").hasClass("progress-bar-success")) {
                $(".table." + ticker + " #" + actionId + " .progress-bar-success").removeClass("progress-bar-success").toggleClass("progress-bar-danger");
              }
              actionVoteTotal = actionVoteTotal + action[actionId];         
            }
          }

          // Actually update the votes with pcount
          for (var actionId in action) {
            if (action.hasOwnProperty(actionId)) {

              var pcount = (action[actionId] / actionVoteTotal) * 100;


              $(".table." + ticker + " #" + actionId + " .count").html(action[actionId]);
              $(".table." + ticker + " #" + 
                actionId + " .progress-bar").css("width",pcount + "%");
            }
          }
        }
      }
        
    console.log('Load was performed.');
    });
  }, 1000);

  setInterval(function() {
    $.get("/update_numbers", function(body) {
      var templ = ""
      for (var key in body) {
        templ = templ + "<div>" + body[key] + "</div>";
      }
      
      $('.number-list').html(templ);
        
    console.log('Load was performed.');
    });
  }, 1000);

});


  