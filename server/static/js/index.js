function init() {
  // Set up the color preview boxes
  setupColorPreviews();

  // Set up color mixer
  $('.wheel-color-picker').on('sliderup', function(event) {
    setSliderRGBW($(event.target).parents('.led-input-container'));
  });

  // Set up LED input containers
  let containers = $('.led-input-container');
  containers.each(function (i) {
    let rgbw = getWheelColor(containers[i]);
    updateColorPreview(containers[i], rgbw);
    // Set up direct RGBW input sliders
    setupInputRows(containers[i]);
    // Set up RGBW input submit
    $('.color-input').on('change', function(event) {
      setWheelRGBW('.led-input-container');
    });
  });

  updateFavoriteThumbnails();
  setupLoadSelected();
}


document.onload = init();
