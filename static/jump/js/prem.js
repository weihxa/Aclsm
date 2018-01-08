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
$(document).ready(function(){
$('#userul').addClass("menu-open");
$('#jump-prem').addClass("active");
$('#userli').addClass("active");
});
$(document).ready(function() {
$('#example').dataTable();
} );
$(document).ready(function(){
$('#tijiao2').click(function(){
    $("#retune").text('正在处理....');
     $.ajax({
        type:'POST',
        url:'/jump/prem/',
        data:$("#createuser").serialize(),
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
function del_group(doc,id) {
    if(confirm("确认要删除此用户绑定，删除后无法恢复哦？")){
    $.ajax({
    url:'/jump/delprem/',
    type:'POST',
    data:{modify:id},
    success:function (arg) {
        window.location.reload();
        var obj = jQuery.parseJSON(arg);
        var this_id = $(doc).attr('id');
    },
    error:function () {
        console.log('failed');
    }
});
}
}