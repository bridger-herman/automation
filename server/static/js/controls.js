function updateSelectedGradient(which) {
  which = parseInt(which) + 1;
  $('.favorite-thumb').removeClass('selected');
  $('#favorite-list>:nth-child(' + which + ')').addClass('selected');
}

function updateGradientControls(info) {
  $('#gradient-preview').attr('src', info.src);
  $('#gradient-loop').is(':checked',info.loop);
  $('#gradient-duration').val(info.duration);
  updateSelectedGradient(info.which);
}

function setSelectedGradient(event) {
  let selected = $(event.target).parent().index();
  updateSelectedGradient(selected);
  sendGradientUpdates();
  ajGET('get-gradient', updateGradientControls);
}

function toggleGradientPlay() {
  ajPOST('toggle-play', {}, function() {});
  updatePlayingIcons();
  // Update icon when current gradient is done (quasi-HACK)
  ajGET('get-gradient', function (info) {
    setTimeout(
      function () { updatePlayingIcons(); },
      1200*parseInt(info.duration)
    );
  });
}

function updatePlayingIcons() {
  ajGET('is-playing', function(info) {
    if (info.playing) { $('#gradient-play-pause').html('pause'); }
    else { $('#gradient-play-pause').html('play_arrow'); }
  });
}

function sendGradientUpdates() {
  let src = $('#gradient-preview').attr('src');
  let loop = $('#gradient-loop').is(':checked');
  let duration = $('#gradient-duration').val();

  // Not sure why this is necessary...
  let selected = $('#favorite-list').find('.selected');
  let which = $('#favorite-list').children().index(selected);

  let data = {'src':src, 'loop':loop, 'duration':duration, 'which':which};
  ajPOST('set-gradient', data, function() {});
}
