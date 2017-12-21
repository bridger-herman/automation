function init() {
  // Set up color mixer
  $('.wheel-color-picker').on('sliderup', function(event){
    // console.log($(event.target).wheelColorPicker('color'));
    setMixedColorRGB($(event.target).parent().parent());
  });
  let mixers = $('.color-mixer-box')
  mixers.each(function(i) {
    setMixedColorRGB($(mixers[i]).parent());
  });
}

function setMixedColorRGB(inputContainer) {
  let color = $(inputContainer).find('.wheel-color-picker').wheelColorPicker('color');
  let rgba = [color.r, color.g, color.b, color.a];
  let rgbw = [0, 0, 0, 0];
  for (var i = 0; i < rgba.length; i++) {
    rgbw[i] = floatTo255(rgba[i]);
  }
  color = rgbToHex(...rgbwToRGB(...rgbw));
  $(inputContainer).find('.color-mixer-box').css('background-color', color);
}

document.onload = init();
