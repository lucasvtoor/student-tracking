window.onload = function () {
  document.getElementById("nameField").innerHTML = sessionStorage["name"];
};

// reset search and sort value after reset button click
function resetSearch() {
  document.getElementById("search-input3").value = "";
  document.getElementById("sort-form3").submit();
}
