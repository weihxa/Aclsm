/**
* Created by Administrator on 2017/12/12.
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
    function del_page(doc,id) {
        if(confirm("确认要删除此playbook，删除后无法恢复哦？")){
                $.ajax({
                url:'/scms/delplaybook/',
                type:'POST',
                data:{modify:id},
                success:function (arg) {
                    window.location.reload();
                },
                error:function () {
                    console.log('failed');
                }
            });
            }

        };
$(document).ready(function () {
  $("#myFiles").change(function () {
    var filepath = $("input[name='myfile']").val();
    var extStart = filepath.lastIndexOf(".");
    var ext = filepath.substring(extStart, filepath.length).toUpperCase();
    if (ext != ".GZ") {
      $("#retune").css('color','red');
      $("#returns").attr('disabled','disabled');
        $("#retune").text('格式错误,仅能上传.tar.gz压缩文件！');
      return false;
    } else {
        $("#retune").text('');
        $("#returns").removeAttr('disabled');
    }
  });
});
function subimtBtn() {
var form = $("form[name=fileForm]");
$("#returns").text('正在处理....');
var options = {
url:'/scms/playbook_upload/', //上传文件的路径
type:'post',
dataType:'json',
success:function(data){
 console.log(data[0])
if (data[0])
          {
            $("#retune").css('color','green');
            console.log(data[1])
            $("#retune").text(data[1]+'2秒后刷新页面。');
            $("#returns").text('成功!');
            setTimeout(function(){
            window.location.reload();
            },2000);
          }
        else
          {
          $("#retune").css('color','red');
          $("#returns").text('提交');
          $("#returns").attr('disabled','disabled');
            $("#retune").text(data[1]);
          }

    },
     error:function(){
        $("#retune").css('color','red');
        $("#returns").attr('disabled','disabled');
        $("#retune").text('数据请求失败，请刷新页面尝试!');
    }
};
form.ajaxSubmit(options);
}
