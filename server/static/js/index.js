function init() {
  setupInputRows();
  // Set up direct for submit
  $('.color-input').on('change', function(event) {
    $(event.target).parent().parent().submit();
  })
  // Set up color preview boxes
  let boxes = $('.color-preview-box');
  boxes.each(function(i) {
    $(boxes[i]).css('background-color', $(boxes[i]).attr('data-color'));
  });
  // Set up color mixer
  setMixedColorRGB('single-led');
}

function setupInputRows() {
  let inputRows = $('.led-input-row');
  inputRows.each(function (i) {
    let hex = $(inputRows[i]).attr('data-hex');
    let name = $(inputRows[i]).attr('data-name');
    let value = $(inputRows[i]).attr('data-value');
    $(inputRows[i]).append(getColorPreview(hex));
    $(inputRows[i]).append(getColorInput(name, value));
    $(inputRows[i]).append(getValueDisplay(value));
  });

}

function getColorPreview(color) {
  return '<div class="color-preview-box" data-color="' + color + '"></div>';
}
function getColorInput(name, value) {
  return '<input class="color-input" type="range" name="' + name + '" value="' + value + '" min="0" max="255">';
}
function getValueDisplay(value) {
  return '<div>(' + value + ')</div>';
}

function setMixedColorRGB(inputContainer) {
  let inputRows = $('#' + inputContainer + ' .led-input-row');
  let rgb = [0, 0, 0];
  inputRows.each(function (i) {
    let colorPreview = $(inputRows[i]).find('.color-preview-box').attr('data-color');
    let value = parseInt($(inputRows[i]).find('.color-input').val());
    let nonzero = nonzeroIndex(colorPreview);
    if (nonzero >= 0) {
      rgb[nonzero] = value;
    }
  });
  $('#' + inputContainer).find('.color-mixer-box').css('background-color', rgbToHex(...rgb));
}

document.onload = init();
