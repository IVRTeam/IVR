$("li.menuItem.nav-parent").click(function(){
	if($(this).hasClass("opened")){
		
		$(this).removeClass("opened nav-expanded");
	}else{
		$("li.menuItem.nav-parent").removeClass("opened nav-expanded");
		$(this).addClass("opened nav-expanded");
	}
	});
//左侧导航条高度动态设置
$(".sidebar-menu").css("min-height",screen.height/1.5);
    $(function () {
	 	$(document).on("click", "#msgtable tr", function() {
			bootbox.dialog({
    		title: $(this).find('td').eq(2).html(),
    		message: $(this).find('td').eq(3).html()
			});
			$(this).removeClass('read');
			$(this).addClass('read');
        });
 });
 

 
