function init() {
  // Set up direct RGBW input sliders
  setupInputRows();
  // Set up RGBW submit
  $('.color-input').on('change', function(event) {
    $(event.target).parent().parent().submit();
  })
  // Set up color mixer
  $('.wheel-color-picker').on('sliderup', function(event){
    // console.log($(event.target).wheelColorPicker('color'));
    setSliderRGBW($(event.target).parent().parent());
    $(event.target).parent().parent().submit();
  });
  let mixers = $('.color-mixer-box')
  mixers.each(function(i) {
    setSliderRGBW($(mixers[i]).parent());
  });
}

function setupInputRows() {
  let inputRows = $('.led-input-row');
  inputRows.each(function (i) {
    let hex = $(inputRows[i]).attr('data-hex');
    let name = $(inputRows[i]).attr('data-name');
    // $(inputRows[i]).append(getColorPreview(hex));
    $(inputRows[i]).append(getColorInput(name, 255, hex)); // Default to #ffffffff
  });
  // let boxes = $('.color-preview-box');
  // boxes.each(function(i) {
  //   $(boxes[i]).css('background-color', $(boxes[i]).attr('data-color'));
  // });
  let ranges = $('.color-input');
  ranges.each(function(i) {
    $(ranges[i]).css('background', $(ranges[i]).attr('data-color'));
  });
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
  $(inputContainer).find('.color-mixer-box').css('background-color', rgbToHex(...rgbwToRGB(...rgbw)));
}

function setSliderRGBW(inputContainer) {
  let color = $(inputContainer).find('.wheel-color-picker').wheelColorPicker('color');
  let rgba = [color.r, color.g, color.b, color.a];
  let rgbw = [0, 0, 0, 0];
  let names = ['red', 'green', 'blue', 'white'];
  for (var i = 0; i < rgba.length; i++) {
    rgbw[i] = floatTo255(rgba[i]);
    $('#' + names[i]).val(rgbw[i]);
  }
  $(inputContainer).find('.color-mixer-box').css('background-color', rgbToHex(...rgbwToRGB(...rgbw)));
}

function getColorPreview(color) {
  return '<div class="color-preview-box" data-color="' + color + '"></div>';
}

function getColorInput(name, value, color) {
  return '<input class="color-input" type="range" name="'
      + name + '" id="' + name + '" value="' + value +
      '" min="0" max="255" data-color="' + color + '">';
}

document.onload = init();
