;(function() {
  var $ = require("jquery")
  
  var processes = {
    _data: null,
    get: function(success) {
      if(this._data == null) {
        $.get("/jobs/api/processes", function(data, status, thing) {
          this._data = data
          success(this._data)
        })
      } else {
        success(this._data)
      }
    }
  }





  module.exports = {
    processes: processes
  }
}())