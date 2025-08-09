# Employee Management System

## Overview
This is a full-stack Employee Management System designed to manage companies, departments, and employees with full CRUD functionality. The system includes role-based access control, validations, secure API, and a clean user interface.

## Features

### ✅ Completed Features
- User Interface (UI)
- Login Page
- Company Management
- Department Management
- Employee Management
- Summary Dashboard 
- User Account Management 
- Employee Report 

### 🔄 Pending Features
- Workflow
- Testing 
- Logging

## Installation

### Frappe App Installation

```bash
# Create new site
bench new-site employee_management.com
bench use employee_management.com

# Install ERPNext
bench install-app erpnext

# Get the app
bench get-app https://github.com/AhmedAbokhatwa/employee-management-system.git

# Install the app
bench --site employee_management.com install-app employee-management-system

# Migrate to add custom fields
bench --site employee_management.com migrate
```

### Frontend (Vue.js) Installation

1. **Clone the frontend application**
   ```bash
   git clone https://github.com/AhmedAbokhatwa/EMS-Vue.git
   cd employee-management-frontend
   ```

2. **Install dependencies**
   ```bash
   # Use Node.js version 22
   nvm install 22
   nvm use 22
   
   # Install required packages
   npm install axios vue-router@4 pinia
   npm i vue-toast-notification
   npm install
   ```

3. **Environment Configuration**
   Create a `.env` file and configure your backend host:
   ```env
   VITE_API_BASE=http://localhost:8002
   ```

4. **Run development server**
   ```bash
   npm run develop
   ```

### CORS Configuration

Configure CORS in `sites/common_site_config.json`:

```json
{
  "allow_cors": "http://localhost:5173"
}
```

> **Note:** Use specific domain instead of `"*"` to allow cookies. Use `localhost` consistently (not `127.0.0.1`).

## System Architecture

### Backend Models

#### 1. User Accounts
- Username, Email, Role

#### 2. Company
- Name, Number of Departments, Number of Employees

#### 3. Department
- Company, Name, Number of Employees

#### 4. Employee
- Company, Department, Status, Name, Email, Mobile, Address, Designation, Hired On, Days Employed

### Key Features

- ✅ Custom fields loaded from JSON fixtures
- ✅ Email and Mobile format validation
- ✅ Automatic counting of Departments/Employees in Company
- ✅ Automatic counting of Employees in Department
- ✅ Automatic calculation of Days Employed
- ✅ Department filtering by Company
- ✅ Cascading delete operations
  - Delete Company → Deletes related Departments and Employees
  - Delete Department → Shows warning for related Employees

## Security & Permissions

### Authentication
- **Endpoint:** `POST /api/method/employee_management_system.employee_management.middleware.authenticated_user`
- Returns: User data, Session ID (SID), API Keys

### Role-Based Access Control

#### Admin Role
- ✅ Dashboard access
- ✅ Full CRUD on Companies, Departments, Employees

#### Manager Role
- ✅ Dashboard access
- ✅ Full CRUD on Companies, Departments, Employees

#### Employee Role
- ✅ Dashboard access
- ✅ View-only access to Employees
- ❌ No access to Companies or Departments

### Permission Management
Configure permissions via ERPNext/Frappe Role Permissions Manager:

1. Open Role Permissions Manager
2. Select role (Admin/Manager/Employee)
3. Choose DocType (Company/Department/Employee)
4. Grant permissions: Read, Write, Create, Delete
5. Save changes

## API Documentation

### Authentication & Authorization

#### Get CSRF Token
```http
GET /api/method/employee_management_system.employee_management.middleware.get_csrf_token
```

#### User Login
```http
POST /api/method/employee_management_system.employee_management.middleware.authenticated_user
```

### Company APIs

#### Get All Companies
```http
GET /api/method/employee_management_system.employee_management.api.get_companies
```

#### Get Company by ID
```http
GET /api/resource/Company/{id}
```

#### Create Company
```http
POST /api/method/employee_management_system.employee_management.api.create_company

Content-Type: application/json

{
    "company_name": "H Groups",
    "abbr": "HG",
    "default_currency": "USD",
    "country": "Egypt"
}
```

#### Update Company
```http
PUT /api/resource/Company/{id}
```

#### Delete Company
```http
DELETE /api/method/employee_management_system.employee_management.api.delete_company

Content-Type: application/json

{
    "company": "My Company"
}
```

### Department APIs

#### Get Departments by Company
```http
GET /api/method/employee_management_system.employee_management.api.get_departments?company={companyName}
```

#### Get Department by ID
```http
GET /api/resource/Department/{id}
```

#### Create Department
```http
POST /api/method/employee_management_system.employee_management.api.create_department
```

#### Update Department
```http
PUT /api/resource/Department/{id}
```

#### Delete Department
```http
DELETE /api/method/employee_management_system.employee_management.api.delete_department

Content-Type: application/json

{
    "department_name": "Accounts"
}
```

#### Remove Department from Company
```http
POST /api/method/employee_management_system.employee_management.api.remove_department_from_company
```

### Employee APIs

#### Get All Employees
```http
GET /api/method/employee_management_system.employee_management.api.get_employees
```

#### Get Employee by ID
```http
GET /api/resource/Employee/{id}
```

#### Create Employee
```http
POST /api/method/employee_management_system.employee_management.api.create_employee
```
*Automatically updates employee counts in Company and Department*

#### Update Employee
```http
PUT /api/resource/Employee/{id}
```

#### Delete Employee
```http
DELETE /api/method/employee_management_system.employee_management.api.delete_employee

Content-Type: application/json

{
    "employee_name": "John Doe"
}
```
*Automatically updates employee counts in Company and Department*

### Additional APIs

#### Get All Designations
```http
GET /api/method/employee_management_system.employee_management.api.get_designation
```

#### Create User
```http
POST /api/method/employee_management_system.employee_management.api.create_user
```
*Creates user with role (Admin/Manager/Employee)*

#### Delete User Permission
```http
DELETE /api/method/employee_management_system.employee_management.utils.delete_user_permission

Content-Type: application/json

{
    "email": "user@example.com"
}
```

### User Account Management

#### Get All Users
```javascript
const users = await UserAccountAPI.getAllUsers();
```

#### Get User by Name
```javascript
const user = await UserAccountAPI.getUserByName("john@example.com");
```

#### Edit User
```javascript
await UserAccountAPI.edit_user({
    name: "john@example.com",
    full_name: "John Doe",
    role: "Manager"
});
```

#### Delete User
```javascript
await UserAccountAPI.deleteUser("john@example.com");
```

## Frontend Integration

### API Integration Features
- ✅ HTTP client integration (Axios/fetch)
- ✅ Full CRUD operations on UI
- ✅ Form binding to API methods
- ✅ Real-time data synchronization

### Security Implementation
- ✅ CSRF token management
- ✅ Session state maintenance
- ✅ Role-based UI permissions
- ✅ Automatic login redirect

### Error Handling
- ✅ Server-side error handling
- ✅ User-friendly error messages
- ✅ Authentication failure handling
- ✅ Permission denial handling
- ✅ Network error handling

### User Experience
- ✅ Loading state management
- ✅ Success/failure feedback
- ✅ UI state reversion on errors
- ✅ Toast notifications
- ✅ Progress indicators

## Technologies Used

### Backend
- **Framework:** Frappe/ERPNext
- **Language:** Python
- **Database:** MariaDB/MySQL

### Frontend
- **Framework:** Vue.js 3
- **Router:** Vue Router 4
- **State Management:** Pinia
- **HTTP Client:** Axios
- **Notifications:** vue-toast-notification

## Contributing

This app uses `pre-commit` for code formatting and linting:

```bash
cd apps/employee_management_system
pre-commit install
```

Pre-commit tools:
- ruff
- eslint
- prettier
- pyupgrade

## License

MIT

---

## Quick Start Commands

```bash
# Backend setup
bench new-site employee_management.com
bench use employee_management.com
bench install-app erpnext
bench get-app https://github.com/AhmedAbokhatwa/employee-management-system.git
bench --site employee_management.com install-app employee-management-system
bench --site employee_management.com migrate

# Frontend setup
cd employee-management-frontend
nvm use 22
npm install
npm run develop
```

## Support

For issues and questions, please create an issue in the GitHub repository.