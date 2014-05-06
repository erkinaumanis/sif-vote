$(function () {

  $('.create button').on('click',function() {
    var name = $('.form-control')[0].value;
    var ticker = $('.form-control')[1].value;
    var date = $('.form-control')[2].value;
    var action1 = $('.form-control')[3].value;
    var amount1 = $('.form-control')[4].value;
    var action2 = $('.form-control')[5].value;
    var amount2 = $('.form-control')[6].value;

    if (name == null || name == "", ticker == null || ticker == "", date == null || date == "", action1 == null || action1 == "", action1 == null || action1 == "", amount1 == null || amount1 == "", action2 == null || action2 == "", amount2 == null || amount2 == "") {
      alert("Please fill all required fields");
      return false;
    }

    if (validate(amount1) == false || validate(amount2) == false) {
      alert("Invalid amount, please provide an integer value");
      return false;
    }

  });

  function validate(value){    
    re = /\d/;
    if(re.test(value)) {
       return true;
    }
    else {
       return false;
    }
  }
});
