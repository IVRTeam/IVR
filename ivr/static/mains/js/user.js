function previewImage(file)
{
      var MAXWIDTH  = 120;
      var MAXHEIGHT = 120;
      var div = document.getElementById('preview');
      if (file.files && file.files[0])
      {
          div.innerHTML ='<img id="imghead" class="img-circle bk-img-60">';
          var img = document.getElementById('imghead');
          img.onload = function(){
            var rect = clacImgZoomParam(MAXWIDTH, MAXHEIGHT, 120, 120);
            img.width  =  rect.width;
            img.height =  rect.height;
//                 img.style.marginLeft = rect.left+'px';
            img.style.marginTop = rect.top+'px';
          }
          var reader = new FileReader();
          reader.onload = function(evt){img.src = evt.target.result;}
          reader.readAsDataURL(file.files[0]);
      }
      else //兼容IE
      {
        var sFilter='filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale,src="';
        file.select();
        var src = document.selection.createRange().text;
        div.innerHTML = '<img id=imghead>';
        var img = document.getElementById('imghead');
        img.filters.item('DXImageTransform.Microsoft.AlphaImageLoader').src = src;
        var rect = clacImgZoomParam(MAXWIDTH, MAXHEIGHT, img.offsetWidth, img.offsetHeight);
        status =('rect:'+rect.top+','+rect.left+','+rect.width+','+rect.height);
        div.innerHTML = "<div id=divhead style='width:"+rect.width+"px;height:"+rect.height+"px;margin-top:"+rect.top+"px;"+sFilter+src+"\"'></div>";
      }
      //弹出模态框 是否确认上传
      setTimeout(function(){
            $("#uploadImg").modal('show');
      }, 800);

}

function clacImgZoomParam( maxWidth, maxHeight, width, height ){
    var param = {top:0, left:0, width:width, height:height};
    if( width>maxWidth || height>maxHeight )
    {
        rateWidth = width / maxWidth;
        rateHeight = height / maxHeight;

        if( rateWidth > rateHeight )
        {
            param.width =  maxWidth;
            param.height = Math.round(height / rateWidth);
        }else
        {
            param.width = Math.round(width / rateHeight);
            param.height = maxHeight;
        }
    }
    param.left = Math.round((maxWidth - param.width) / 2);
    param.top = Math.round((maxHeight - param.height) / 2);
    return param;
}
/*
     ** 点击取消上传文件按钮，刷新页面
*/
$("#upCancer").click(function(){
    $(location).attr('href','/mains/user/');
});
/*
     ** 点击确认上传文件按钮
*/
$("#upCommit").click(function(){
    $("#uploadImg").modal('hide');
    var form_data = new FormData();
    var file_info = $('#file')[0].files[0];//文件对象
    form_data.append('file',file_info);
    //ajax提交给后端处理
    $.ajax({
        type:'POST',
        dataType:'json',
        timeout:3000,
        data:form_data,
        url:'/mains/uploadImg/',
        processData:false, // 告诉jQuery不要去处理发送的数据
        contentType:false, // 告诉jQuery不要去设置Content-Type请求头
        error:function(){
            bootbox.alert({
                message:"头像上传失败,请重新上传！",
                size:'small',
                callback: function(){
                    $(location).attr('href','/mains/user/');  //刷新页面
                }
            });
        },
        success:function(data){
            if(data.status =='200'){
                var dialog = bootbox.dialog({
                    message: '<p class="text-center">头像上传成功！</p>',
                    size : 'small',
                    closeButton: false
                });
                dialog.init(function(){
                    setTimeout(function(){
                        $(location).attr('href','/mains/user/');
                    }, 800);
                });
            }
            else
            {
                bootbox.alert({
                    message:"头像上传失败,请重新上传！",
                    size:'small',
                    callback: function(){
                        $(location).attr('href','/mains/user/');  //刷新页面
                    }
                });
            }

        }
    });
});

//提交按钮：检查信息是否填全，向后台提交数据
$("#submit").click(function(){
    var name = $("#userName").val()
    var phone = $("#TelePhone").val()
    var pw = $("#possword").val()
    var pw2 = $("#repossword").val()
    if(name=="")
    {
         bootbox.alert({
                message : "请填写姓名",
                size : 'small'
         });
         return;
    }
    if(phone=="")
    {
         bootbox.alert({
                message : "请填写电话号码",
                size : 'small'
            });
         return;
    }
    else // 检查是否11位有效手机号码
    {
        var myreg=/^[1][3,4,5,7,8][0-9]{9}$/;
            if (!myreg.test(phone)) {
                bootbox.alert({
                    message: "电话号码有误，请重新输入！",
                    size : 'small',
                    callback: function () {
                           $("#TelePhone").val('');
                        }
                    });
                return;
            }
    }
    if(pw=="")
    {
         bootbox.alert({
                message : "请填写要修改的密码",
                size : 'small'
            });
         return;
    }
    if(pw2=="")
    {
         bootbox.alert({
                message : "请填写确认密码",
                size : 'small'
            });
         return;
    }
    if(pw!=pw2){
        bootbox.alert({
                message : "两次密码输入不正确，请重新输入",
                size : 'small'
         });
        $("#possword").val()
        $("#repossword").val()
        return;
    }
    $.ajax({
        type: 'POST',
        dataType: 'json',
        timeout: 3000,
        url: '/mains/modify/',
        async: false,
        data: {
            name:name,
            phone:phone,
            pwd:pw,
        },
        error: function(msg) {
            alert(msg.status);
        },
        success: function(data){
            if (data.status=='200')
            {
                var dialog = bootbox.dialog({
                    message: '<p class="text-center">修改成功！</p>',
                    size : 'small',
                    closeButton: false
                });
                dialog.init(function(){
                    setTimeout(function(){
                        $(location).attr('href','/mains/user/');
                    }, 1000);
                });
            }
            else {
                bootbox.alert({
                    message: "修改失败",
                    size : 'small',
                })
            }
//          清空密码框的内容
            $("#possword").val('');
            $("#repossword").val('');
        }
    });
});

//重置：清空4个输入框
$("#reset").click(function(){
    $("#userName").val('');
    $("#TelePhone").val('');
    $("#possword").val('');
    $("#repossword").val('');
});

