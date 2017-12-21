function init() {
  let container = $('.led-input-container');
  container.append(getColorInput('red', 255));
  container.append(getColorInput('green', 255));
  container.append(getColorInput('blue', 255));
  container.append(getColorInput('white', 255));
  // Set up color mixer
  $('.wheel-color-picker').on('sliderup', function(event){
    // console.log($(event.target).wheelColorPicker('color'));
    setMixedColorRGB($(event.target).parent().parent());
    $(event.target).parent().parent().submit();
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
  $('#red').val(rgbw[0]);
  $('#green').val(rgbw[1]);
  $('#blue').val(rgbw[2]);
  $('#white').val(rgbw[3]);
}

function getColorInput(name, value) {
  return '<input class="color-input" type="range" name="'
      + name + '" id="' + name + '" value="' + value +
      '" min="0" max="255" style="display: none">';
}

document.onload = init();
