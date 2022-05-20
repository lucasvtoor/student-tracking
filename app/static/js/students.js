$(document).ready(function () {
  // code to read selected table row cell data (values).
  $(".name").on("click", function () {
    var currentRow = $(this).closest("tr");
    var name = currentRow.find("td:eq(1)").html();
    var email = currentRow.find("td:eq(2)").html();
    sessionStorage["name"] = name;
    sessionStorage["email"] = email;
    console.log(name);
    name = name.replace("%20", "");
    name = name.replace(" ", "");
    window.location.replace("http://studenttracking.xyz/detail/" + name);
  });
});
