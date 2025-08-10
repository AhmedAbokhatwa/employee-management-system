import frappe

def ensure_role(role_name):
    """Create role if not exists"""
    if not frappe.db.exists("Role", role_name):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": role_name
        }).insert(ignore_permissions=True)
        print(f"Created role: {role_name}")
    else:
        print(f"ℹ Role already exists: {role_name}")

def ensure_user(email, full_name, roles):
    """Create user if not exists and assign roles"""
    if not frappe.db.exists("User", email):
        frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": full_name,
            "enabled": 1
        }).insert(ignore_permissions=True)
        print(f" Created user: {full_name} ({email})")
    else:
        print(f"ℹ User already exists: {full_name} ({email})")

    for role in roles:
        if not frappe.db.exists("Has Role", {"parent": email, "role": role}):
            frappe.get_doc({
                "doctype": "Has Role",
                "parent": email,
                "parentfield": "roles",
                "parenttype": "User",
                "role": role
            }).insert(ignore_permissions=True)
            print(f" Added role '{role}' to {email}")
        else:
            print(f"  ℹ {email} already has role '{role}'")

    frappe.db.commit()

def run():
    roles_needed = ["admin", "manager", "employee"]
    for r in roles_needed:
        ensure_role(r)

    ensure_user("ahmedadmin@example.com", "Admin User", ["admin"])
    ensure_user("alimanager@example.com", "Manager User", ["manager"])
    ensure_user("saidemployee@example.com", "Employee User", ["employee"])
