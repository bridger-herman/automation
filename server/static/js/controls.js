function updateSelectedGradient(which) {
  which = parseInt(which) + 1;
  $('.favorite-thumb').removeClass('selected');
  $('#favorite-list>:nth-child(' + which + ')').addClass('selected');
}

function updateGradientControls(info) {
  $('#gradient-preview').attr('src', info.src);
  $('#gradient-loop').is(':checked',info.loop);
  $('#gradient-duration').val(info.duration);
  $('#slider-brightness').val(info.brightness);
  updateSelectedGradient(info.which);
}

function setSelectedGradient(event) {
  let selected = $(event.target).parent().index();
  updateSelectedGradient(selected);
  sendGradientUpdates();
  ajGET('get-gradient', updateGradientControls);
}

function playLeds() {
  ajPOST('play-leds', {}, function() {});
  // Update the brightness slider when current gradient is done (quasi-HACK)
  ajGET('get-gradient', function (info) {
    setTimeout(
      function () {
        let d = new Date();
        console.log($('#input-slider-bg'));
        $('#input-slider-bg').css('background-image', 'url("/brightness_slider.png?dont_use_this' + d.getTime() + '")');
      },
      1000*parseInt(info.duration) + 4000
    );
  });
}

function stopLeds() {
  ajPOST('stop-leds', {}, function() {});
  $('#input-slider-bg').css('background-image', 'url("/brightness_slider.png?dont_use_this' + d.getTime() + '")');
}

function sendGradientUpdates() {
  let src = $('#gradient-preview').attr('src');
  let loop = $('#gradient-loop').is(':checked');
  let duration = $('#gradient-duration').val();
  let brightness = $('#slider-brightness').val();

  // Not sure why this is necessary...
  let selected = $('#favorite-list').find('.selected');
  let which = $('#favorite-list').children().index(selected);

  let data = {
    'src':src,
    'loop':loop,
    'duration':duration,
    'which':which,
    'brightness':brightness,
  };
  ajPOST('set-gradient', data, function() {});
}
