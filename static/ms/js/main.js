jQuery(function($){
    var status = $('#status');
  (function(){
      $.ajax({
          url: '',
          type: 'POST',
          data: '1',
          success: callback,
          cache: false,
          contentType: false,
          processData: false
      });
    function callback(msg) {
    if (msg.status) {
        $("#mark").css('display','none');
        $("#status").css('display','block');
      status.text(msg.status);

      return;
    }
    // var ws_url = window.location.href.replace('http', 'ws'),
    var ws_url = 'ws://' + window.location.host,
        join = (ws_url[ws_url.length-1] == '/' ? '' : '/'),
        url = ws_url + join + 'ws?id=' + msg.id,
        socket = new WebSocket(url),
        terminal = document.getElementById('#terminal'),
        term = new Terminal({cursorBlink: true});

    term.on('data', function(data) {
      // console.log(data);
      socket.send(data);
    });

    socket.onopen = function(e) {
      $('.container').hide();
      term.open(terminal, true);
      term.toggleFullscreen(true);
    };

    socket.onmessage = function(msg) {
      // console.log(msg);
      term.write(msg.data);
    };

    socket.onerror = function(e) {
      console.log(e);
    };

    socket.onclose = function(e) {
      term.destroy();
      open(location, '_self').close();
    };
  }
}());
});

