frappe.listview_settings['Serial Number list'] = {
    onload: function (listview) {
        listview.page.add_menu_item(__("Resend SerialNo"), function () {
            console.log("增加一个自定义下拉菜单");
            // listview.refresh();
            frappe.call({
            	method:'erp2thingscloud.tasks.resend.resend_failed_serials',
            	callback: function() {
            		listview.refresh();
            	}
            });
        });
    },
	refresh: function(doclist){
        doclist.page.add_inner_button(__("Resend SerialNo"), function () {
            console.log("增加一个自定义按钮");
            frappe.call({
            	method:'erp2thingscloud.tasks.resend.resend_failed_serials',
            	callback: function() {
                    doclist.refresh();
            	}
            });

        }).addClass('btn-primary');
	}

};
