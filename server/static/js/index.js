function updateGradientControls(info) {
  $('#gradient-preview').attr('src', info.src);
  $('#gradient-loop').attr('value', info.loop);
  $('#gradient-duration').attr('value', info.duration);
}

function toggleGradientPlay() {

}

function sendGradientUpdates() {
  let src = $('#gradient-preview').attr('src');
  let loop = $('#gradient-loop').attr('value');
  let duration = $('#gradient-duration').attr('value');
  let data = {'src':src, 'loop':loop, 'duration':duration};
  ajPOST('set-gradient', data, function() {});
}

function ajGET(url, onSuccess) {
  $.ajax({
    url: url,
    type: "get",
    contentType: "application/json",
    dataType: "json",
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

function ajPOST(url,data, onSuccess) {
  $.ajax({
    url: url,
    type: "post",
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify(data, null, '\t'), // AHHHH stringify so many hours were wasted here. Kept getting 400 error https://stackoverflow.com/a/17082422
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

function init() {
  ajGET('get-gradient', updateGradientControls);
  $('#gradient-loop').on('change', sendGradientUpdates);
  $('#gradient-duration').on('change', sendGradientUpdates);
}

document.onload = init();
