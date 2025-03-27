import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.compose"]

# need to be run before the script can be used
def init():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        flow.redirect_uri = "http://localhost"
        auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
        print("Please go to this URL and authorize access:")
        print(auth_url)

        # After authorizing, paste the authorization code here
        code = input("Enter the authorization code: ")
        flow.fetch_token(code=code)
        creds = flow.credentials
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

def get_creds_closure():
  creds = None
  def get_creds():
    nonlocal creds
    if creds is not None:
      return creds
    if os.path.exists("token.json"):
      return Credentials.from_authorized_user_file("token.json", SCOPES)
    return None
  return get_creds

get_creds = get_creds_closure()

def test():
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=get_creds())
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"])

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


def send_verify_email(user_email, code: str):
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id
  """

  try:
    service = build("gmail", "v1", credentials=get_creds())
    message = EmailMessage()

    message.set_content("Please click the link to verify your email address: http://localhost/api/users/verify?code=" + code)

    message["To"] = user_email
    message["From"] = "teambytebreakers.com"
    message["Subject"] = "Please verify your email address"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message
