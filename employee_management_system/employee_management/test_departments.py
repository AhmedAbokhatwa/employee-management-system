# test_departments.py
import frappe
import pytest
from employee_management_system.employee_management.api import get_departments
def test_create_company():
    name = "Test Company"
    if not frappe.db.exists("Company", name):
        frappe.get_doc({
            "doctype": "Company",
            "company_name": name,
            "abbr": "TC",
            "default_currency": "USD"
        }).insert() 

    assert frappe.db.exists("Company", name)
def test_get_departments_excludes_all_departments():
    # أنشئ شركة للاختبار
    if not frappe.db.exists("Company", "Test Company"):
        frappe.get_doc({
            "doctype": "Company",
            "company_name": "Test Company",
            "abbr": "TC",
            "default_currency": "USD"
        }).insert()

    # أنشئ Department عادي
    # frappe.get_doc({
    #     "doctype": "Department",
    #     "department_name": "Delivery",
    #     "company": "Test DepartmentCompany"
    # }).insert()

    # أنشئ Department اسمه All Departments
    # frappe.get_doc({
    #     "doctype": "Department",
    #     "department_name": "All Departments",
    #     "company": "Test Company"
    # }).insert()

    # نفّذ الدالة
    # result = get_departments(company=" Empolyee Management System")

    # تحقق إن All Departments مش راجعة
    # dept_names = [d["department_name"] for d in result]
    # assert "All Departments" not in dept_names
    # assert "Department" in dept_names
