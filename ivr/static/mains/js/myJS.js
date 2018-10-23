function btnModify()
{
    if($("#alt_name").val()=='' || $("#alt_pwd").val()=='' || $("#alt_phone").val()=='')
    {
        alert("信息不完整！");
    }
    else{
        $.ajax({
                type: 'POST',
                dataType: 'json',
                timeout: 3000,
                url: '/mains/modify/',
                async: false,
                data: {name:$("#alt_name").val(), pwd:$("#alt_pwd").val(), phone:$("#alt_phone").val()},
                error: function(msg) {
                    alert(msg.status);
                },
                success: function(data){
                    if (data.status=='200')
                    {
                        $(location).attr('href', '/mains/');
                    }
                    else {
						bootbox.alert({
                        message: "修改失败",
                        callback: function () {
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