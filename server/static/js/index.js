function init() {
  $('.color-input').on('change', function(event) {
    $(event.target).parent().parent().submit();
  })
  let boxes = $('.color-box');
  boxes.each(function(i) {
    $(boxes[i]).css('background-color', $(boxes[i]).attr('data-color'));
  });
}

document.onload = init();
