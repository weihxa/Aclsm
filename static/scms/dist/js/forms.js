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
$(document).ready(function() {
    $("#textrarval").change(function() {
        var filepath = $("textarea[name='cmd']").val();
        if (filepath == "") {
            $("#returns").attr('disabled', 'disabled');
            $("#textrarval").addClass("redxsq");
            return false;
        } else {
            $("#textrarval").removeClass("redxsq");
            $("#returns").removeAttr('disabled');
        }
    });
});
$(document).ready(function() {
    $("#textrarval2").change(function() {
        var filepath = $("textarea[name='gcmd']").val();
        if (filepath == "") {
            $("#g_return").attr('disabled', 'disabled');
            $("#textrarval2").addClass("redxsq");
            return false;
        } else {
            $("#textrarval2").removeClass("redxsq");
            $("#g_return").removeAttr('disabled');
        }
    });
});
function del_device(doc, id) {
  $("#xianshi").text('正在执行，请稍后。。。');
  $('#myModal2').modal({
    show: true
  });
  $.ajax({
    type: "POST",
    url: "/scms/cmdrun/",
    data: $('#nameform22').serialize(),
    error: function(request) {
      $("#xianshi").addClass('redxsq');
      $("#xianshi").text('请求失败！');
      $('#myModal2').modal({
        show: true
      });
    },
    success: function(arg) {
      var obj = jQuery.parseJSON(arg);
      if (obj.status == 1) {
        $("#xianshi").addClass('redxsq');
      } else {
        $("#xianshi").removeClass('redxsq');
      }
      $("#xianshi").text(obj.data);

    }
  });
}
function group(doc, id) {
  $("#xianshi").text('正在执行，请稍后。。。');
  $('#myModal2').modal({
    show: true
  });
  $.ajax({
    type: "POST",
    url: "/scms/cmdrun/",
    data: $('#nameform3').serialize(),
    error: function(request) {
      $("#xianshi").addClass('redxsq');
      $("#xianshi").text('请求失败！');

      $('#myModal2').modal({
        show: true
      });
    },
    success: function(arg) {
      var obj = jQuery.parseJSON(arg);
      if (obj.status == 1) {
        $("#xianshi").addClass('redxsq');
      } else {
        $("#xianshi").removeClass('redxsq');
      }
      $("#xianshi").text(obj.data);

    }
  });
}
// 初始化
$('#optgroup').multiSelect({
  selectableHeader: "<div class='custom-header'>可选主机</div>",
  selectionHeader: "<div class='custom-header'>已选主机</div>",
  selectableOptgroup: true,
  afterSelect: function(values) {
    select.modifyselectNum('#optgroup');
  },
  afterDeselect: function(values) {
    select.modifyselectNum('#optgroup');
  }
});