# Authentication

## User

### /auth/user/register

Name, email, password, OTP "seed"

### /auth/user/login

email, password, OTP "seed"

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