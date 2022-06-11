window.onload = function () {
  document.getElementById("nameField").innerHTML = sessionStorage["name"];
};

function resetSearch() {
  document.getElementById("search-input3").value = "";
  document.getElementById("sort-form3").submit();
}
