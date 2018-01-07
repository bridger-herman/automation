function setupInputRows(inputContainer) {
  let inputRows = $(inputContainer).find('.led-input-row');
  let colorObj = $(inputRows).parent().find('.wheel-color-picker').wheelColorPicker('getColor');
  let currentRGBA = colorObjToArray(colorObj);
  inputRows.each(function (i) {
    let hex = $(inputRows[i]).attr('data-hex');
    let name = $(inputRows[i]).attr('data-name');
    $(inputRows[i]).append(getColorInput(name, floatTo255(currentRGBA[i]), hex));
  });
  let ranges = $('.color-input');
  ranges.each(function(i) {
    $(ranges[i]).css('background', $(ranges[i]).attr('data-color'));
  });
}

function setupColorPreviews() {
  $('.color-preview').append('<div class="rgb-preview"></div>');
  $('.color-preview').append('<div class="w-preview"></div>');
}

function updateColorPreview(inputContainer, rgbw) {
  // console.log(rgbToHex(...(rgbw.slice(0, -1))));
  // console.log({{ wheel_color_value }});
  $(inputContainer).find('.color-preview').not('.static, .preview-selected').find('.rgb-preview').css('background-color', rgbToHex(...(rgbw.slice(0, -1))));
  $(inputContainer).find('.color-preview').not('.static, .preview-selected').find('.w-preview').css('background-color', valueToAllHex(rgbw[3]));
}

function setWheelRGBW(inputContainer) {
  let inputRows = $(inputContainer + ' .led-input-row');
  let rgbw = [0, 0, 0, 0];
  let floated = [0, 0, 0, 0];
  inputRows.each(function (i) {
    let colorPreview = $(inputRows[i]).find('.color-preview-box').attr('data-color');
    let value = parseInt($(inputRows[i]).find('.color-input').val());
    rgbw[i] = value;
    floated[i] = byteToFloat(value);
  });
  $(inputContainer).find('.wheel-color-picker').wheelColorPicker('setRgba', ...floated);
  updateColorPreview(inputContainer, rgbw);
}

function setSliderRGBW(inputContainer) {
  let color = $(inputContainer).find('.wheel-color-picker').wheelColorPicker('color');
  let rgba = colorObjToArray(color);
  let rgbw = [0, 0, 0, 0];
  let names = ['red', 'green', 'blue', 'white'];
  for (var i = 0; i < rgba.length; i++) {
    rgbw[i] = floatTo255(rgba[i]);
    $('#' + names[i]).val(rgbw[i]);
  }
  updateColorPreview(inputContainer, rgbw);
}

function getColorInput(name, value, color) {
  return '<input class="color-input" type="range" name="'
      + name + '" id="' + name + '" value="' + value +
      '" min="0" max="255" data-color="' + color + '">';
}
