/**
* Created by Administrator on 2017/11/16.
*/


$(document).ready(function(){
    $('#weeklyul').addClass("menu-open");
    $('#weekly').addClass("active");
    $('#weeklyli').addClass("active");
});
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
function del_users(doc,id) {
if(confirm("确认要删除此条计划？")){
        $.ajax({
            url:'/delweekly/',
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
function edit_users(id) {
    $("#eweeklyid").attr("value",id);
    $("#eweeklys").attr("value",$('#tweeklys'+id).text());
    $("#eworkplan").attr("value",$('#tworkplan'+id).text());
    $("#ecompletion").attr("value",$('#tcompletion'+id).text());
    $("#ecoordination").attr("value",$('#tcoordination'+id).text());
    $("#enextweek").attr("value",$('#tnextweek'+id).text());
    $('#myModaledit').modal({show:true});

};
function copy_weekly(id) {
    $("#weeklys").attr("value",$('#copyweeklys'+id).text());
    $("#workplan").attr("value",$('#copyworkplan'+id).text());
    $("#completion").attr("value",$('#copycompletion'+id).text());
    $("#coordination").attr("value",$('#copycoordination'+id).text());
    $("#nextweek").attr("value",$('#copynextweek'+id).text());
    $('#myModal2').modal({show:true});
};
$(document).ready(function() {
    $('#creategroup')
    .bootstrapValidator({
    feedbackIcons: {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'glyphicon glyphicon-remove',
        validating: 'glyphicon glyphicon-refresh'
    },
    fields: {
        weeklys: {
            validators: {
                notEmpty: {
                message: '兄弟至少要写个计划吧！'
                },
            }
        },
    }
});
});
$(document).ready(function() {
    $('#editgroup')
    .bootstrapValidator({
    feedbackIcons: {
        valid: 'glyphicon glyphicon-ok',
        invalid: 'glyphicon glyphicon-remove',
        validating: 'glyphicon glyphicon-refresh'
    },
    fields: {
        eweeklys: {
            validators: {
                notEmpty: {
                message: '兄弟至少要写个计划吧！'
                },
            }
        },
    }
    });
})