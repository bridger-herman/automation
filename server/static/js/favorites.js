function updateFavoriteThumbnails() {
  let thumbs = $('.favorite-thumb');
  for (var i = 0; i < thumbs.length; i++) {
    let rgbw = colorHexToArray($(thumbs[i]).attr('data-color'));
    if (!rgbw) {
      return;
    }
    $(thumbs[i]).find('.rgb-preview').css('background-color', rgbToHex(...(rgbw.slice(0, -1))));
    $(thumbs[i]).find('.w-preview').css('background-color', valueToAllHex(rgbw[3]));
    if ($(thumbs[i]).hasClass('add-current')) {
      continue;
    }
    $(thumbs[i]).on('click', function(event) {
      $(thumbs).removeClass('selected');
      let parent = $(event.target);
      while (!$(parent).hasClass('favorite-thumb')) {
        parent = $(parent).parent();
      }
      $(parent).addClass('selected');
      updateLoadSelected(parent);
    });
  }
}

function setupLoadSelected() {
  let firstSelected = $('.favorite-thumb.selected');
  updateLoadSelected(firstSelected);
  let button = $('.load-selected button');
  $(button).on('click', function(event) {
    let selected = $('.favorite-thumb.selected');
    let rgbw = colorHexToArray(selected.attr('data-color'));
    if (!rgbw) {
      return;
    }
    let container = $(event.target).parents('.page');
    setSliderRGBW(container, rgbw);
    let color = $(container).find('.wheel-color-picker').wheelColorPicker('color');
    let names = ['red', 'green', 'blue', 'white'];
    for (var i = 0; i < rgbw.length; i++) {
      $('#' + names[i]).val(rgbw[i]);
    }
    updateColorPreview(container, rgbw);
    container.submit();
  });
}

function updateLoadSelected(selectedThumb) {
  let hex = selectedThumb.attr('data-color');
  if (!hex) {
    return;
  }
  let rgbw = colorHexToArray(hex);
  $(selectedThumb).parents().find('.load-selected.color').not('.static').find('.rgb-preview').css('background-color', rgbToHex(...(rgbw.slice(0, -1))));
  $(selectedThumb).parents().find('.load-selected.color').not('.static').find('.w-preview').css('background-color', valueToAllHex(rgbw[3]));
}

// Make an HTML thumbnail for a particular color
function makeThumb(color=[0, 0, 0, 0], addCurrent=false) {
  let rgb = rgbToHex
  let r = '<li class="favorite-thumb';
  if (addCurrent) {
    r += ' add-current';
  }
  r += '<div class="add-symbol"></div>';
  r += '<div class="color-preview" data-rgb="' + color + '">';
}
