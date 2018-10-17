function refresh_check_code(ths) {
    ths.src += '?';
    //src后面加问好会自动刷新验证码img的src
}
function btnRegister()
{
	$(location).attr('href', '/logins/register/');
}

function btnLogin()
{
    if($("#uids").val()=='' || $("#pwds").val()=='' || $("#authCode").val()=='')
    {
        $("#shows").show();
        src = $("#codeImage").attr("src") + '?';
        $("#codeImage").attr("src",src);
    }
    else{
        $.ajax({
                type: 'POST',
                dataType: 'json',
                timeout: 3000,
                url: '/logins/loginCheck/',
                async: false,
                data: $('#form').serialize(),
                error: function(msg) {
                    alert(msg.status);
                },
                success: function(data){
                    if (data.status=='200')
                    {
                        var dialog = bootbox.dialog({
                            message: '<p class="text-center">登录成功，正在前往主界面</p>',
                            closeButton: false
                        });
                        dialog.init(function(){
                            setTimeout(function(){
                                $(location).attr('href', '/logins/testSession/');
                            }, 1500);
                        });
                    }
                    else if(data.status=='400')
                    {
                        bootbox.alert({
                        message: "验证码错误，请重新输入",
                        callback: function () {
                                src = $("#codeImage").attr("src") + '?';
                                $("#codeImage").attr("src",src);
                                $("#authCode").val('');
                            }
                        })
                    }
                    else {
                        bootbox.alert({
                        message: "用户名,密码错误，请重新输入",
                        callback: function () {
                                src = $("#codeImage").attr("src") + '?';
                                $("#codeImage").attr("src",src);
                                $("#uids").val('');
                                $("#pwds").val('');
                                $("#authCode").val('');
                            }
                        })
                    }
                }
            });
    }
}