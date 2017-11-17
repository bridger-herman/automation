function init() {
  $('.color-input').on('change', function(event) {
    $(event.target).parent().parent().submit();
  })
}

document.onload = init();
