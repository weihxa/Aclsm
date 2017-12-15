/**
 * Created by Administrator on 2017/12/15.
 */

var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});
function logshow(doc, id) {
  var obj = setTimeout('myrefresh()', 6000);
  $('#logs').text($("#logs" + id).text());
  $('#myModal2').modal({
    show: true
  });
  clearInterval(obj);
};
function myrefresh() {
  window.location.reload();
};
$(function() {
  var obj = setTimeout('myrefresh()', 6000); // 每6秒刷新一次页面
  $("a.stopfresh").click(function() {
    clearInterval(obj); // 点击即停止刷新
  });
});
$(function() {
  $('#myModal2').on('hide.bs.modal',
  function() {
    setTimeout('myrefresh()', 1000);
  });
});