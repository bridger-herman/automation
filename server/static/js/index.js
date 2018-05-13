function updateGradientControls(info) {
  $('#gradient-preview').attr('src', info.src);
  $('#gradient-loop').attr('value', info.loop);
  $('#gradient-duration').attr('value', info.duration);
}

function toggleGradientPlay() {
  // ajGET('playing', function(info) {
  //   if (info.playing == false) { // Opposite, until threading
    // }
    // else {
    // }
  // });
  $('#gradient-play-pause').html('pause');
  ajPOST('toggle-play', {}, function() {});
  $('#gradient-play-pause').html('play_arrow');
}

function sendGradientUpdates() {
  let src = $('#gradient-preview').attr('src');
  let loop = $('#gradient-loop').attr('value');
  let duration = $('#gradient-duration').attr('value');
  let data = {'src':src, 'loop':loop, 'duration':duration};
  ajPOST('set-gradient', data, function() {});
}

function init() {
  ajGET('get-gradient', updateGradientControls);
  $('#gradient-loop').on('change', sendGradientUpdates);
  $('#gradient-duration').on('change', sendGradientUpdates);
  $('#gradient-play-pause').on('click', toggleGradientPlay);
}

document.onload = init();
