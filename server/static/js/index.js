function updateGradientControls(info) {
  $('#gradient-preview').attr('src', info.src);
  $('#gradient-loop').attr('value', info.loop);
  $('#gradient-duration').attr('value', info.duration); 
}

function init() {
  $.ajax({
    url: "gradient-info",
    type: "get",
    contentType: "application/json",
    dataType: "json",
    // data: JSON.stringify({rgbw:currentRGBW}, null, '\t'), // AHHHH stringify so many hours were wasted here. Kept getting 400 error https://stackoverflow.com/a/17082422
    success: function(response) {
      console.log(response);
      updateGradientControls(response);
    },
    error: function(xhr) {
      console.log('error');
      console.log(xhr);
    }
  });

  // // Set up the color preview boxes
  // setupColorPreviews();
  //
  // // Set up color mixer
  // $('.wheel-color-picker').on('sliderup', function(event) {
  //   setSliderRGBW($(event.target).parents('.led-input-container'));
  // });
  //
  // // Set up LED input containers
  // let containers = $('.led-input-container');
  // containers.each(function (i) {
  //   let rgbw = getWheelColor(containers[i]);
  //   updateColorPreview(containers[i], rgbw);
  //   // Set up direct RGBW input sliders
  //   setupInputRows(containers[i]);
  //   // Set up RGBW input submit
  //   $('.color-input').on('change', function(event) {
  //     setWheelRGBW('.led-input-container');
  //   });
  // });
  //
  // updateFavoriteThumbnails();
  // setupLoadSelected();
}


document.onload = init();
