window.onload = function () {
  document.getElementById("nameField").innerHTML = sessionStorage["name"];
  document.getElementById("emailField").innerHTML = sessionStorage["email"];
};
