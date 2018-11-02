var obj = [];
$(function(){
    var page = $('#states').DataTable({
            "processing" : true,
            "serverSide" : true,
            "bSort" : false,
            //"aLengthMenu" : [ 5, 10, 20, 30 ], // 动态指定分页后每页显示的记录数。
            "aLengthMenu" : [5, 10, 15, 20, 25, 30],
            "lengthChange" : true, // 是否启用改变每页显示多少条数据的控件
            "iDisplayLength" : 10, // 默认每页显示多少条记录
            "ordering":true,
            "filter" : true,
            "dom" : 'ftipr<"bottom"l>',
            "ajax" : {
                "url" : "/calls/stateDatas/",
                "type" : "POST",
                "data" : {
                            "callState" : '',
                            "lengthStart" : '',
                            "lengthEnd" : '',
                            "timeStart" : '',
                            "timeEnd" : ''
                         }
            },
            "aoColumns" : [
                { // aoColumns设置列时，不可以任意指定列，必须列出所有列。
                    "mData" : "id",
                    "orderable" : false, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "4%"
                },
                { // aoColumns设置列时，不可以任意指定列，必须列出所有列。
                    "mData" : "sid",
                    "visible" : false,
                    "orderable" : false, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "4%"
                },
                {
                    "mData" : "phone",
                    "orderable" : true, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "10%",

                },
                {
                    "mData" : "status",
                    "orderable" : true, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "6%",
                },
                { // aoColumns设置列时，不可以任意指定列，必须列出所有列。
                    "mData" : "callTime",
                    "orderable" : true, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "10%"
                },
                { // aoColumns设置列时，不可以任意指定列，必须列出所有列。
                    "mData" : "callLength",
                    "orderable" : true, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "8%"
                },
                {
                    "mData" : "digits",
                    "orderable" : false, // 禁用排序
                    "sDefaultContent" : "",
                    "sWidth" : "10%",

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
            $("#states input[name='recordcheck']").prop("checked", true);
            /*$("#calls input[name='recordcheck']").each(function () {
                //将checkbox中的val放入变量中
                checked.push($(this).val());
            });
            alert(checked);*/
        }
        else {
            $("#states input[name='recordcheck']").prop("checked", false);
        }
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
                    recordstr = recordstr + "," + obj[indexs].sid;
                }
                else
                {
                    recordstr = recordstr + obj[indexs].sid;
                }
                i++;
            }
        );
        recordstr = recordstr + ')';
        $.ajax({
            data : {
                "recordstr" : recordstr
            },
            url : '/calls/deleteState/',
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
    // 点击筛选按钮，弹出筛选框
    $("#filter").click(function() {
        $("#callState").val("");
        $("#callLength").val("");
        var myDate = new Date();
        //获取当前年
        var year=myDate.getFullYear();
        //获取当前月
        var month=myDate.getMonth()+1;
        //获取当前日
        var date=myDate.getDate();
        if (month<'10')
        {
            month='0'+ month;
        }
        if (date<'10')
        {
            date='0'+ date;
        }
        var now=year+'-'+month+"-"+date;
        $("#demo").val(now);
        $("#demo2").val(now);
        $("#filters").modal('show');
    });

    //点击筛选完成按钮
    $("#finishshai").click(function() {
        obj=[];
        var callState = $("#callState option:selected").val();
        var lengthStart = $("#callLength option:selected").val();
        if (lengthStart == "")
        {
            lengthEnd="";
        }
        else
        {
            lengthEnd=parseInt(lengthStart)+30;
        }
        var timeStart = $("#demo").val();
        var timeEnd = $("#demo2").val();
        console.log("callState:"+callState+";lengthStart:"+lengthStart+";lengthEnd:"+lengthEnd+";timeStart:"+timeStart+";timeEnd:"+timeEnd);

        if (timeStart == "") {
            bootbox.alert({
                message: "请选择呼叫开始时间!",
                size: 'small'
            });
        } else if (timeEnd == "") {
            bootbox.alert({
                message: "请选择呼叫结束时间!",
                size: 'small'
            });
        }
        else {
            if (timeStart > timeEnd) {
                bootbox.alert({
                    message: "日期时间段选择错误",
                    size: 'small'
                });
                return false;
            }
            page = $('#states').DataTable({
                        "processing" : true,
                        "serverSide" : true,
                        "bSort" : false,
                        "bDestroy" : true,
                        //"aLengthMenu" : [ 5, 10, 20, 30 ], // 动态指定分页后每页显示的记录数。
                        "aLengthMenu" : [5, 10, 15, 20, 25, 30],
                        "lengthChange" : true, // 是否启用改变每页显示多少条数据的控件
                        "iDisplayLength" : 10, // 默认每页显示多少条记录
                        "ordering":true,
                        "filter" : true,
                        "dom" : 'ftipr<"bottom"l>',
                        "ajax" : {
                            "url" : "/calls/stateDatas/",
                            "type" : "POST",
                            "data" : {
                                        "callState" : callState,
                                        "lengthStart" : lengthStart,
                                        "lengthEnd" : lengthEnd,
                                        "timeStart" : timeStart,
                                        "timeEnd" : timeEnd
                                     }
                        },
                        "aoColumns" : [
                            { // aoColumns设置列时，不可以任意指定列，必须列出所有列。
                                "mData" : "id",
                                "orderable" : false, // 禁用排序
                                "sDefaultContent" : "",
                                "sWidth" : "4%"
                            },
                            { // aoColumns设置列时，不可以任意指定列，必须列出所有列。
                                "mData" : "sid",
                                "visible" : false,
                                "orderable" : false, // 禁用排序
                                "sDefaultContent" : "",
                                "sWidth" : "4%"
                            },
                            {
                                "mData" : "phone",
                                "orderable" : true, // 禁用排序
                                "sDefaultContent" : "",
                                "sWidth" : "10%",

                            },
                            {
                                "mData" : "status",
                                "orderable" : true, // 禁用排序
                                "sDefaultContent" : "",
                                "sWidth" : "6%",
                            },
                            { // aoColumns设置列时，不可以任意指定列，必须列出所有列。
                                "mData" : "callTime",
                                "orderable" : true, // 禁用排序
                                "sDefaultContent" : "",
                                "sWidth" : "10%"
                            },
                            { // aoColumns设置列时，不可以任意指定列，必须列出所有列。
                                "mData" : "callLength",
                                "orderable" : true, // 禁用排序
                                "sDefaultContent" : "",
                                "sWidth" : "8%"
                            },
                            {
                                "mData" : "digits",
                                "orderable" : false, // 禁用排序
                                "sDefaultContent" : "",
                                "sWidth" : "10%",

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
        $("#filters").modal('hide');
        }
    })



});