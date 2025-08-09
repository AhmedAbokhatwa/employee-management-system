import frappe
from frappe import _
from frappe.auth import LoginManager
# from frappe.sessions import Session

@frappe.whitelist(allow_guest=True)
def authenticated_user(name, password):
    try:
        # Start login manager
        login_manager = LoginManager()
        login_manager.authenticate(user=name, pwd=password)
        login_manager.post_login()

        user = frappe.get_doc("User", frappe.session.user)
        if not user.api_key:
            user.api_key = frappe.generate_hash(length=15)
        if not user.api_secret:
            user.api_secret = frappe.generate_hash(length=15)
        user.save(ignore_permissions=True)

        frappe.response['type'] = 'json'
        frappe.response['message'] = {
            "status": "success",
            "message": "Login successful",
            "redirect_to": "/employees",
            "api_key": user.api_key,
            "api_secret": user.api_secret,
            "sid": frappe.session.sid,
            "user_id":user.email,
            "user": user.name,
            "email": user.email,    
            "user_type": user.user_type,
            "role":user.role_profile_name,
        }

        # Ensure Set-Cookie is attached
        # frappe.local.cookie_manager.init_cookies()
        print("frappe.response['message']",frappe.response['message'])
        return frappe.response['message']

    except frappe.AuthenticationError:
        frappe.clear_messages()
        return {
            "status": "error",
            "message": _("Authentication failed. Please check your username and password.")
        }


@frappe.whitelist(allow_guest=True)
def get_csrf_token():
    csrf_token = frappe.sessions.get_csrf_token()
    if csrf_token:
        return {
            "status": "success",
            "message": csrf_token
        }
    else:
          return {
            "status": "error",
            "message":  _("CSRF Token failed.")
        }


@frappe.whitelist(allow_guest=False)
def update_account(name=None, email=None, username=None):
    """Update the logged-in user's account details"""
    user = frappe.session.user

    # Make sure we have a logged-in user
    if not user or user == "Guest":
        frappe.throw(_("Not logged in"), frappe.PermissionError)

    doc = frappe.get_doc("User", user)

    if name:
        doc.full_name = name
    if email:
        # Only allow if the email is unique
        if frappe.db.exists("User", email) and email != doc.email:
            frappe.throw(_("This email is already in use"))
        doc.email = email
    if username:
        doc.username = username

    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "success",
        "message": _("Account updated successfully"),
        "user": {
            "name": doc.full_name,
            "email": doc.email,
            "username": doc.username
        }
    }
    
@frappe.whitelist()
def get_all_users():
    """Return list of users with role info"""
    users = frappe.get_all("User", 
        fields=["name", "full_name", "email", "username"])
    
    result = []
    for u in users:
        roles = frappe.get_roles(u.name)
        result.append({
            **u,
            "role": roles[0] if roles else "No Role"
        })
    
    return result


@frappe.whitelist()
def get_user(name):
    if not name:
        frappe.throw("User name is required", frappe.MandatoryError)

    user = frappe.get_doc("User", name)
    data = {
        "name": user.name,
        "full_name": user.full_name,
        "email": user.email,
        "username": user.username,
        "role": get_user_role(user.name),
        "creation": user.creation
    }
    return {"message": data}


def get_user_role(user_name):

    roles = frappe.get_all("Has Role", filters={"parent": user_name}, fields=["role"])
    return roles[0].role if roles else 'No Role Found None'


@frappe.whitelist()
def delete_user(name):
    if not name:
        frappe.throw("User name is required", frappe.MandatoryError)

    if name == "Administrator":
        frappe.throw("Cannot delete the Administrator account.")

    frappe.delete_doc("User", name, ignore_permissions=False)

    return {"message": f"User {name} deleted successfully."}

# API Edit User
@frappe.whitelist()
def edit_user(name, full_name=None, email=None, username=None, role=None):
    if not name:
        frappe.throw("User name is required", frappe.MandatoryError)
    try:
        user = frappe.get_doc("User", name)
        
        if full_name is not None:
            user.full_name = full_name
        if email is not None:
            user.email = email
        if username is not None:
            user.username = username
        if role:   
            user.role_profile_name = role
        user.save(ignore_permissions=True)
        
      
        if role:
            existing_roles = frappe.get_all("Has Role", 
                                          filters={"parent": user.name, "parenttype": "User"},
                                          fields=["name"])
            
            for existing_role in existing_roles:
                frappe.delete_doc("Has Role", existing_role.name, ignore_permissions=True)
            
            role_doc = frappe.get_doc({
                "doctype": "Has Role",
                "parent": user.name,
                "parenttype": "User",
                "parentfield": "roles",
                "role": role
            })
            role_doc.insert(ignore_permissions=True)
        
        frappe.db.commit()
        return {
            "message": f"User Account {name} updated successfully",
            "status": "success"
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.throw(f"Error updating user: {str(e)}")


