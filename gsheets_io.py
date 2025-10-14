# gsheets_io.py
import os
import time
from typing import Dict, List
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from gspread.exceptions import APIError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# =========================
# 授權 & Spreadsheet 物件（資源級快取）
# =========================
@st.cache_resource
def get_client():
    """直接在函式內讀取 st.secrets，避免 UnhashableParamError。"""
    svc = st.secrets.get("gcp_service_account", None)
    if svc is not None:
        svc = dict(svc)
        pk = svc.get("private_key", "")
        if "\\n" in pk and "BEGIN PRIVATE KEY" in pk:
            svc["private_key"] = pk.replace("\\n", "\n")
        creds = Credentials.from_service_account_info(svc, scopes=SCOPES)
        return gspread.authorize(creds)

    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path or not os.path.exists(cred_path):
        raise RuntimeError("缺少憑證：請在 .streamlit/secrets.toml 放 gcp_service_account，或設 GOOGLE_APPLICATION_CREDENTIALS")
    creds = Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    return gspread.authorize(creds)

@st.cache_resource
def open_spreadsheet(sheet_id: str):
    """快取 Spreadsheet 物件。"""
    gc = get_client()
    return gc.open_by_key(sheet_id)

# =========================
# 一次抓 worksheets metadata（避免每次 worksheet(name) 都打 API）
# =========================
@st.cache_resource
def list_worksheets_map(sheet_id: str) -> Dict[str, gspread.Worksheet]:
    sh = open_spreadsheet(sheet_id)
    wss = sh.worksheets()  # 打一次 metadata API
    return {ws.title: ws for ws in wss}

def get_or_create_worksheet(sheet_id: str, name: str, headers: List[str] | None = None) -> gspread.Worksheet:
    ws_map = list_worksheets_map(sheet_id)
    if name in ws_map:
        return ws_map[name]
    sh = open_spreadsheet(sheet_id)
    ws = sh.add_worksheet(title=name, rows=2000, cols=26)
    if headers:
        safe_update(ws, 'A1', [headers])
    return ws

# =========================
# API 呼叫：指數退避重試
# =========================
def _need_retry(e: Exception) -> bool:
    if isinstance(e, APIError):
        try:
            code = e.response.status_code
        except Exception:
            code = None
        msg = str(e)
        return (code in (429, 500, 503)) or ("Quota exceeded" in msg) or ("rateLimitExceeded" in msg)
    return False

def with_retry(func, *args, **kwargs):
    """最多 5 次，1s,2s,4s,8s,16s。"""
    delay = 1.0
    last = None
    for _ in range(5):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last = e
            if _need_retry(e):
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise last

def safe_update(ws: gspread.Worksheet, range_name: str, values: List[List[str]]):
    return with_retry(ws.update, range_name, values)

def safe_clear(ws: gspread.Worksheet):
    return with_retry(ws.clear)

def safe_get_all_values(ws: gspread.Worksheet) -> List[List[str]]:
    return with_retry(ws.get_all_values)

def safe_append_row(ws: gspread.Worksheet, row: List[str]):
    return with_retry(ws.append_row, row)

def safe_update_cell(ws: gspread.Worksheet, row: int, col: int, value):
    return with_retry(ws.update_cell, row, col, value)

# =========================
# 讀寫：資料級快取（避免重複打 API）
# =========================
@st.cache_data(ttl=60)
def read_sheet_to_df(sheet_id: str, sheet_name: str) -> pd.DataFrame:
    """同一分鐘內重用資料。"""
    ws = get_or_create_worksheet(sheet_id, sheet_name)
    vals = safe_get_all_values(ws)
    if not vals:
        return pd.DataFrame()
    header = vals[0]
    rows = vals[1:]
    if not rows:
        return pd.DataFrame(columns=header)
    return pd.DataFrame(rows, columns=header)

def write_df_to_sheet(sheet_id: str, sheet_name: str, df: pd.DataFrame):
    ws = get_or_create_worksheet(sheet_id, sheet_name, headers=list(df.columns))
    safe_clear(ws)
    if df.empty:
        safe_update(ws, 'A1', [list(df.columns)])
    else:
        values = [list(df.columns)] + df.astype(str).values.tolist()
        safe_update(ws, 'A1', values)

# =========================
# ReadStatus：單列即時 upsert
# =========================
def upsert_read_status(sheet_id: str, item_key: str, read_state: bool):
    """
    單列 upsert：一次 get_all_values 建索引，找到就 update_cell，找不到就 append_row。
    完成後清掉資料快取，讓畫面立即反映。
    """
    ws = get_or_create_worksheet(sheet_id, "ReadStatus", headers=["ItemKey", "Read"])
    vals = safe_get_all_values(ws)
    rows = vals[1:] if len(vals) > 1 else []
    index = {r[0]: i for i, r in enumerate(rows, start=2)}  # ItemKey -> 實際 row（含表頭）

    if item_key in index:
        row_no = index[item_key]
        safe_update_cell(ws, row_no, 2, "true" if read_state else "false")
    else:
        safe_append_row(ws, [item_key, "true" if read_state else "false"])

    st.cache_data.clear()  # 資料變更後清 cache
