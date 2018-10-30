$("#certainimport").click(function(){
    //将文件以form_data方式提交
    var form_data = new FormData();
    var file_info = $('#btn_file')[0].files[0];//文件对象
    form_data.append('file',file_info);
    //获取单选框内容
    var e = document.getElementsByName("uptype");
    var item_id="";
    for(var i=0;i<e.length;i++){
        if(e[i].checked)
            item_id = e[i].value;
    }
    form_data.append('type',item_id);
    // 判断文件是否为空
    if(file_info==undefined){
         bootbox.alert({
            message : "导入的文件不能为空",
            size : 'small'
        });
        return false;
    }
    //判断是否为excel文件
    var fireStr = $("#btn_file").val();
    var fireL = fireStr.lastIndexOf(".");
    fireStr = fireStr.substring(fireL);
    if(fireStr != ".xls" && fireStr!=".xlsx"){
        bootbox.alert({
            message:"请导入excel格式文档，后缀名为.xls或.xlsx",
        });
        $("#btn_file").val("");
        return false;
    }
    //ajax提交给后端处理
    $.ajax({
        type:'POST',
        dataType:'json',
        timeout:3000,
        data:form_data,
        url:'/calls/fileUpload/',
        processData:false, // 告诉jQuery不要去处理发送的数据
        contentType:false, // 告诉jQuery不要去设置Content-Type请求头
        error:function(){
            bootbox.alert({
                message:"导入失败",
                size:'small'
            });
        },
        success:function(data){
            if(data.status == '200'){
                bootbox.alert({
                    message: "数据导入成功,导入"+ data.y +" 条,重复" + data.x + "条,有" + data.z + "行为空!",
                });
            }
            else if(data.status == '400'){
                bootbox.alert({
                    message: "您上传的不是模板文件，请先下载模板文件再上传！",
                });
            }
            else{
                 bootbox.alert({
                    message:"导入失败500",
                    size:'small'
                });
            }
        }
    });
    //清空模态框的内容并消失
    $("#btn_file").val("");//清空文件框的内容
    $("input[name='uptype']")[0].checked="checked";//清空选择框内容
    $('#import').modal('hide');//模态框消失
});