function updateGradientControls(info) {
  $('#gradient-preview').attr('src', info.src);
  $('#gradient-loop').is(':checked',info.loop);
  $('#gradient-duration').val(info.duration);
}

function toggleGradientPlay() {
  ajPOST('toggle-play', {}, function() {});
  updatePlayingIcons();
  // Update icon when current gradient is done (quasi-HACK)
  ajGET('get-gradient', function (info) {
    setTimeout(
      function () { updatePlayingIcons(); },
      1000*parseInt(info.duration)
    );
  });
}

function updatePlayingIcons() {
  ajGET('is-playing', function(info) {
    if (info.playing) { $('#gradient-play-pause').html('pause'); }
    else { $('#gradient-play-pause').html('play_arrow'); }
  });
}

function makeGradientPreview(gradientPath) {
    return '<li class="favorite-thumb">' +
        '<img src="' + gradientPath + '"</img>' +
        '</li>';
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

  ajGET('gradient-list', function(info) {
    let list = $('#favorite-list');
    for (var x in info.gradients) {
      list.append(makeGradientPreview(info.gradients[x]));
    }
  });
}

document.onload = init();
