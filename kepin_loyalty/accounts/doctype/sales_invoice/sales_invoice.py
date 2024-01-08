from __future__ import unicode_literals
import frappe
from frappe.utils import today, cint, flt, getdate, add_days
from erpnext.accounts.doctype.loyalty_program.loyalty_program import \
	get_loyalty_program_details_with_points

def on_claim_loyalty_point(doc, method=None):
    if not doc.is_return and doc.loyalty_program:
        remaining_points = get_remaining_points(doc)
        set_previous_point(doc, remaining_points)
    elif doc.is_return and doc.return_against and doc.loyalty_program:
        against_si_doc = frappe.get_doc("Sales Invoice", doc.return_against)
        
        against_si_doc.delete_loyalty_point_entry()

        revert_deleted_invoice_loyalty_point_entry(against_si_doc)
        remaining_points = get_remaining_points(against_si_doc, filters={'creation': ['<', against_si_doc.creation]})
        set_previous_point(against_si_doc, remaining_points)

        make_return_invoice_loyalty_point_entry(doc, against_si_doc)
        remaining_points = get_remaining_points(doc)
        set_previous_point(doc, remaining_points)

def on_cancel_claim_loyalty_point(doc, method=None):
    if doc.is_return and doc.return_against and doc.loyalty_program:
        # delete return sales invoice loyalty point entry
        return_si_doc = frappe.get_doc("Sales Invoice", doc.name)
        return_si_doc.delete_loyalty_point_entry()

        against_si_doc = frappe.get_doc("Sales Invoice", doc.return_against)
        remaining_points = get_remaining_points(against_si_doc, filters={'creation': ['<', against_si_doc.creation]})
        set_previous_point(against_si_doc, remaining_points)

def make_return_invoice_loyalty_point_entry(doc, against_si_doc):
    returned_amount = against_si_doc.get_returned_amount()
    current_amount = flt(against_si_doc.grand_total) - cint(against_si_doc.loyalty_amount)
    eligible_amount = returned_amount

    lp_details = get_loyalty_program_details_with_points(against_si_doc.customer, company=against_si_doc.company,
        current_transaction_amount=current_amount, loyalty_program=against_si_doc.loyalty_program,
        expiry_date=against_si_doc.posting_date, include_expired_entry=True)
    if lp_details and getdate(lp_details.from_date) <= getdate(against_si_doc.posting_date) and \
        (not lp_details.to_date or getdate(lp_details.to_date) >= getdate(against_si_doc.posting_date)):

        collection_factor = lp_details.collection_factor if lp_details.collection_factor else 1.0
        points_earned = cint(eligible_amount/collection_factor)

        new_doc = frappe.get_doc({
            "doctype": "Loyalty Point Entry",
            "company": doc.company,
            "loyalty_program": lp_details.loyalty_program,
            "loyalty_program_tier": lp_details.tier_name,
            "customer": doc.customer,
            "sales_invoice": doc.name,
            "loyalty_points": -1 * points_earned,
            "purchase_amount": eligible_amount,
            "expiry_date": add_days(doc.posting_date, lp_details.expiry_duration),
            "posting_date": doc.posting_date
        })
        new_doc.flags.ignore_permissions = 1
        new_doc.save()
        doc.set_loyalty_program_tier()

def revert_deleted_invoice_loyalty_point_entry(doc):
    returned_amount = 0
    current_amount = flt(doc.grand_total) - cint(doc.loyalty_amount)
    eligible_amount = current_amount - returned_amount
    lp_details = get_loyalty_program_details_with_points(doc.customer, company=doc.company,
        current_transaction_amount=current_amount, loyalty_program=doc.loyalty_program,
        expiry_date=doc.posting_date, include_expired_entry=True)
    if lp_details and getdate(lp_details.from_date) <= getdate(doc.posting_date) and \
        (not lp_details.to_date or getdate(lp_details.to_date) >= getdate(doc.posting_date)):

        collection_factor = lp_details.collection_factor if lp_details.collection_factor else 1.0
        points_earned = cint(eligible_amount/collection_factor)

        new_doc = frappe.get_doc({
            "doctype": "Loyalty Point Entry",
            "company": doc.company,
            "loyalty_program": lp_details.loyalty_program,
            "loyalty_program_tier": lp_details.tier_name,
            "customer": doc.customer,
            "sales_invoice": doc.name,
            "loyalty_points": points_earned,
            "purchase_amount": eligible_amount,
            "expiry_date": add_days(doc.posting_date, lp_details.expiry_duration),
            "posting_date": doc.posting_date
        })
        new_doc.flags.ignore_permissions = 1
        new_doc.save()
        doc.set_loyalty_program_tier()

def get_remaining_points(doc, filters={}):
    expiry_date = doc.posting_date
    if not expiry_date:
        expiry_date = today()

    default_filters =  {
        'customer': doc.customer, 
        'sales_invoice': ["!=", doc.name], 
        'loyalty_program': doc.loyalty_program, 
        'expiry_date': ['>=', expiry_date],
        'company': doc.company
    }

    filters.update(default_filters)

    return frappe.db.get_value('Loyalty Point Entry', filters, 'sum(loyalty_points)')

def set_previous_point(doc, remaining_points):
    expiry_date = doc.posting_date
    if not expiry_date:
        expiry_date = today()

    if not remaining_points:
        remaining_points = 0
        
    new_lp_entries = frappe.db.get_list('Loyalty Point Entry', 
        filters={
            'customer': doc.customer, 
            'sales_invoice': doc.name, 
            'loyalty_program': doc.loyalty_program, 
            'expiry_date': ['>=', expiry_date],
            'company': doc.company
        }, 
        fields=['name', 'loyalty_points'],
        order_by='creation'
    )
    
    for lp_entry in new_lp_entries:
        doc = frappe.get_doc('Loyalty Point Entry', lp_entry.get('name'))
        doc.db_set('previous_loyalty_points', remaining_points)
        remaining_points = remaining_points + lp_entry.get('loyalty_points')