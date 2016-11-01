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

  module.exports = {
    AddPipe: AddPipe
  }
}())