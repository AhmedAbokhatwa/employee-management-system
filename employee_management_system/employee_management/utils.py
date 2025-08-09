
import frappe
from frappe.utils import today, date_diff


def calculate_employment_days(doc, method):
    if doc.date_of_joining:
        doc.custom_days_employed = date_diff(today(), doc.date_of_joining)
        frappe.db.commit()     
        
@frappe.whitelist()        
def delete_user_permission(email):
    perms = frappe.get_all("User Permission",{"user":email})            
    
    if perms:
        for perm in perms:
            frappe.db.delete("User Permission",{"name":perm.name})
        frappe.db.commit()  
        return {"message": f"Deleted {len(perms)} permissions for {email}"}  
    else:
        return{
            "message":"No Permissions Found for{0}".format(email)
        }
        

            