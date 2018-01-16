var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
}
});
$(document).ready(function(){
$('#userul').addClass("menu-open");
$('#jump-alogs').addClass("active");
$('#userli').addClass("active");
});
$(document).ready(function() {
$('#example').dataTable();
} );
function logshow(id) {
    $.ajax({
        url:'/jump/get_log/',
        type:'GET',
        data:{modify:id},
        success:function (arg) {
            var obj = jQuery.parseJSON(arg);
            $('#logs').text(obj);
            $('#myModal2').modal({show:true});

        },
        error:function () {
            console.log('failed');
            $('#logs').text('日志获取失败，请联系管理员！');
            $('#myModal2').modal({show:true});
        }
    });
    }
$("body").addClass("sidebar-collapse");