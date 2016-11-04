;(function () {
  "use strict"
  var $ = require('jquery')

  function AddPipe(vars) {
    this.detach = function() {
      vars.button.off("click.main_handler")
    }

    vars.button.on("click.main_handler", function() {
      if (vars.lock.lock != null) {
        return
      }

      vars.button.addClass("active")
      
      var source = null
      var elements = vars.nodes()

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
        vars.lock.lock = null
        vars.button.removeClass("active")
        vars.add_pipe(source, $(this))
      }

      function clearClickHandlers() {
        elements.each(function() {
          $(this).off('click.add_pipe')
        })
      }
      vars.lock.lock = clearClickHandlers
    })
  } 

  function AddProcess(vars) {
    this.detach = function() {
      vars.button.off("click.main_handler")
    }

    var canvas = vars.svg()
    vars.button.on("click.main_handler", function() {
      if (vars.lock.lock != null) {
        return
      }
      vars.button.addClass("active")

      canvas.addClass("clickable")
      canvas.on("click.add_process", function(e) {
        var parentOffset = $(this).parent().offset()
        var relX = e.pageX - parentOffset.left
        var relY = e.pageY - parentOffset.top

        vars.add_node(relX, relY)

        clearClickHandlers()
        vars.button.removeClass("active")
        canvas.removeClass("clickable")
      })

      function clearClickHandlers() {
        canvas.off("click.add_process")
        vars.lock.lock = null
      }

      vars.lock.lock = clearClickHandlers
    })


  }

  module.exports = {
    AddPipe: AddPipe,
    AddProcess: AddProcess
  }
}())