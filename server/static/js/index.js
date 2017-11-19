function init() {
  $('.color-input').on('change', function(event) {
    $(event.target).parent().parent().submit();
  })
  let boxes = $('.color-preview-box');
  boxes.each(function(i) {
    $(boxes[i]).css('background-color', $(boxes[i]).attr('data-color'));
  });
  setMixedColorRGB('single-led');
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
