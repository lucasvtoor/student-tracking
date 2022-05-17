$(document).ready(function () {
  // code to read selected table row cell data (values).
  $(".name").on("click", function () {
    var currentRow = $(this).closest("tr");
    var name = currentRow.find("td:eq(1)").html();
    sessionStorage["name"] = name;
    console.log(name);
    window.location.replace("http://127.0.0.1:5000/detail");
  });
});
