function updateFavoriteThumbnails() {
  let thumbs = $('.favorite-thumb');
  for (var i = 0; i < thumbs.length; i++) {
    updateColorPreview(thumbs[i], [255, 0, 0, 221]);
    console.log($(thumbs[i]).attr('data-color'));
  }
}

function makeFavorites() {
  $('.favorites').append();
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
