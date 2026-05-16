# Module: Customer Login

**Application:** ParaBank
**File:** `login.md`

## 1. Business Objective

Allow registered customers to securely access their accounts and perform banking operations, while preventing unauthorized access.

## 2. Acceptance Criteria (Business Rules)

### 2.1. Successful Login (Happy Path)

* **Given** a registered user exists in the database.
* **When** the user enters a valid `Username` and `Password` in the Customer Login panel.
* **And** clicks the "Log In" button.
* **Then** the system successfully authenticates the user.
* **And** redirects the user to the "Accounts Overview" page.
* **And** displays a welcome message containing the user's first and last name.
* **And** the "Log Out" link becomes visible in the left-hand menu.

### 2.2. Unsuccessful Login - Invalid Credentials

* **Given** a user is on the homepage.
* **When** the user enters an invalid `Username` OR an invalid `Password`.
* **And** clicks the "Log In" button.
* **Then** the system denies access.
* **And** displays the error message: "The username and password could not be verified."
* **And** the user is redirected to the `/parabank/login.htm` error page.

### 2.3. Unsuccessful Login - Empty Fields

* **Given** a user is on the homepage.
* **When** the user leaves the `Username` OR `Password` field empty.
* **And** clicks the "Log In" button.
* **Then** the system denies access.
* **And** displays the error message: "Please enter a username and password."
* **And** the user is redirected to the `/parabank/login.htm` error page.

### 2.4. Session Termination (Log Out)

* **Given** an authenticated user is currently logged in.
* **When** the user clicks the "Log Out" link.
* **Then** the system securely terminates the session.
* **And** redirects the user back to the public homepage (`/parabank/index.htm`).