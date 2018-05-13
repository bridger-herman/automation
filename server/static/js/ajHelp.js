function ajGET(url, onSuccess) {
  $.ajax({
    url: url,
    type: "get",
    contentType: "application/json",
    dataType: "json",
    success: function(response) {
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
    success: function(response) {
      onSuccess(response);
    },
    error: function(xhr) {
      console.log('error');
      console.log(xhr);
    }
  });
}
