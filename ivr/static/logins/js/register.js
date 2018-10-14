function btnAction()
{
    if ($("#pwds").val()=='' || $("#names").val()=='' || $("#phones").val()=='' || $("#uids").val()=='')
        {
            $("#shows").show();
        }
    else
    {
        $.ajax({
            type: 'GET',
            dataType: 'json',
            timeout: 3000,
            url: '/logins/checkUid/',
            async: false,
            cache: false,
            data: {
                "uid": $("#uids").val()
            },
            error: function(msg) {
                alert(msg.status);
            },
            success: function(data){
                if(data.status=='有')
                {
                    bootbox.alert({
                    message: "用户名已存在，请重新输入",
                    callback: function () {
                            $("#uids").val('');
                            $("#pwds").val('');
                            $("#names").val('');
                            $("#phones").val('');
                        }
                    })
                }
                else
                {
                    $.ajax({
                        type: 'POST',
                        timeout: 3000,
                        url: '/logins/registerCheck/',
                        async: false,
                        data: {
                            "uid" : $("#uids").val(),
                            "pwd" : $("#pwds").val(),
                            "username" : $("#names").val(),
                            "phone" : $("#phones").val(),
                        },
                        error: function(msg) {
                            alert(msg.status);
                        },
                        success: function(data){
                            if (data=='200')
                            {
                                var dialog = bootbox.dialog({
                                    message: '<p class="text-center">注册成功，正在前往登录界面</p>',
                                    closeButton: false
                                });
                                dialog.init(function(){
                                    setTimeout(function(){
                                        $(location).attr('href', '/');
                                    }, 1500);
                                });
                            }
                            else
                            {
                                bootbox.alert({
                                    message: "注册失败，请重新注册",
                                    callback: function () {
                                        $("#uids").val('');
                                        $("#pwds").val('');
                                        $("#names").val('');
                                        $("#phones").val('');
                                    }
                                })
                            }
                        }
                    });
                }
            }
        });
    };
}
