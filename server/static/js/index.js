function init() {
  // Set up direct RGBW input sliders
  setupInputRows();
  // Set up the color preview boxes
  setupColorPreviews();
  // Set up RGBW submit
  $('.color-input').on('change', function(event) {
    $(event.target).parent().parent().submit();
  })
  // Set up color mixer
  $('.wheel-color-picker').on('sliderup', function(event){
    setSliderRGBW($(event.target).parent().parent());
    $(event.target).parent().parent().submit();
  });
  let containers = $('.led-input-container');
  containers.each(function (i) {
    let colorObj = $(containers[i]).find('.wheel-color-picker').wheelColorPicker('getColor');
    let currentRGBA = colorObjToArray(colorObj); // TODO assumes there's only one set of color input rows
    let rgbw = [0, 0, 0, 0];
    for (var j = 0; j < currentRGBA.length; j++) {
      rgbw[j] = floatTo255(currentRGBA[j]);
    }
    updateColorPreview(containers[i], rgbw);
  });
}

function setupInputRows() {
  let inputRows = $('.led-input-row');
  let colorObj = $(inputRows).parent().find('.wheel-color-picker').wheelColorPicker('getColor');
  let currentRGBA = colorObjToArray(colorObj); // TODO assumes there's only one set of color input rows
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
  $(inputContainer).find('.color-preview').find('.rgb-preview').css('background-color', rgbToHex(...(rgbw.slice(0, -1))));
  $(inputContainer).find('.color-preview').find('.w-preview').css('background-color', valueToAllHex(rgbw[3]));
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
  // $(inputContainer).find('.color-preview').css('background-color', rgbToHex(...rgbw.slice(0, -1)));
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
  // $(inputContainer).find('.color-preview').css('background-color', rgbToHex(...rgbw.slice(0, -1)));
  updateColorPreview(inputContainer, rgbw);
}

function getColorInput(name, value, color) {
  return '<input class="color-input" type="range" name="'
      + name + '" id="' + name + '" value="' + value +
      '" min="0" max="255" data-color="' + color + '">';
}

document.onload = init();
