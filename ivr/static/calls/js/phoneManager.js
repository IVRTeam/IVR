var obj = [];
$(function(){
    var page = $('#calls').DataTable({
            "processing" : true,
            "serverSide" : true,
            "bSort" : false,
            //"aLengthMenu" : [ 5, 10, 20, 30 ], // 动态指定分页后每页显示的记录数。
            "aLengthMenu" : [ 3, 5, 10, 15, 20 ],
            "lengthChange" : true, // 是否启用改变每页显示多少条数据的控件
            //"iDisplayLength" : 10, // 默认每页显示多少条记录
            "iDisplayLength" : 5,
            "ordering":true,
            "filter" : true,
            "dom" : 'ftipr<"bottom"l>',
            "ajax" : {
                "url" : "/calls/datas/",
                "type" : "POST"
            },
            "aoColumns" : [
                { // aoColumns设置列时，不可以任意指定列，必须列出所有列。
                    "mData" : "id",
                    "orderable" : false, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "4%"
                },
                { // aoColumns设置列时，不可以任意指定列，必须列出所有列。
                    "mData" : "pid",
                    "visible" : false,
                    "orderable" : false, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "4%"
                },
                {
                    "mData" : "number",
                    "orderable" : true, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "10%",

                },
                {
                    "mData" : "name",
                    "orderable" : false, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "6%",
                },
                { // aoColumns设置列时，不可以任意指定列，必须列出所有列。
                    "mData" : "address",
                    "orderable" : false, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "10%"
                },
                { // aoColumns设置列时，不可以任意指定列，必须列出所有列。
                    "mData" : "num",
                    "orderable" : true, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "8%"
                },
                {
                    "mData" : "star",
                    "orderable" : true, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "10%",

                },
                {
                    "mData" : "createTime",
                    "orderable" : true, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "6%"
                },
				{
                    "mData" : "id",
                    "orderable" : false, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "8%",
                    "render" : function(data,type, row) {
                        obj.push(row);
                        return data = '<span id="updateDetail" class="icon-edit edit-color" value="'
                                + (obj.length - 1)
                                + '"></span>';
                        }
				}],
            "columnDefs" : [ {
                    "orderable" : false, // 禁用排序
                    "targets" : [ 0 ], // 指定的列
                    "data" : "id",
                    "render" : function(data, type, row) {
                        obj.push(row);
                        return '<label><input type="checkbox" name="recordcheck" value="'
                                + (obj.length - 1)
                                + '" class="ck" id="checkHa"></label>';
                    }
                }],

        "language" : {
            "lengthMenu" : "每页 _MENU_ 条记录",
            "zeroRecords" : "没有找到记录",
            "info" : "第 _PAGE_ 页 ( 总共 _PAGES_ 页 )",
            "infoEmpty" : "无记录",
            "infoFiltered" : "(从 _MAX_ 条记录过滤)",
            "sSearch" : "搜索：",
            "oPaginate" : {
                "sFirst" : "首页",
                "sPrevious" : " 上一页 ",
                "sNext" : " 下一页 ",
                "sLast" : " 尾页 "
                }
            }
        })
    // //全选反选
    $("#ck1").on("click", function()
    {
        if ($(this).prop("checked") == true) {
            var checked = [];
            $("#calls input[name='recordcheck']").prop("checked", true);
            /*$("#calls input[name='recordcheck']").each(function () {
                //将checkbox中的val放入变量中
                checked.push($(this).val());
            });
            alert(checked);*/
        }
        else {
            $("#calls input[name='recordcheck']").prop("checked", false);
        }
    });
    //点击增加,弹出增加框
    $(document).on("click", "#ZJ", function() {
        $("#add").css("display","block");
    });
    //关闭增加的模态框，这里用模态框会和那个bootbox冲突
    $(document).on("click", "#closebas", function() {
        $("#add").css("display","none");
        $("#add input").val('');
        $(".colle").prop('checked',true);
        $("#add select").val('');
    });
    //点击增加确定按钮
    //增加框的js控制
    $(document).on("click", "#submitForm_0", function() {
        var phone=$("#phones").val();
        var name=$("#names").val();
        var address=$("#addresss").val();
        var star=$("#stars").val();
        if(phone=="")
        {
             bootbox.alert({
                    message : "请填写电话号码",
                    size : 'small'
                });
             return;
		}
		if(name=="")
        {
             bootbox.alert({
                    message : "请填写姓名",
                    size : 'small'
                });
             return;
		}
		if(address=="")
        {
             bootbox.alert({
                    message : "请填写地址",
                    size : 'small'
                });
             return;
		}
		if(star=="")
        {
             bootbox.alert({
                    message : "请选择用户等级",
                    size : 'small'
                });
             return;
		}
        $.ajax({
                type: 'POST',
                dataType: 'json',
                timeout: 3000,
                url: '/calls/addPhone/',
                async: false,
                data: {
                    "phone": phone,
                    "name": name,
                    "address": address,
                    "star": star,
                },
                error: function(msg) {
                    alert(msg.status);
                },
                success: function(data){
                    if (data.status=='200')
                    {
                        bootbox.alert({
                        message: "增加号码成功!",
                        callback: function () {
                                $("#add").css("display","none");
                                $("#add input").val('');
                                $(".colle").prop('checked',true);
                                $("#add select").val('');
                                page.draw(false);
                            }
                        })
                    }
                    else if(data.status=='400')
                    {
                        bootbox.alert({
                        message: "增加号码已存在!",
                        callback: function () {
                                $("#phones").val('');
                                $("#names").val('');
                                $("#addresss").val('');
                                $("#stars").val('');
                            }
                        })
                    }
                    else {
                        bootbox.alert({
                        message: "增加失败，请重新输入!",
                        callback: function () {
                                $("#phones").val('');
                                $("#names").val('');
                                $("#addresss").val('');
                                $("#stars").val('');
                            }
                        })
                    }
                }
        });
    });

    // 点击删除按钮,判断是否已选择
    $("#delete").click(function() {
        var chk_value = [];
        $('input[name="recordcheck"]:checked').each(function() {
            chk_value.push($(this).val());
        });
        if (chk_value.length == 0) {
            bootbox.alert({
                message : "您还没有选择任何内容",
                size : 'small'
            });
            return;
        }
        $("#deleteOneModal").modal('show');

    });
    // 确认删除
    $("#delSubmit").click(function() {
        var recordstr = '(';
        var i = 0;
        var indexs;
        $("input[type='checkbox'][name='recordcheck']:checked").each(function()
            {
                indexs = $(this).val();
                if (i != 0)
                {
                    recordstr = recordstr + "," + obj[indexs].pid;
                }
                else
                {
                    recordstr = recordstr + obj[indexs].pid;
                }
                i++;
            }
        );
        recordstr = recordstr + ')';
        $.ajax({
            data : {
                "recordstr" : recordstr
            },
            url : '/calls/deletePhone/',
            async : false,
            type : "POST",
            dataType : "json",
            success : function(data) {
                    bootbox.alert({
                        message : data.status,
                        size : 'small'
                    });
                    $("#deleteOneModal").modal('hide');
                    page.draw(false);
            },
            error : function(data) {
                alert("请求异常");
            }
        });
    });

    var index;
    // 点击修改图标，填充修改模态框中的内容
    $(document).on("click", "#updateDetail", function() {
        index = $(this).attr("value");
        $("#Epid").val(obj[index].pid);
        $("#Ephones").val(obj[index].number);
        $("#Ephone").val(obj[index].number);
        $("#Ename").val(obj[index].name);
        $("#Eaddress").val(obj[index].address);
        $("#Enum").val(obj[index].num);
        $("#Estar").val(obj[index].star);
        $("#EcreateTime").val(obj[index].createTime);
        $("#edit").modal('show');
    });

    //确认修改
    $("#saverun").click(function() {
        var pid=$("#Epid").val();
        var phones=$("#Ephones").val();
        var phone=$("#Ephone").val();
        var name=$("#Ename").val();
        var address=$("#Eaddress").val();
        var star=$("#Estar").val();
        var flag="1";
        if(phone=="")
        {
             bootbox.alert({
                    message : "请填写电话号码",
                    size : 'small'
                });
             return;
		}
		if(name=="")
        {
             bootbox.alert({
                    message : "请填写姓名",
                    size : 'small'
                });
             return;
		}
		if(address=="")
        {
             bootbox.alert({
                    message : "请填写地址",
                    size : 'small'
                });
             return;
		}
		if(star=="")
        {
             bootbox.alert({
                    message : "请选择用户等级",
                    size : 'small'
                });
             return;
		}
		if(phones!=phone)
		{
		    flag="0";
		}
        $.ajax({
                type: 'POST',
                dataType: 'json',
                timeout: 3000,
                url: '/calls/alterPhone/',
                async: false,
                data: {
                    "pid": pid,
                    "phone": phone,
                    "name": name,
                    "address": address,
                    "star": star,
                    "flag": flag
                },
                error: function(msg) {
                    alert(msg.status);
                },
                success: function(data){
                    if (data.status=='200')
                    {
                        bootbox.alert({
                        message: "修改成功!",
                        callback: function () {
                                $("#edit").modal('hide');
                                page.draw(false);
                            }
                        })
                    }
                    else if(data.status=='400')
                    {
                        bootbox.alert("修改号码已存在!");
                    }
                    else {
                        bootbox.alert("修改失败，请重新输入!");
                    }
                }
        });
    });


    // 点击呼叫按钮,判断是否已选择
    $("#HJ").click(function() {
        var chk_value = [];
        $('input[name="recordcheck"]:checked').each(function() {
            chk_value.push($(this).val());
        });
        if (chk_value.length == 0) {
            bootbox.alert({
                message : "您还没有选择任何内容",
                size : 'small'
            });
            return;
        }
        //呼叫
        var checked = [];
        var Oneindex;
        $("input[type='checkbox'][name='recordcheck']:checked").each(function()
            {
                Oneindex = $(this).val();
                //var Oneindex= $(this).parent('tr').find("span").attr("value");
                checked.push(obj[Oneindex].number);
            }
        );
        //alert(checked);
        $.ajax({
            url: '/calls/callNumber/',
            type: 'GET',
            dataType: 'json',
            data: {
                "recordstr": checked.toString(),
            },
            success: function (data) {
                bootbox.alert("电话号码正在呼叫...");
            },
            error : function(data) {
                alert("请求异常");
            },
        });

    });






});