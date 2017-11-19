// https://stackoverflow.com/questions/40312216/converting-rgb-to-rgbw
function rgbToRGBW(r, g, b) {
  let max = Math.max(r, g, b);
  if (max === 0) {
    return [0, 0, 0 ,0];
  }
  // Figure out 100% hue colors
  let multiplier = 255.0/max;
  let hueR = multiplier*r;
  let hueG = multiplier*g;
  let hueB = multiplier*b;

  // Calculate brightness?
  let maxHue = Math.max(hueR, hueG, hueB);
  let minHue = Math.min(hueR, hueG, hueB);
  let brightness = ((maxHue + minHue)/2.0 - 127.5) * (255.0/127.5)/multiplier;

  let rgbw = [r - brightness, g - brightness, b - brightness, brightness];
  for (var i = 0; i < rgbw.length; i++) {
    rgbw[i] = parseInt(rgbw[i]);
    if (rgbw[i] > 255) {
      rgbw[i] = 255;
    }
    else if (rgbw[i] < 0) {
      rgbw[i] = 0;
    }
  }
  return rgbw;
}

// Inspiration http://www.qlcplus.org/forum/viewtopic.php?t=7491
// RGBx=RGB+(255-RGB)*W/3/255
function rgbwToRGB(r, g, b, w) {
  let rgb = [r, g, b];
  for (var i = 0; i < rgb.length; i++) {
    rgb[i] = rgb[i] + (255 - rgb[i])*w/3/255;
    rgb[i] = parseInt(rgb[i]);
  }
  return rgb;
}

// From https://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? [
    parseInt(result[1], 16),
    parseInt(result[2], 16),
    parseInt(result[3], 16)
  ] : null;
  // return result ? {
  //     r: parseInt(result[1], 16),
  //     g: parseInt(result[2], 16),
  //     b: parseInt(result[3], 16)
  // } : null;
}

function rgbToHex(r, g, b) {
  return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

function nonzeroIndex(hex) {
  let rgb = hexToRgb(hex);
  let count = 0;
  let index = -1;
  for (var i = 0; i < rgb.length; i++) {
    if (rgb[i] != 0) {
      count++;
      index = i;
    }
  }
  if (count === 1) {
    return index;
  }
  else {
    return -1;
  }
}
