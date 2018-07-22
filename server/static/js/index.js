// Depends on proper formatting of names...
function makeGradientPreview(gradientPath) {
  let nameIndex = gradientPath.lastIndexOf('_');
  let dotIndex = gradientPath.lastIndexOf('.');
  return '<li class="ten-margin favorite-thumb">' +
      '<img src="' + gradientPath + '"</img>' +
      '<p>' + gradientPath.slice(nameIndex + 1, dotIndex) + '</p>' +
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
