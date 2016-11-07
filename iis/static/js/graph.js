;(function() {
  "use strict"
  var joint = require("jointjs")
  var $ = require("jquery")
  var controls = require("./modules/graph_controls")
  var api = require("./modules/api.js")
  var modals = require("./modules/detail_modals.js")

  var graph = new joint.dia.Graph
  var paper = new joint.dia.Paper({
    el: $('#diagram'),
    model: graph,
    gridSize: 10
  })
  paper.drawGrid()

  var nodes = new Map()
  var canvas_event_lock = {lock: null}

  var add_node = new controls.AddProcess({
    button: $("#iis_add_process"),
    svg: getSvg,
    add_node: placeNode,
    lock: canvas_event_lock
  })

  var add_pipe = new controls.AddPipe({
    button: $("#iis_add_pipe"),
    lock: canvas_event_lock,
    node_elements: getNodes,
    nodes: nodes,
    add_pipe: makePipe,
    processes: api.processes,
    paper: paper
  })


  function getSvg() {
    return $("#diagram").find("svg").first()
  }

  function getNodeMouseDownHandler(node) {
    return function(event) {
      switch (event.which) {
      case 1:
        $("[model-id=" + node.id + "]").addClass("focus")
        break
      case 3:
        event.preventDefault()
        event.stopPropagation()
        displayProcessModal(node)
        break
      default:
        break
      }
    }
  }

  function getNodeMouseUpHandler(node) {
    return function(event) {
      switch(event.which) {
      case 1:
        $("[model-id=" + node.id + "]").removeClass("focus")
        break
      default:
        break
      }
    }
  }

  function placeNode(relX, relY) {
    var node = new joint.shapes.basic.Rect({
      position: {x: relX, y: relY},
      size: {width: 100, height: 30},
      attrs: {rect: {fill: 'blue'},
              text: {text: 'my box', fill: 'white'}}
    })
    graph.addCell(node)
    displayProcessModal(node)
    $("[model-id=" + node.id +"]").on("mousedown.main_handler",
                                      getNodeMouseDownHandler(node))
    $("[model-id=" + node.id +"]").on("mouseup.main_handler",
                                      getNodeMouseUpHandler(node))
  }

  function getNodes() {
    return getSvg().find("[data-type=basic\\.Rect]")
  }

  function makePipe(source, target) {
    var link = new joint.dia.Link({
      source: {id: source.attr("model-id")},
      target: {id: target.attr("model-id")}
    })
    graph.addCell(link)
  }

  function displayProcessModal(node) {
    api.processes.get(function (data) {
      var modal_element = $("#iis_details_modal") 
      var modal_vars = {
        processes: data,
        modal: modal_element,
        modal_body: modal_element.find(".modal-body").first(),
        set_button: modal_element.find("button#set_button").first(),
        success: function (process) {
          node.attr({
            text: {text: process, fill: "white"}
          })
          nodes.set(node.id, {
            node: node,
            process: process
          })
        }
      }
      modals.processModal(modal_vars)
    })
  }

}())