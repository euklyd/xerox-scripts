from typing import List, Dict, Any, Optional

import gspread
from gspread import Worksheet
from oauth2client.service_account import ServiceAccountCredentials


class SheetConnection:
    def __init__(self, secret: str, scope: List[str]):
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(secret, scope)

    def get_sheet(self, sheet_name: str) -> gspread.Spreadsheet:
        client = gspread.authorize(self.creds)
        return client.open(sheet_name)

    def get_page(self, sheet_name: str, page_name=None) -> gspread.Worksheet:
        if page_name is None:
            return self.get_sheet(sheet_name).sheet1
        else:
            return self.get_sheet(sheet_name).worksheet(page_name)

    def client(self):
        return gspread.authorize(self.creds)


def get_headings(ws: Worksheet) -> List[str]:
    return ws.row_values(1)


def get_column_values(ws: Worksheet, heading: str) -> Optional[List[Any]]:
    if heading not in get_headings(ws):
        return None
    return [record[heading] for record in ws.get_all_records()]


def get_headings_to_columns(ws: Worksheet) -> Dict[str, int]:
    return {k: i + 1 for i, k in enumerate(ws.row_values(1))}


def find_row(records: List[Dict[str, Any]], lookup_value, search_heading) -> int:
    for i, record in enumerate(records):
        if record[search_heading] == lookup_value:
            return i + 2


def find_record(records: List[Dict[str, Any]], lookup_value, search_heading) -> dict:
    for record in records:
        if record[search_heading] == lookup_value:
            return record


# def vlookup_column(ws: List[Dict[str, Any]], lookup_value, search_col, return_col):
#     pass


def vlookup_heading(records: List[Dict[str, Any]], lookup_value, search_heading, return_heading):
    for record in records:
        if record[search_heading] == lookup_value:
            return record[return_heading]
