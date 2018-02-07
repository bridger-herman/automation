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

function setWheelRGBW(inputContainer, newRGBW) {
  let inputRows = $(inputContainer + ' .led-input-row');
  let rgbw = [0, 0, 0, 0];
  let floated = [0, 0, 0, 0];
  inputRows.each(function (i) {
    if (!newRGBW) {
      let colorPreview = $(inputRows[i]).find('.color-preview-box').attr('data-color');
      let value = parseInt($(inputRows[i]).find('.color-input').val());
      rgbw[i] = value;
      floated[i] = byteToFloat(value);
    }
    else {
      rgbw[i] = newRGBW[i];
      floated[i] = byteToFloat(newRGBW[i]);
    }
  });
  $(inputContainer).find('.wheel-color-picker').wheelColorPicker('setRgba', ...floated);
  updateColorPreview(inputContainer, rgbw);
  ajaxCurrentColor(rgbw);
}

function setSliderRGBW(inputContainer, newRGBW) {
  let color = $(inputContainer).find('.wheel-color-picker').wheelColorPicker('color');
  let rgba = colorObjToArray(color);
  let rgbw = [0, 0, 0, 0];
  let names = ['red', 'green', 'blue', 'white'];
  for (var i = 0; i < rgba.length; i++) {
    if (!newRGBW) {
      rgbw[i] = floatTo255(rgba[i]);
    }
    else {
      rgbw[i] = newRGBW[i];
    }
    $('#' + names[i]).val(rgbw[i]);
  }
  updateColorPreview(inputContainer, rgbw);
  ajaxCurrentColor(rgbw);
}

function getColorInput(name, value, color) {
  return '<input class="color-input" type="range" name="'
      + name + '" id="' + name + '" value="' + value +
      '" min="0" max="255" data-color="' + color + '">';
}

function getWheelColor(inputContainer) {
  let colorObj = $(inputContainer).find('.wheel-color-picker').wheelColorPicker('getColor');
  let currentRGBA = colorObjToArray(colorObj);
  let rgbw = [0, 0, 0, 0];
  for (var j = 0; j < currentRGBA.length; j++) {
    rgbw[j] = floatTo255(currentRGBA[j]);
  }
  return rgbw;
}

function ajaxCurrentColor(currentRGBW) {
  $.ajax({
    url: "update-leds",
    type: "post",
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify({rgbw:currentRGBW}, null, '\t'), // AHHHH stringify so many hours were wasted here. Kept getting 400 error https://stackoverflow.com/a/17082422
    success: function(response) {
    },
    error: function(xhr) {
      console.log('error');
      console.log(xhr);
    }
  });
}
