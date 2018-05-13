function updateGradientControls(info) {
  $('#gradient-preview').attr('src', info.src);
  $('#gradient-loop').attr('value', info.loop);
  $('#gradient-duration').attr('value', info.duration);
}

function sendGradientUpdates() {
  let src = $('#gradient-preview').attr('src');
  let loop = $('#gradient-loop').attr('value');
  let duration = $('#gradient-duration').attr('value');
  $.ajax({
    url: "set-gradient",
    type: "post",
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify({'src':src, 'loop':loop, 'duration':duration}, null, '\t'), // AHHHH stringify so many hours were wasted here. Kept getting 400 error https://stackoverflow.com/a/17082422
    success: function(response) {
      console.log(response);
      updateGradientControls(response);
    },
    error: function(xhr) {
      console.log('error');
      console.log(xhr);
    }
  });
}

function init() {
  $.ajax({
    url: "get-gradient",
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
  // $('#gradient-preview').on('update', sendGradientUpdates);
  $('#gradient-loop').on('change', sendGradientUpdates);
  $('#gradient-duration').on('change', sendGradientUpdates);


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
