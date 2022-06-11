$(document).ready(function () {
  // code to read selected table row cell data (values).
  $(".name").on("click", function () {
    var currentRow = $(this).closest("tr");
    var name = currentRow.find("td:eq(0)").html();
    sessionStorage["name"] = name;
    console.log(name);
    name = name.replace("%20", "");
    name = name.replace(" ", "");
    window.location.replace("http://127.0.0.1:5000/detail/" + name);
  });
});

function resetSearch() {
  document.getElementById("search-input2").value = "";
  document.getElementById("sort-form2").submit();
}
