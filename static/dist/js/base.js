/**
 * Created by Administrator on 2017/11/16.
 */

NProgress.start();
NProgress.configure({ trickleRate: 10, trickleSpeed: 100 });
$(document).ready(function(){
    setTimeout("NProgress.done();",1000);

});
$(document).ready(function() {
    $('#nameform').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            oldpassword:{
                message: "The password is not valid",
                validators:{
                    notEmpty:{
                        'message': "原密码不得为空！"
                    },
                    stringLength:{
                        min:6,
                        max:30,
                        message:'用户名长度必须大于6个字符，且小于30个字符.'
                    },
                }
            },
            password: {
                validators: {
                    notEmpty: {
                        message: '新密码不得为空！'
                    },
                    stringLength:{
                        min:6,
                        max:30,
                        message:'用户名长度必须大于6个字符，且小于30个字符.'
                    },
                }
            },
            password2: {
                validators: {
                    identical: {
                        field: 'password',
                        message: '两次输入的密码不相符'
                    },
                    notEmpty: {
                        message: '新密码不得为空！'
                    },
                    stringLength:{
                        min:6,
                        max:30,
                        message:'用户名长度必须大于6个字符，且小于30个字符.'
                    },
                }
            }
        }
    });
});
