import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import gspread
from gspread.client import Client


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]


def login(credential_file_path):
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            tok_info = pickle.load(token)
            if all(scp in tok_info["scopes"] for scp in SCOPES):
                creds = tok_info["creds"]
    if not creds or not creds.valid:
        if os.path.exists("token.pickle"):
            os.remove("token.pickle")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credential_file_path, SCOPES
            )
            creds = flow.run_console()
        with open("token.pickle", "wb") as token:
            pickle.dump(
                {"scopes": SCOPES, "creds": creds}, token,
            )

    return Client(creds)


def service_login(service_account_file):
    return gspread.service_account(filename=service_account_file)


def entries(
    client,
    url,
    sheet="Sheet1",
    range_=None,
    indirect=None,
):
    book = client.open_by_url(url)
    sheet_ = book.worksheet(sheet)

    if range_:
        data = sheet_.get(range_)
        return [dict(zip(data[0], entry)) for entry in data[1:]]
    elif indirect:
        sheet_range = sheet_.get(indirect)[0][0]
        return entries(client, url, sheet, rng=sheet_range)
    else:
        return sheet_.get_all_records()


def gsheet(id_):
    return f"https://docs.google.com/spreadsheets/d/{id_}/edit#gid=0"


def google_sheet_reader(url, tab):

    def _google_sheet_reader():
        # FIXME: Ugh, configuring the sheets client is painful.
        # Just setting it as a constant from the file for now
        client = service_login("service-account.json")
        return entries(client, url, sheet=tab)

    return _google_sheet_reader
