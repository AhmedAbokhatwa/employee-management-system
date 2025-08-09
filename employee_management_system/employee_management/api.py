import frappe
from frappe.utils import today, date_diff
# ApI GET One Or List Of Department   
@frappe.whitelist(allow_guest =True)
def get_departments(company=None):
    filters = {"company":company} if company else {}
    departments = frappe.get_all("Department", filters=filters, fields=["name", "department_name", "company", "custom_number_of_employees"])
    return  [dept for dept in departments if dept["department_name"] != "All Departments"]


# API create department
#  Also increase No. Departments in company 
@frappe.whitelist()
def create_department():
    data = frappe.request.get_json()
    department_name = data.get("department_name")
    company = data.get("company")
    try:     
        if not department_name or not company:
            frappe.throw("Department Name and Company are required")

        doc = frappe.get_doc({
            "doctype": "Department",
            "department_name": department_name,
            "company": company
        })
        doc.insert(ignore_permissions=True)
        try:
            if company:
                company_doc = frappe.get_doc("Company", company)
                if hasattr(company_doc, "custom_number_of_departments"):
                    company_doc.custom_number_of_departments = (company_doc.custom_number_of_departments or 0) + 1
                    company_doc.save(ignore_permissions=True)
        except Exception as count_error:
            frappe.log_error(
                f"Failed to  count for Department {company}: {str(count_error)}", 
                "Department Count Update Error"
            )      
            return {
                "success":False,
                "message": f"Department Count Update Error"
            }     
        frappe.db.commit()
        return {
            "message": f"Department '{department_name}' created successfully.", "success": True
        }
    except frappe.DuplicateEntryError as e:
        frappe.log_error(frappe.get_traceback(), "Create Department Duplicate Error")
        frappe.response["http_status_code"] = 409
        return {
            "error": f"Department '{department_name}' already exists. Please use a different name.",
            "success": False,
            "error_type": "duplicate"
        }   
    except Exception as inner_error:
        # Rollback transaction on any error
        frappe.db.rollback()
        raise inner_error
 
# API Delete Department
@frappe.whitelist()
def delete_department(department_name):
    """Update Company counts when  Department is deleted
         Delelte All Employee For this Department
    """
    department = frappe.get_doc("Department",department_name)
    company = department.company
 
    employees = frappe.get_all("Employee", filters={"department": department_name}, pluck="name")
    for emp in employees:
        frappe.delete_doc("Employee", emp, force=1)


    if company:
        dept_count = frappe.db.count("Department", {"company": company})
        frappe.db.set_value("Company", company, "custom_number_of_departments", dept_count)


        emp_count = frappe.db.count("Employee", {"company": company})
        frappe.db.set_value("Company", company, "custom_number_of_employees", emp_count)
    frappe.delete_doc("Department", department_name, force=1)
    frappe.db.commit()
    return {
        "status": "success",
        "message": f"Department {department_name} deleted successfully"}

# API Remove Department Linked from Company
@frappe.whitelist(allow_guest=True)
def remove_department_from_company(department): 
    department_name = department
    if not department_name:
        frappe.throw("Department name is required")
    department_doc = frappe.get_doc("Department", department_name)
    company_name = department_doc.company
    
    company_doc = frappe.get_doc("Company", company_name)
    original_len = len(company_doc.custom_department_list)
    
    company_doc.custom_department_list = [
        dep for dep in company_doc.custom_department_list
        if dep.department != department_name
    ]

    if len(company_doc.custom_department_list) < original_len:
        company_doc.save()
        frappe.db.commit()
        return{
            "status":1,
            "message": f'{department_name} removed from company {company_name}'
            }
    else:
        return{
            "status":0,
            "message": f'{department_name} not found in company {company_name}'
        }
        
# API Create Employee 
@frappe.whitelist(allow_guest=True)
def create_employee(**data):
    
    employee = frappe.get_doc({
        "doctype": "Employee",
        **data
    }).insert(ignore_permissions=True)
    
   
    company_name = data.get("company")
    if company_name:
        company_doc = frappe.get_doc("Company", company_name)
        
        if employee.date_of_joining:
            employee.custom_days_employed = date_diff(today(), employee.date_of_joining)

       
        if hasattr(company_doc, "custom_number_of_employees"):
            company_doc.custom_number_of_employees = (company_doc.custom_number_of_employees or 0) + 1
            company_doc.save(ignore_permissions=True)
            
    department_name = data.get("department")
    if department_name:
        dep_doc = frappe.get_doc("Department", department_name)
        if hasattr(dep_doc, "custom_number_of_employees"):
            dep_doc.custom_number_of_employees = (dep_doc.custom_number_of_employees
                                                  or 0 ) +1
            dep_doc.save(ignore_permissions=True)
    frappe.db.commit()
    return employee.name

# API GET Employee 
@frappe.whitelist(allow_guest =True)
def get_employees(company=None, department=None):
    filters = {}
    if company: filters["company"] = company
    if department: filters["department"] = department
            
    return frappe.get_all("Employee", 
        filters=filters,
        fields=["name", "employee_name", "user_id",
                "cell_number", "custom_mobile","custom_email",  
                "designation", "custom_employee_status", "date_of_joining", "custom_days_employed", "company", "department"]
    )
import frappe


# API Delete Employee 
@frappe.whitelist()
def delete_employee(employee_name):
    """
    Delete an employee and update employee counts in Company and Department doctypes.
    """

    employee = frappe.get_doc("Employee", employee_name)
    company_name = employee.company
    department_name = employee.department

    frappe.delete_doc("Employee", employee_name, force=1)

    # Update employee count in Doctype Company
    if company_name:
        company_count = frappe.db.count("Employee", {"company": company_name})
        frappe.db.set_value("Company", company_name, "custom_number_of_employees", company_count)

    # Update employee count in Doctype Department
    if department_name:
        dept_count = frappe.db.count("Employee", {"department": department_name})
        frappe.db.set_value("Department", department_name, "custom_number_of_employees", dept_count)
    
    frappe.db.commit()

    return {
        "status": "success",
        "message": f"Employee {employee_name} deleted successfully.",
        "company_count": company_count if company_name else None,
        "department_count": dept_count if department_name else None
    }
    
    
@frappe.whitelist(allow_guest =True)
def get_designation():
    return frappe.get_all("Designation","name")
        
        
@frappe.whitelist(allow_guest =True)
def create_user(**kwargs):
    email = kwargs.get("email")
    first_name = kwargs.get("first_name")
    role = kwargs.get("role")
    if not email or not first_name or not role:
        return {
            "success": False,
            "message": "Missing required fields: email, first_name, or role"
        }

    if frappe.db.exists('User',{"email":email}):
        return {
            "success": False,
            "message": f"User with email {email} already exists."
        }
    else:
        try:
            user = frappe.get_doc({"doctype":"User","email":email,"first_name":first_name,"role_profile_name": role})
            user.insert(ignore_permissions=True)
            frappe.db.commit()
            return {
                "success": True,
                "message": f"User {email} created successfully.",
                "user": user.name
            }
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Create User Failed")
            return {
                "success": False,
                "message": f"Error Create User Failed {str(e)}",  
            }
                      
        
#API create company
@frappe.whitelist()
def create_company():
    try:
        data = frappe.request.get_json()
        
        if not data:
            frappe.throw("No data provided")
        
        company_name = data.get("company_name", "").strip()
        abbr = data.get("abbr", "").strip().upper()
        default_currency = data.get("default_currency")
        country = data.get("country")
        
        if not all([company_name, abbr, default_currency, country]):
            frappe.throw("All fields are required")
        
        # Check duplicates
        if frappe.db.exists("Company", {"company_name": company_name}):
            frappe.throw(f"Company '{company_name}' already exists")
            
        if frappe.db.exists("Company", {"abbr": abbr}):
            frappe.throw(f"Company with abbreviation '{abbr}' already exists")
        
        # Create minimal company record
        frappe.db.sql("""
            INSERT INTO `tabCompany` 
            (name, company_name, abbr, default_currency, country, 
             creation, modified, owner, modified_by, docstatus)
            VALUES 
            (%s, %s, %s, %s, %s, NOW(), NOW(), %s, %s, 0)
        """, (company_name, company_name, abbr, default_currency, country, 
              frappe.session.user, frappe.session.user))
        
        frappe.db.commit()
        
        return {
            "message": f"Company '{company_name}' created successfully",
            "company_name": company_name,
            "success": True
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Simple Company Error")
        frappe.response["http_status_code"] = 500
        return {"error": str(e), "success": False}

#API delete company        
@frappe.whitelist()  
def delete_company(company):
    try:
        frappe.db.delete("Company", {"name": company})
        frappe.db.delete("Department", {"company": company})
        frappe.db.delete("Employee", {"company": company})
        frappe.db.commit()  
        return {
            "message": f"Company '{company}' Deleted  successfully.",
            "company_name": company ,
            "success": True
        }
    except Exception as e:
        return {
            "message": f" Failed to Delete Company '{company}'.",
            "company_name": company,
            "success": False
        }   


#API GET Companies
@frappe.whitelist(allow_guest =True)
def get_companies():
    companies = frappe.get_all("Company", fields=["name", "company_name","custom_number_of_employees","custom_number_of_departments"])
    return companies
        
           
            
               
          
    