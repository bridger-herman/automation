function init() {
  setUpNav();
  // Set up the color preview boxes
  setupColorPreviews();

  // Set up color mixer
  $('.wheel-color-picker').on('sliderup', function(event) {
    let form = $(event.target).parents('.page');
    setSliderRGBW($(form));
    $(form).submit();
  });

  // Set up LED input containers
  let containers = $('.page');
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
      $(event.target).parents('.page').submit();
    })
  });

  updateFavoriteThumbnails();
  setupLoadSelected();
}

function setUpNav() {
  // Set up navigation
  let defaultPage = 'single-led';
  if (window.location.hash === '') {
      window.location.hash = '#' + defaultPage;
  }
  $('nav ul li a[href="' + window.location.hash +
      '"]').parent().addClass('active');
  $(window).on(
    'hashchange', function() {
      $('nav ul li a').parent().removeClass('active'); $('nav ul li a[href="' +
      window.location.hash + '"]').parent().addClass('active');
    }
  );
}

document.onload = init();
