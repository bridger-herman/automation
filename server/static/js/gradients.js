function setupGradientPreviews() {
  let previews = $('.gradient-preview');
  $(previews).each(function(i) {
    let source = $(previews[i]).parent().attr('data-src');
    if (source) {
      $(previews[i]).css('background-image', 'url("../../gradients/' + source + '")');
    }
  })
}
