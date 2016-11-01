var joint = require('jointjs');
var jquery = require('jquery');

var graph = new joint.dia.Graph;

var paper = new joint.dia.Paper({
    el: $('#diagram'),
    width: 600,
    height: 800,
    model: graph,
    gridSize: 1
});


var nodes = new Map()

$('#iis_add_process').click(function(e) {
  $('#diagram').find('svg').on('click.add_process', function(e) {
    console.log(this);
    var parentOffset = $(this).parent().offset(); 
    var relX = e.pageX - parentOffset.left;
    var relY = e.pageY - parentOffset.top;
    console.log(relX)
    console.log(relY)
    node = new joint.shapes.basic.Rect({
      position: {x: 0, y: relY},
      size: {width: 100, height: 30},
      attrs: { rect: { fill: 'blue' }, text: { text: 'my box', fill: 'white' } }
    });
    graph.addCells([node]);
    nodes.set(node.id, node);
    $(this).off('click.add_process');
  });
});

$('#iis_add_pipe').click(function() {
  source = null;
  target = null;

  var elements = $('#diagram').find('svg').first().find('.joint-cell');
  elements.each(function() {
    if (nodes.has($(this).attr("model-id"))) {
      $(this).on('click.add_pipe', sourceClickHandler);
    }
  });

  function sourceClickHandler(e) {
    source = $(this);
    clearClickHandlers();
    elements.each(function() {
      if (nodes.has($(this).attr("model-id"))) {
        $(this).on('click.add_pipe', targetClickHandler)
      }
    });
  }

  function targetClickHandler(e) {
    target = $(this);
    clearClickHandlers();
    finish();
  }

  function clearClickHandlers() {
    elements.each(function() {
      $(this).off('click.add_pipe');
    });
  }

  function finish() {
    var link = new joint.dia.Link({
      source: {id: source.attr("model-id")},
      target: {id: target.attr("model-id")}
    });
    graph.addCell(link);
  }
});