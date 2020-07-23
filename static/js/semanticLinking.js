var deps_dictionary = {};
var canvasTop = 0;
var left = 0;
var tofromseparation = 0;
// degrees to radians, because most people think in degrees
function degToRad(angle_degrees) {
  return angle_degrees / 180 * Math.PI;
}

function drawHorizArc(ctx, inax, inbx, y, label, alpha_degrees, upside) {
  var alpha = degToRad(alpha_degrees);
  var startangle = (upside ? ((3.0 / 2.0) * Math.PI + alpha) : ((1.0 / 2.0) * Math.PI - alpha));
  var endangle = (upside ? ((3.0 / 2.0) * Math.PI - alpha) : ((1.0 / 2.0) * Math.PI + alpha));
  var ax = Math.min(inax, inbx);
  var bx = Math.max(inax, inbx);
  var circleyoffset = ((bx - ax) / 2) / Math.tan(alpha);
  var circlex = (ax + bx) / 2.0;
  var circley = y + (upside ? 1 : -1) * circleyoffset;
  var radius = Math.sqrt(Math.pow(circlex - ax, 2) + Math.pow(circley - y, 2));
  ctx.beginPath();
  if (upside) {
    ctx.moveTo(bx, y);
    ctx.arc(circlex, circley, radius, startangle, endangle, 1);
    var midx = ((bx + ax) / 2.0) - 15.0;
    var midy = y * (alpha + 1);
    ctx.font = '12px Arial';
    ctx.fillText(label, midx, midy);
    console.log("mid", circleyoffset, circley, radius, alpha, y, startangle, endangle, (startangle + endangle) / 2);
  } else {
    ctx.moveTo(bx, y);
    ctx.arc(circlex, circley, radius, startangle, endangle, 1);
  }
  ctx.stroke();
}
// draw the head of an arrow (not the main line)
// ctx: canvas context
// xX,y: coords of arrow point
// angle_from_north_clockwise: angle of the line of the arrow from horizontal
// upside: true=above the horizontal, false=below
// barb_angle: angle between barb and line of the arrow
// filled: fill the triangle? (true or false)
function drawArrowHead(ctx, x, y, angle_from_horizontal_degrees, upside, //mandatory
  barb_length, barb_angle_degrees, filled) { //optional
  (barb_length == undefined) && (barb_length = 13);
  (barb_angle_degrees == undefined) && (barb_angle_degrees = 26);
  (filled == undefined) && (filled = true);
  var alpha_degrees = (upside ? -1 : 1) * angle_from_horizontal_degrees;
  //first point is end of one barb
  var plus = degToRad(alpha_degrees - barb_angle_degrees);
  a = x + (barb_length * Math.cos(plus));
  b = y + (barb_length * Math.sin(plus));
  //final point is end of the second barb
  var minus = degToRad(alpha_degrees + barb_angle_degrees);
  c = x + (barb_length * Math.cos(minus));
  d = y + (barb_length * Math.sin(minus));
  ctx.beginPath();
  ctx.moveTo(a, b);
  ctx.lineTo(x, y);
  ctx.lineTo(c, d);
  if (filled) {
    ctx.fill();
  } else {
    ctx.stroke();
  }
  return true;
}
// draw a horizontal arcing arrow
// ctx: canvas context
// inax: start x value
// inbx: end x value
// y: y value
// alpha_degrees: angle of ends to horizontal (30=shallow, >90=silly)
function drawHorizArcArrow(ctx, inax, inbx, y, label, //mandatory
  alpha_degrees, upside, barb_length) { //optional
  (alpha_degrees == undefined) && (alpha_degrees = 45);
  (upside == undefined) && (upside = true);
  drawHorizArc(ctx, inax, inbx, y, label, alpha_degrees, upside);
  if (inax > inbx) {
    drawArrowHead(ctx, inbx, y, alpha_degrees * 0.9, upside, barb_length);
  } else {
    drawArrowHead(ctx, inbx, y, (180 - alpha_degrees * 0.9), upside, barb_length);
  }
  return true;
}

function drawArrow(ctx, fromelem, toelem, label, //mandatory
  above, angle) { //optional
  (above == undefined) && (above = true);
  (angle == undefined) && (angle = 45); //degrees
  // tofromseparation = Math.abs(toelem.offsetLeft - fromelem.offsetLeft)
  // have to create a check here to see if it is highlighted otherwise it calculates
  // the width incorrectly
  console.log("offset", fromelem.offsetWidth, toelem.offsetWidth, fromelem.offsetLeft, toelem.offsetLeft);
  console.log(fromelem);
  console.log(toelem);
  try {
    console.log(fromelem.parentNode.nodeName);
    if (fromelem.parentNode.nodeName == "MARK") {
      console.log("from-left", fromelem.parentNode.offsetLeft);
      midfrom = fromelem.parentNode.offsetLeft;
    } else {
      midfrom = fromelem.offsetLeft;
    }
  } catch (e) {
    console.log(e);
    midfrom = fromelem.offsetLeft + (fromelem.clientwidth / 2);
    fromelem.offsetLeft + (fromelem.clientWidth / 2);
  }
  try {
    if (toelem.parentNode.nodeName == "MARK") {
      midto = (toelem.parentNode.offsetLeft + toelem.offsetLeft);
    } else {
      midto = toelem.offsetLeft;
    }
  } catch (e) {
    midto = toelem.offsetLeft;
  }
  //var y = above ? (fromelem.offsetTop - top) : (fromelem.offsetTop + fromelem.offsetHeight - top); |
  var y = fromelem.offsetTop + (above ? 0 : fromelem.offsetHeight) + canvasTop;
  console.log(y, midto, midfrom);
  drawHorizArcArrow(ctx, midfrom, midto, y, label, angle, above);
}

function drawDeps() {
  var spanboxdiv = document.getElementById("sentence");
  // will eventually have to add custom ids to these sentences to break them up into their own dependency structures
  try {

    console.log(spanboxdiv);
    var canvasdiv = document.getElementById("canvas");
    if (canvasdiv == null) {
      $("<canvas id='canvas' class='sentence' style='border:1px solid red; margin-top: -" + spanboxdiv.clientHeight * 2 + "px ' width='" + spanboxdiv.parentNode.clientWidth + "' height='" + spanboxdiv.clientHeight * 6 + "'> < /canvas>").insertBefore('#sentence');
      canvasdiv = document.getElementById("canvas");
      var ctx = canvasdiv.getContext("2d");
    } else {
      var ctx = canvasdiv.getContext("2d");
      ctx.clearRect(0, 0, canvasdiv.width, canvasdiv.height);
    }
  } catch (e) {
    $("<canvas id='canvas' class='sentence' style='border:1px solid red; margin-top: -" + spanboxdiv.clientHeight * 2 + "px' width='" + spanboxdiv.parentNode.clientWidth + "' height='" + spanboxdiv.clientHeight * 6 + "'> </canvas>").insertBefore('#sentence');
    var canvasdiv = document.getElementBylId("canvas");
    var ctx = canvasdiv.getContext("2d");
  }
  console.log("drawing")
  // chnge this took look for first child inspanbox in case id changes
  var first = document.getElementById("0")
  console.log("canvasdiv");
  console.log(canvasdiv.parentNode.offsetLeft);
  if (canvasdiv.parentNode.offsetLeft > 1) {
    left = canvasdiv.parentNode.offsetLeft + spanboxdiv.offsetLeft;
  } else {
    left = spanboxdiv.offsetLeft;
  }
  console.log(canvasdiv);
  // need to fix this
  canvasTop = canvasdiv.offsetTop - spanboxdiv.offsetHeight;
  console.log(canvasTop);
  for (var key in deps_dictionary) {
    for (var val in deps_dictionary[key]) {
      fromid = String(deps_dictionary[key][val].split(":")[0]);
      toid = String(deps_dictionary[key][val].split(":")[1]);
      console.log("linking", fromid, "to", toid);
      drawArrow(ctx, document.getElementById(fromid), document.getElementById(toid), String(key), true, 30);
    }
  }
}