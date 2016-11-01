var joint = require('jointjs')
var $ = require('jquery')
var controlls = require('./modules/graph_controlls')

var graph = new joint.dia.Graph;

var paper = new joint.dia.Paper({
  el: $('#diagram'),
  width: 600,
  height: 800,
  model: graph,
  gridSize: 1
});


var nodes = new Map();

$('#iis_add_process').click(function(e) {
  $('#diagram').find('svg').on('click.add_process', function(e) {
    var parentOffset = $(this).parent().offset(); 
    var relX = e.pageX - parentOffset.left;
    var relY = e.pageY - parentOffset.top;
    var node = new joint.shapes.basic.Rect({
      position: {x: relX, y: relY},
      size: {width: 100, height: 30},
      attrs: { rect: { fill: 'blue' }, text: { text: 'my box', fill: 'white' } }
    });
    graph.addCells([node]);
    nodes.set(node.id, node);
    $(this).off('click.add_process');
  });
});


var add_pipe = new controlls.AddPipe(
  $("#iis_add_pipe"),
  function() {
    return $("#diagram").find("svg").first().find("[data-type=basic\\.Rect]")
  },
  finish
)

function finish(source, target) {
  var link = new joint.dia.Link({
    source: {id: source.attr("model-id")},
    target: {id: target.attr("model-id")}
  });
  graph.addCell(link);
}