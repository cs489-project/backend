# Authentication

## User

### /api/users/register

Name, email, password, OTP "seed"

### /api/users/login-password

email, password, OTP "seed"

### /api/users/login-mfa
- code: string
- Updates the session object with the user's MFA status
- If it's the first time the user logs in with MFA, it will change the user's status to `mfa_verified`

### /api/users/register-mfa
- generates a new MFA secret for the user, update the user's status to `mfa_pending`
- returns the uri for the QR code

## Organization

### /auth/org/register

### /auth/org/login

# Admin Controls

## User management

### delete_user

### delete_org

## Job request management

### delete_job_request

### approve_job_request

### reject_job_request

# Pentest Request

## Organization

`job_request` is organization pentest request

### submit_job_request

### edit_job_request

### delete_job_request

### comment_on_report

### accept_report

### reject_report

### get_reports

job_request opt

### get_requests

3 way flag

- only rejected
- only approved
- both

## User

### get_orgs

### get_requests

org_id (opt)

sort feature for most recent

### create_report

### comment_on_report

### get_reports
