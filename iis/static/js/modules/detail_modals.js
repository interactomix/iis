;(function() {
  "use strict"
  var _ = require("lodash")

  function processModal(vars) {
    var select_options = ""
    _.forEach(vars.processes.processes, function (process, i, collection) {
      select_options += '<option value="' + process.id + '">'
        + process.name  + '</option>'
    })

    var modal_body_html = "<select name=process>" +
                          select_options +
                          "</select>"
    vars.modal_body.html(modal_body_html)

    vars.modal.modal({
      backdrop: "static",
      show: true
    })

    vars.set_button.on("click.main_handler", function () {
      vars.modal.modal("hide")
      vars.set_button.off("click.main_handler")
    })

    vars.modal.on("hide.bs.modal", function() {
      var process = vars.modal_body.find("[name=process]").val()
      vars.modal_body.html("")
      vars.modal.off("hide.bs.modal")
      vars.success(process)
    })
  }

  module.exports = {
    processModal: processModal
  }
  
}())