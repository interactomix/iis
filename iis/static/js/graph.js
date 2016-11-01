;(function() {
  "use strict"
  var joint = require('jointjs')
  var $ = require('jquery')
  var controls = require('./modules/graph_controls')

  var graph = new joint.dia.Graph

  var paper = new joint.dia.Paper({
    el: $('#diagram'),
    width: 600,
    height: 800,
    model: graph,
    gridSize: 1
  })


  var nodes = new Map()

  var add_node = new controls.AddProcess(
    $("#iis_add_process"),
    function() {
      return $("#diagram").find("svg").first()
    },
    function(relX, relY) {
      var node = new joint.shapes.basic.Rect({
        position: {x: relX, y: relY},
        size: {width: 100, height: 30},
        attrs: {rect: {fill: 'blue'},
                text: {text: 'my box', fill: 'white'}}
      })
      graph.addCell(node)
      nodes.set(node.id, node)
    }
  )

  var add_pipe = new controls.AddPipe(
    $("#iis_add_pipe"),
    function() {
      return $("#diagram").find("svg").first().find("[data-type=basic\\.Rect]")
    },
    function(source, target) {
      var link = new joint.dia.Link({
        source: {id: source.attr("model-id")},
        target: {id: target.attr("model-id")}
      })
      graph.addCell(link)
    }
  )
}())