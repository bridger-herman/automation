// function loadDoc() {
//   var xhttp = new XMLHttpRequest();
//   xhttp.onreadystatechange = function() {
//     if (this.readyState == 4 && this.status == 200) {
//       console.log(this.responseText);
//     }
//   };
//   xhttp.open("GET", "home_server.py", true);
//   xhttp.send();
// }
$.ajax({
  url: "color_database",
  type: "get",
  contentType: "application/json",
  dataType: "json",
  data: JSON.stringify({nah:"wow"}, null, '\t'), // AHHHH stringify so many hours were wasted here. Kept getting 400 error https://stackoverflow.com/a/17082422
  success: function(response) {
    console.log('success');
    console.log(response);
  },
  error: function(xhr) {
    console.log('error');
    console.log(xhr);
  }
});
