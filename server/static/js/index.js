function updateGradientControls(info) {
  $('#gradient-preview').attr('src', info.src);
  $('#gradient-loop').is(':checked',info.loop);
  $('#gradient-duration').val(info.duration);
}

function toggleGradientPlay() {
  $('#gradient-play-pause').html('pause');
  ajPOST('toggle-play', {}, function() {});
  $('#gradient-play-pause').html('play_arrow');
}

function sendGradientUpdates() {
  let src = $('#gradient-preview').attr('src');
  let loop = $('#gradient-loop').is(':checked');
  let duration = $('#gradient-duration').val();
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
