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
        var filepath = $("input[name='p_name']").val();
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

function subimtBtn() {
    var form = $("form[name=fileForm]");
    $("#returns").text('正在处理....');
    var options = {
        url: '/scms/roles/',
        type: 'post',
        dataType: 'json',
        success: function(data) {
            if (data[0]) {
                $("#zhuangtai2").removeClass("alert-danger");
                $("#zhuangtai2").addClass("alert-success");
                $("#zhuangtai2").css('display', 'block');
                $("#zhuangtai2").text(data[1]);
                $("#returns").text('成功!');
                setTimeout(function() {
                    $("#zhuangtai2").css('display', 'none');
                    $("#returns").text('提交任务');
                },
                2000);
            } else {
                $("#zhuangtai2").removeClass("alert-success");
                $("#zhuangtai2").addClass("alert-danger");
                $("#zhuangtai2").css('display', 'block');
                $("#returns").text('提交任务');
                $("#returns").attr('disabled', 'disabled');
                $("#zhuangtai2").text(data[1]);
                setTimeout(function() {
                    $("#returns").removeAttr('disabled');
                    $("#returns").text('提交任务');
                },
                2000);
            }

        },
        error: function() {
            $("#zhuangtai2").addClass("alert-danger");
            $("#zhuangtai2").css('display', 'block');
            $("#mess").text('数据请求失败，请刷新页面后尝试!');
        }
    };
    form.ajaxSubmit(options);
}