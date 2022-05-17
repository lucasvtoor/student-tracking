window.onload = function () {
  console.log("hekk");
  const data = document.getElementById("data").innerHTML;
  console.log("hello1" + data);
  var string1 = JSON.stringify(data);
  const user = JSON.parse(string1);
  console.log("hello2" + user["name"]);
  console.log(user);
};
