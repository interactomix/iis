;(function () {
  "use strict"
  var $ = require("jquery")
  var _ = require("lodash")

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
      var elements = vars.node_elements()

      elements.each(function() {
        var node = vars.nodes.get($(this).attr("model-id")).node
        node.findView(vars.paper).highlight()
        $(this).on("click.add_pipe", sourceClickHandler)
        $(this).on("mousedown.mask_mousedown_event",
                   function(e) {e.stopPropagation()})
      })

      function sourceClickHandler(e) {
        elements.each(function() {
          vars.nodes.get($(this).attr("model-id")).node
            .findView(vars.paper).unhighlight()
        })
        source = $(this)
        var source_process = vars.nodes.get($(this).attr("model-id")).process
        vars.processes.get(function(data) {
          var source_postset = _.find(
            data.processes,
            {"id": source_process}
          ).postset
          console.log(source_postset)
          elements.each(function() {
            if(_.includes(
              source_postset,
              vars.nodes.get($(this).attr("model-id")).process
            )) {
              $(this).on('click.add_pipe', targetClickHandler)

              vars.nodes.get($(this).attr("model-id")).node
                .findView(vars.paper).highlight()
            } else {
              $(this).addClass("disabled")
            }
          })
        })
        clearClickHandlers()
      }

      function targetClickHandler(e) {
        clearClickHandlers()
        vars.lock.lock = null
        vars.button.removeClass("active")
        elements.each(function() {
          vars.nodes.get($(this).attr("model-id")).node
            .findView(vars.paper).unhighlight()
          $(this).off("mousedown.mask_mousedown_event")
          $(this).removeClass("disabled")
        })
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