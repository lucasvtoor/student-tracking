$(document).ready(function () {
  // code to read selected table row cell data (values).
  $(".name").on("click", function () {
    var currentRow = $(this).closest("tr");
    var name = currentRow.find("td:eq(0)").html();
    // set clicked name in session storage
    sessionStorage["name"] = name;
    // replace space weird added space with joined strinf
    name = name.replace("%20", "");
    name = name.replace(" ", "");
    // redirect app to detail page with selected student info
    window.location.replace("http://127.0.0.1:5000/detail/" + name);
  });
});

// reset search and sort value after reset button click
function resetSearch() {
  document.getElementById("search-input2").value = "";
  document.getElementById("sort-form2").submit();
}
