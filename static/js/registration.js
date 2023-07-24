$(document).ready(function() {
    $("#registration-form").on("submit", function(event) {
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
        $("#usernameError").text("Username must contain a mix of letters, numbers,'@'and no spaces.");
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
      

      // First name validation
      var firstName = $("#first_name").val();
      if (!firstName) {
        $("#firstNameError").text("First name is required. Please provide a first name.");
        $("#first_name").removeClass("is-valid");
        $("#first_name").addClass("is-invalid");
        formValid = false;
      } else if (!/^[a-zA-Z]+$/.test(firstName)) {
        $("#firstNameError").text("First name must contain only alphabetic characters and no spaces.");
        $("#first_name").removeClass("is-valid");
        $("#first_name").addClass("is-invalid");
        formValid = false;
      } else if (firstName.length > 150) {
        $("#firstNameError").text("First name cannot exceed 150 characters.");
        $("#first_name").removeClass("is-valid");
        $("#first_name").addClass("is-invalid");
        formValid = false;
      } else {
        $("#firstNameError").text("");
      }

      // Last name validation
      var lastName = $("#last_name").val();
      if (!lastName) {
        $("#lastNameError").text("Last name is required. Please provide a last name.");
        $("#last_name").removeClass("is-valid");
        $("#last_name").addClass("is-invalid");
        formValid = false;
      } else if (!/^[a-zA-Z]+$/.test(lastName)) {
        $("#lastNameError").text("Last name must contain only alphabetic characters and no spaces.");
        $("#last_name").removeClass("is-valid");
        $("#last_name").addClass("is-invalid");
        formValid = false;
      } else if (lastName.length > 150) {
        $("#lastNameError").text("Last name cannot exceed 150 characters.");
        $("#last_name").removeClass("is-valid");
        $("#last_name").addClass("is-invalid");
        formValid = false;
      } else {
        $("#lastNameError").text("");
      }

      // Email validation
      var email = $("#email").val();
      if (!email) {
        $("#emailError").text("Email is required. Please provide an email address.");
        $("#email").removeClass("is-valid");
        $("#email").addClass("is-invalid");
        formValid = false;
      } else {
        $("#emailError").text("");
      }

      // Department validation
      var department = $("#department").val();
      if (!department || department === "0") {
        $("#department").removeClass("is-valid");
        $("#department").addClass("is-invalid");
        $("#department-error").text("Department is required. Please select a department.");
        formValid = false;
      } else {
        $("#department").removeClass("is-invalid");
        $("#department").addClass("is-valid");
        $("#department-error").text("");
      }

      // Role validation
      // var role = $("#role").val();
      // if (!role || role === "0") {
      //   $("#role").removeClass("is-valid");
      //   $("#role").addClass("is-invalid");
      //   $("#role-error").text("Role is required. Please select a role.");
      //   formValid = false;
      // } else {
      //   $("#role").removeClass("is-invalid");
      //   $("#role").addClass("is-valid");
      //   $("#role-error").text("");
      // }


      // Disconnect date validation
      var disconnectDate = $("#disconnect_date").val();
      if (!disconnectDate) {
        $("#disconnectDateError").text("Disconnect date is required. Please provide a disconnect date.");
        $("#disconnect_date").removeClass("is-valid");
        $("#disconnect_date").addClass("is-invalid");
        formValid = false;
      } else {
        $("#disconnectDateError").text("");
      }

      // Password validation
      var password1 = $("#password1").val();
      if (!password1) {
          $("#password1Error").text("Password is required. Please provide a password.");
          $("#password1").removeClass("is-valid");
          $("#password1").addClass("is-invalid");
          formValid = false;
      } else if (!/^[a-zA-Z0-9@*#]+$/.test(password1)) {
          $("#password1Error").text("Password must be alphanumeric with special characters '@', '*', '#'.");
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
  

      // Confirm password validation
      var password2 = $("#password2").val();
      if (!password2 || password2 !== password1) {
        $("#password2Error").text("Confirm password does not match the password.");
        $("#password2").removeClass("is-valid");
        $("#password2").addClass("is-invalid");
        formValid = false;
      } else {
        $("#password2Error").text("");
      }

      if (formValid) {
        // If all validations pass, submit the form
        this.submit();
      }
    });
  });