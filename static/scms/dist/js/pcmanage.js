/**
* Created by Administrator on 2017/11/17.
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
function generate(doc,id) {
$.ajax({
    url:'/scms/generate/',
    type:'POST',
    data:{modify:id},
    success:function (arg) {
        $(doc).attr("disabled","disabled");
        var obj = jQuery.parseJSON(arg);
        console.log(obj.status);
    },
    error:function () {
       console.log('failed');
    }
});
};
function del_device(doc,id) {
    $("#devid").attr("value",id);
$.ajax({
    url:'/scms/deldevice/',
    type:'POST',
    data:{modify:id},
    success:function (arg) {
        window.location.reload();
        var obj = jQuery.parseJSON(arg);
        var this_id = $(doc).attr('id');
        console.log(this_id);
        console.log(obj.status);
    },
    error:function () {
        console.log('failed');
    }
});
};

$(document).ready(function() {
$('#pcconfig')
.bootstrapValidator({
feedbackIcons: {
    valid: 'glyphicon glyphicon-ok',
    invalid: 'glyphicon glyphicon-remove',
    validating: 'glyphicon glyphicon-refresh'
},
fields: {
    ipAddress: {
        validators: {
            notEmpty: {
            message: 'ip地址不得为空！'
            },
            ip: {
                message: '您输入的IP地址不合法！'
            }
        }
    }
}
})
.find('[name="ipAddress"]').mask('099.099.099.099');
});
$(document).ready(function(){
$('#tijiao2').click(function(){
    $("#retune").text('正在处理....');
     $.ajax({
        type:'POST',
        url:'/scms/adddevice/',
        data:$("#pcconfig").serialize(),
        cache:false,
        dataType:'json',
        success:function(data){
            if (data[0])
              {
                $("#retune").css('color','green');
                $("#retune").text(data[1]+'，2秒后刷新页面。');
                setTimeout(function(){
                window.location.reload();
                },2000);
              }
            else
              {
              $("#retune").css('color','red');
                $("#retune").text(data[1]);
              }

        },
         error:function(){
            $("#retune").css('color','red');
            $("#retune").text('数据请求失败，请刷新页面尝试!');
        }
    });
});
});