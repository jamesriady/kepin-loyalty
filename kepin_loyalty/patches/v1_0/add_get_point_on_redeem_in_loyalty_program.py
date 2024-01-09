from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    doctype = "Loyalty Program"

    df = {
        "fieldname": "get_point_on_redeem",
        "fieldtype": "Check",
        "label": "Get Point on Redeem",
        "default": 0,
        "insert_after": "auto_opt_in",
    }

    create_custom_field(doctype, df)