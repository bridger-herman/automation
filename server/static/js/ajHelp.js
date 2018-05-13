function ajGET(url, data, onSuccess) {
  let jString = JSON.stringify(data, null, '\t');
  $.ajax({
    url: url,
    type: "get",
    contentType: "application/json",
    dataType: "json",
    // headers: {'Content-Length':jString.length}, // TODO doesn't work
    // data: jString,
    success: function(response) {
      console.log(response);
      onSuccess(response);
    },
    error: function(xhr) {
      console.log('error');
      console.log(xhr);
    }
  });
}

function ajPOST(url, data, onSuccess) {
  // AHHHH stringify so many hours were wasted here. Kept getting 400 error
  // https://stackoverflow.com/a/17082422
  $.ajax({
    url: url,
    type: "post",
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify(data, null, '\t'),
    // headers: {'Content-Length':jString.length},
    success: function(response) {
      console.log(response);
      onSuccess(response);
    },
    error: function(xhr) {
      console.log('error');
      console.log(xhr);
    }
  });
}
