from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    doctype = "Loyalty Point Entry"

    df = {
        "fieldname": "previous_loyalty_points",
        "fieldtype": "Int",
        "label": "Previous Loyalty Points",
        "read_only": 1,
        "default": 0,
        "insert_after": "redeem_against",
    }

    create_custom_field(doctype, df)