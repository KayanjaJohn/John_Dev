$(document).ready(function() {
  $("#login-form").on("submit", function(event) {
    event.preventDefault(); // Prevent the form from submitting

    var formValid = true;

    $(this).find("input").each(function() {
      if ($(this).val() === "") {
        $(this).removeClass("is-valid");
        $(this).addClass("is-invalid");
        formValid = false;
      } else {
        $(this).removeClass("is-invalid");
        $(this).addClass("is-valid");
      }
    });

    // Username validation
    var username = $("#username").val();
    if (!username) {
      $("#usernameError").text("Username is required. Please provide a username.");
      $("#username").removeClass("is-valid");
      $("#username").addClass("is-invalid");
      formValid = false;
    } else if (!/^(?=.*[a-zA-Z])(?=.*\d)(?=.*@)[a-zA-Z\d@]+$/.test(username)) {
      $("#usernameError").text("Username must contain a mix of letters, numbers, '@' and no spaces.");
      $("#username").removeClass("is-valid");
      $("#username").addClass("is-invalid");
      formValid = false;
    } else if (username.length < 4 || username.length > 150) {
      $("#usernameError").text("Username must be between 4 and 150 characters.");
      $("#username").removeClass("is-valid");
      $("#username").addClass("is-invalid");
      formValid = false;
    } else {
      $("#usernameError").text("");
    }
       

      // Password validation
      var password1 = $("#password1").val();
      if (!password1) {
          $("#password1Error").text("Password is required. Please provide a password.");
          $("#password1").removeClass("is-valid");
          $("#password1").addClass("is-invalid");
          formValid = false;
      } else if (!/^[a-zA-Z0-9@*#]+$/.test(password1)) {
          $("#password1Error").text("Password must be alphanumeric with special characters '@', '*', '#' and no spaces.");
          $("#password1").removeClass("is-valid");
          $("#password1").addClass("is-invalid");
          formValid = false;
      } else if (password1.length < 6 || password1.length > 25) {
          $("#password1Error").text("Password must be between 6 and 25 characters..");
          $("#password1").removeClass("is-valid");
          $("#password1").addClass("is-invalid");
          formValid = false;
      } else {
          $("#password1Error").text("");
      }
  
      if (formValid) {
          // If all validations pass, submit the form
          this.submit();
      }
      });
  });
