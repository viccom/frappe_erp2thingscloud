// Copyright (c) 2020, viccom.dong and contributors
// For license information, please see license.txt

frappe.ui.form.on('ThingsCloud Settings', {
	// refresh: function(frm) {
	setup: function(frm) {
		frm.events.refresh_status(frm);
	},
	refresh: function(frm) {
		frm.add_custom_button(__("Refresh Server Status"), function() {
			frm.events.refresh_status(frm);
		}).removeClass("btn-default").addClass("btn-primary");

		var grid_html = '<div class="form-group"> \
							<div class="clearfix"> \
								<label class="control-label" style="padding-right: 0px;">%(title)s</label> \
							</div> \
							<div class="control-input-wrapper"> \
								<img height="32px" src="/assets/erp2thingscloud/images/connect/%(status)s.png"> \
							</div> \
						</div>'

		var thingscloud_status = frm.doc.thingscloud_status  || 'none';
		var s = $(repl(grid_html, {title: __("ThingsCloud"), status: thingscloud_status.toLowerCase()}));
		$(frm.fields_dict['server_status_html'].wrapper).append(s);

	},
	refresh_status: function(frm) {
		return frappe.call({
			doc: frm.doc,
			method: "refresh_status",
			freeze: true,
			callback: function(r) {
				if(!r.exc) frm.reload_doc();
			}
		})
	}
	// }
});
