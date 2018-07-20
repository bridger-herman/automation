function makeGradientPreview(gradientPath) {
    return '<li class="favorite-thumb">' +
        '<img src="' + gradientPath + '"</img>' +
        '</li>';
}

function init() {

  // Get the available gradients from the server
  ajGET('gradient-list', function(info) {
    let list = $('#favorite-list');
    for (var x in info.gradients) {
      list.append(makeGradientPreview(info.gradients[x]));
    }
    $('.favorite-thumb img').on('click', setSelectedGradient)
    ajGET('get-gradient', updateGradientControls);
    $('#gradient-loop').on('change', sendGradientUpdates);
    $('#gradient-duration').on('change', sendGradientUpdates);
    $('#slider-brightness').on('change', sendGradientUpdates);
    $('#gradient-play').on('click', playLeds);
    $('#gradient-stop').on('click', stopLeds);
  });

}

document.onload = init();
