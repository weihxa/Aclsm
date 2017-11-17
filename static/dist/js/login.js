/**
 * Created by Administrator on 2017/11/16.
 */
$(document).ready(function() {
    $('#loginForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            password:{
                message: "The password is not valid",
                validators:{
                    notEmpty:{
                        'message': "password不得为空！"
                    },
                    stringLength:{
                        min:6,
                        max:30,
                        message:'用户名长度必须大于6个字符，且小于30个字符.'
                    }
                }
            },

            email: {
                validators: {
                    notEmpty: {
                        message: 'Email不得为空！'
                    },
                    emailAddress: {
                        message: '您输入的Email不合法,请重新输入'
                    }
                }
            },
            code: {
                validators: {
                    notEmpty: {
                        message: '请输入正确的验证码！'
                    },
                    stringLength:{
                        min:4,
                        max:4,
                        message:'正确的验证码为4个字符！'
                    }
                }
            }
        }
    });
});
function refresh_check_code(ths) {
    ths.src += '?';
    //src后面加问好会自动刷新验证码img的src
}
