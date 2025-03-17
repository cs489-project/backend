# Authentication

## User

### /api/users/register

Request body

```ts
{
	"name": string
	"email": string
	"password": string
}
```

Response

```ts
set-cookie: session_id, httponly=True, secure=True
response 200 {
	"message": "Registered"
}

response 400 {
	"error": "Error registering"
}
```

### /api/users/register-mfa

- generates a new MFA secret for the user, update the user's status to `mfa_pending`
- returns the uri for the QR code

Request

```ts
cookie: session_id
```

Response

```ts
response 200 {
  "uri": string
}
```

### /api/users/login-password

Request

```ts
{
	"email": string
	"password": string
}
```

Response

```ts
set-cookie: session_id, httponly=True, secure=True
response 200 {
	"message": "Logged in"
}

response 401 {
	"error": "Error logging in"
}
```

### /api/users/login-mfa

- Updates the session object to be post MFA, long lived session
- If it's the first time the user logs in with MFA, it will change the user's status to `mfa_verified`

Request

```ts
cookie: session_id
request body {
	"code": number
}
```

Response

```ts
set-cookie: session_id, httponly=True, secure=True
response 200 {
	"message": "Logged in"
}

response 401 {
	"error": "Error logging in"
}
```



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
