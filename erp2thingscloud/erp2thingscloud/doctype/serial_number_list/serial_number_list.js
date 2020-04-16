// Copyright (c) 2020, viccom.dong and contributors
// For license information, please see license.txt

frappe.ui.form.on('Serial Number list', {
    // refresh: function(frm) {
    refresh: function (frm) {
        frm.add_custom_button('Resend SerialNo', function () {
            var skey = $("div.title-text").text();
            console.log("增加一个自定义按钮");
            console.log(skey);
            // frappe.call({
            // 	method: 'frappe.core.doctype.translation.translation.contribute_translation',
            // 	args: {
            // 		"language": frm.doc.language,
            // 		"contributor": frm.doc.owner,
            // 		"source_name": frm.doc.source_name,
            // 		"target_name": frm.doc.target_name,
            // 		"doc_name": frm.doc.name
            // 	}
            // });
        }).addClass('btn-primary');
    }



    // }
});
