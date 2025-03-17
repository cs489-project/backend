# Authentication

## User

### POST /api/users/register

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

### POST /api/users/register-mfa

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

### POST /api/users/login-password

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

### POST /api/users/login-mfa

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

### GET /api/users/me

Request

```ts
cookie: session_id
```

Response

```ts
{
  "name": string 
  "email": string
  "role": "admin" | "researcher" | "organization"
  "auth_stage": "password" | "mfa_pending" | "mfa_verified" | "email_verified"
}
```

### POST /api/users/logout

Request

```ts
cookie: session_id
```

Response

```ts
{"message": "Logged out"}
```

## Admin

### POST /api/admin/delete-user

Request

```ts
cookie: session_id

Request {
	"user_id": int
}
```

Response

```ts
400 - no email provided
404 - user doesn't exist
200 - {"message": "User deleted"}
```

### GET /api/admin/researchers

- Returns a list of all researchers

Request

```ts
cookie: session_id
```

Response

```ts
{
	"name": string
	"email": string
	"id": int
}[]
```

### GET /api/admin/organizations

- Returns a list of all organizations

Request

```ts
cookie: session_id
```

Response

```ts
{
	"name": string
	"email": string
	"id": int
}[]
```

### GET /api/admin/user

- Returns details about a specific user / organization

Request

```ts
cookie: session_id
{
  "user_id": int
}
```

Response

```ts
{
	"name": string
	"email": string
	"id": int
  "auth_stage": "password" | "mfa_pending" | "mfa_verified" | "email_verified"
}[]
```

## Organization

### /auth/org/register

### /auth/org/login

# Admin Controls

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
