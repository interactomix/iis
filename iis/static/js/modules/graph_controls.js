;(function () {
  "use strict"
  var $ = require('jquery')

  function AddPipe(button, nodes, add_pipe) {
    this.detach = function() {
      button.off("click.main_handler")
    }

    button.on("click.main_handler", function() {
      var source = null
      var elements = nodes()

      elements.each(function() {
        $(this).on('click.add_pipe', sourceClickHandler)
      })

      function sourceClickHandler(e) {
        source = $(this)
        clearClickHandlers()
        elements.each(function() {
          $(this).on('click.add_pipe', targetClickHandler)
        })
      }

      function targetClickHandler(e) {
        clearClickHandlers()
        add_pipe(source, $(this))
      }

      function clearClickHandlers() {
        elements.each(function() {
          $(this).off('click.add_pipe')
        })
      }

    })
  } 

  function AddProcess(button, svg, add_node) {
    this.detach = function() {
      button.off("click.main_handler")
    }

    var canvas = svg()
    button.on("click.main_handler", function() {
      canvas.addClass("clickable")
      canvas.on("click.add_process", function(e) {
        var parentOffset = $(this).parent().offset()
        var relX = e.pageX - parentOffset.left
        var relY = e.pageY - parentOffset.top

        add_node(relX, relY)

        canvas.off("click.add_process")
        canvas.removeClass("clickable")
      })
    })


  }

  module.exports = {
    AddPipe: AddPipe,
    AddProcess: AddProcess
  }
}())