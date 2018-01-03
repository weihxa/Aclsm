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
$('#jump-users').addClass("active");
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
        url:'/jump/users/',
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
function del_users(doc,id) {
    if(confirm("确认要删除此账户，删除后无法恢复哦？")){
                    $.ajax({
    url:'/jump/deluser/',
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

};
function edit_users(id) {
		$("#userid").attr("value",id);
		$("#e_username").attr("value",$("#username"+id).text());
		$("#e_description").text($("#description"+id).text());
			$('#myModaledit').modal({show:true});
}
$(document).ready(function(){
$('#e_tijiao').click(function(){
    $("#e_retune").text('正在处理....');
     $.ajax({
        type:'POST',
        url:'/jump/edit_users/',
        data:$("#edituser").serialize(),
        cache:false,
        dataType:'json',
        success:function(data){
            if (data[0])
              {
                $("#e_retune").css('color','green');
                $("#e_retune").text(data[1]+'，2秒后刷新页面。');
                setTimeout(function(){
                window.location.reload();
                },2000);
              }
            else
              {
              $("#e_retune").css('color','red');
                $("#e_retune").text(data[1]);
              }

        },
         error:function(){
            $("#e_retune").css('color','red');
            $("#e_retune").text('数据请求失败，请刷新页面尝试!');
        }
    });
});
})
$(document).ready(function() {
    $('#createuser')
        .bootstrapValidator({
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                username: {
                    validators: {
                        notEmpty: {
                        message: '账户名不得为空！'
                        },
                        stringLength:{
                        min:0,
                        max:15,
                        message:'账户名应小于15个字符.'
                    },
                    }
                },
                u_password: {
                    validators: {
                        notEmpty: {
                        message: '账户密码不得为空！'
                        }
                    }
                },
                description: {
                    validators: {
                        notEmpty: {
                        message: '权限不得为空！'
                        }
                    }
                },
            }
        });
});
$(document).ready(function() {
$('#edituser')
    .bootstrapValidator({
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            e_description: {
                validators: {
                        notEmpty: {
                        message: '权限不得为空！'
                        }
                    }
            },
        }
    });
})