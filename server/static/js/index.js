function init() {
  // Set up the color preview boxes
  setupColorPreviews();

  // Set up color mixer
  $('.wheel-color-picker').on('sliderup', function(event) {
    let form = $(event.target).parents('.led-input-container');
    setSliderRGBW($(form));
    $(form).submit();
  });

  // Set up LED input containers
  let containers = $('.led-input-container');
  containers.each(function (i) {
    let colorObj = $(containers[i]).find('.wheel-color-picker').wheelColorPicker('getColor');
    let currentRGBA = colorObjToArray(colorObj);
    let rgbw = [0, 0, 0, 0];
    for (var j = 0; j < currentRGBA.length; j++) {
      rgbw[j] = floatTo255(currentRGBA[j]);
    }
    updateColorPreview(containers[i], rgbw);
    // Set up direct RGBW input sliders
    setupInputRows(containers[i]);
    // Set up RGBW input submit
    $('.color-input').on('change', function(event) {
      $(event.target).parents('.led-input-container').submit();
    })
  });

  updateFavoriteThumbnails();
  setupLoadSelected();
}

document.onload = init();
