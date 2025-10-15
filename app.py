# app.py
import time, hashlib
import streamlit as st
import pandas as pd
from gsheets_io import read_sheet_to_df, get_or_create_worksheet, upsert_read_status

st.set_page_config(page_title="Medium Digest-Web", layout="wide")

# ======== 必填 ========
SHEET_ID = "1ams3xdaxMB_iAEpbAK0CT3yZwv9ME-5jZINiiXN0p7Q"
DATA_SHEET_NAME = "Articles"
READ_SHEET_NAME = "ReadStatus"
REQUIRED_COLS = ['Date', 'Author', 'Title', 'Subtitle', 'URL', 'Category (20-class)']

# ======== 即時寫入的短延遲（防連點） ========
DEBOUNCE_MS = 300  # 建議 200~500ms

def stable_key(prefix: str, s: str) -> str:
    return f"{prefix}_{hashlib.md5(s.encode('utf-8'), usedforsecurity=False).hexdigest()}"

def load_articles() -> pd.DataFrame | None:
    df = read_sheet_to_df(SHEET_ID, DATA_SHEET_NAME)
    if df.empty:
        get_or_create_worksheet(SHEET_ID, DATA_SHEET_NAME, headers=REQUIRED_COLS)
        st.warning(f"`{DATA_SHEET_NAME}` 尚無資料。請先在試算表建立欄位：{', '.join(REQUIRED_COLS)}")
        return None

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df["ItemKey"] = df["URL"].astype(str)

    rs = read_sheet_to_df(SHEET_ID, READ_SHEET_NAME)
    if rs.empty:
        df["Read"] = False
    else:
        rs = rs.rename(columns=str)
        if "Read" in rs.columns:
            rs["Read"] = rs["Read"].astype(str).str.lower().isin(["true", "1", "yes"])
        rs = rs[["ItemKey", "Read"]].drop_duplicates(subset=["ItemKey"], keep="last")
        df = df.merge(rs, how="left", on="ItemKey")
        df["Read"] = df["Read"].fillna(False).astype(bool)

    return df

def on_toggle(chk_key: str, item_key: str):
    """checkbox 切換時呼叫：做防抖 + 寫回 + 輕量 rerun。"""
    time.sleep(DEBOUNCE_MS / 1000.0)
    new_state = bool(st.session_state.get(chk_key, False))
    upsert_read_status(SHEET_ID, item_key, new_state)
    #st.rerun()

def display_paginated_articles(df):
    if df.empty:
        st.info("無文章。")
        return

    if "page" not in st.session_state:
        st.session_state.page = 0

    items_per_page = 8
    total_pages = (len(df) + items_per_page - 1) // items_per_page
    st.session_state.page = min(st.session_state.page, max(total_pages - 1, 0))

    start = st.session_state.page * items_per_page
    end = start + items_per_page
    page_df = df.iloc[start:end]

    st.markdown("""
    <style>
    .stMarkdown div { margin-top: -10px; margin-bottom: -10px; }
    .read-dim { opacity: 0.45; }
    </style>
    """, unsafe_allow_html=True)

    for _, row in page_df.iterrows():
        wrapper_class = "read-dim" if row.get("Read", False) else ""
        title_html = f"<font size=5>♦ <b>{row['Title']}</b></font>"
        subtitle_html = f"{row['Subtitle']}" if pd.notna(row['Subtitle']) else ""
        date_str = row['Date'].strftime('%Y-%m-%d') if pd.notna(row['Date']) else 'N/A'
        link_html = (
            f"{row['Author']},  {date_str}, "
            f"<a href='{row['URL']}' target='_blank' style='margin-right:15px'>🔗全文連結</a>"
            f"<a href='https://freedium.cfd/{row['URL']}' target='_blank'>🔗破解連結</a>"
        )

        st.markdown(f"<div class='{wrapper_class}'>{title_html}</div>", unsafe_allow_html=True)
        if subtitle_html:
            st.markdown(f"<div class='{wrapper_class}'>{subtitle_html}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='{wrapper_class}'>{link_html}</div>", unsafe_allow_html=True)

        # 單一 checkbox 控制「已報告」
        col_a, _ = st.columns([3, 3])
        chk_key = stable_key("readchk", row["ItemKey"])
        col_a.checkbox(
            "已報告",
            value=bool(row.get("Read", False)),
            key=chk_key,
            on_change=on_toggle,
            args=(chk_key, row["ItemKey"]),
            help="切換後自動儲存（含 0.3 秒防連點）"
        )

        st.markdown("---")

    # 分頁
    col1, col2, col3 = st.columns([4, 1, 1])
    with col2:
        if st.button("上一頁") and st.session_state.page > 0:
            st.session_state.page -= 1
            st.rerun()
    with col3:
        if st.button("下一頁") and st.session_state.page < total_pages - 1:
            st.session_state.page += 1
            st.rerun()
    st.write(f"頁碼: {st.session_state.page + 1} / {total_pages}")

# ======== 主內容 ========
st.title("Medium Digest-Web（Google Sheets 版）")

df = load_articles()
if df is None:
    st.stop()

# ===== 分類側欄與篩選 =====
ai_categories = [
    "Agentic AI & AI Agents",
    "Retrieval-Augmented Generation (RAG)",
    "Multimodal AI (Vision/Audio/Video + Language)",
    "Prompt Engineering & In-Context Learning",
    "Fine-tuning & Embeddings",
    "Large Language Models (LLM)",
    "Natural Language Processing (non-LLM)",
    "Computer Vision (CV)",
    "Speech & Audio AI",
    "Deep Learning (non-LLM)",
    "Machine Learning (Classical)",
    "AI Algorithm",
    "AI Evaluation & Metrics",
    "AI Infrastructure, MLOps & Frameworks",
    "AI Applications (Business/Dev/Productivity)",
    "AI Policy, Governance & Safety",
]
non_ai_display_categories = [
    "Data Science & Statistics",
    "Software Engineering & Programming",
    "Technology/Science",
    "Finance/Economics/Business",
    "Society/Culture/Other",
]

st.sidebar.subheader("狀態")
total_read = int(df["Read"].sum())
total_unread = int((~df["Read"]).sum())
status_options = [
    f"全部（{len(df)}）",
    f"僅未報告（{total_unread}）",
    f"僅已報告（{total_read}）",
]
status_choice = st.sidebar.radio("依狀態篩選", status_options, index=0, key="status_filter")
st.sidebar.markdown("---")

st.sidebar.header("文章分類")
selected_labels: list[str] = []
unique_cats = set(df["Category (20-class)"].unique())

st.sidebar.subheader("AI（15 類）")
ai_select_all = st.sidebar.checkbox("全選 AI", key="ai__all")
prev_ai_all = st.session_state.get("ai__all_prev", False)
if ai_select_all != prev_ai_all:
    for label in ai_categories:
        if label in unique_cats:
            st.session_state[f"ai_{label}"] = ai_select_all
    st.session_state["ai__all_prev"] = ai_select_all

for label in ai_categories:
    if label in unique_cats:
        cnt = (df["Category (20-class)"] == label).sum()
        if st.sidebar.checkbox(
            f"{label}（{cnt} 篇文章）",
            key=f"ai_{label}",
            value=st.session_state.get(f"ai_{label}", False),
        ):
            selected_labels.append(label)

st.sidebar.markdown("---")

st.sidebar.subheader("非 AI（5 類）")
non_ai_select_all = st.sidebar.checkbox("全選 非AI", key="nonai__all")
prev_nonai_all = st.session_state.get("nonai__all_prev", False)
if non_ai_select_all != prev_nonai_all:
    for display_label in non_ai_display_categories:
        label = f"Non-AI {display_label}"
        if label in unique_cats:
            st.session_state[f"nonai_{display_label}"] = non_ai_select_all
    st.session_state["nonai__all_prev"] = non_ai_select_all

for display_label in non_ai_display_categories:
    label = f"Non-AI {display_label}"
    if label in unique_cats:
        cnt = (df["Category (20-class)"] == label).sum()
        if st.sidebar.checkbox(
            f"{display_label}（{cnt} 篇文章）",
            key=f"nonai_{display_label}",
            value=st.session_state.get(f"nonai_{display_label}", False),
        ):
            selected_labels.append(label)

st.sidebar.markdown("---")

# 搜尋 & 條件變更處理
search_term = st.text_input("在 Title 或 Subtitle 中搜尋", key="search_main")

selected_labels = sorted(set(selected_labels))
if "page" not in st.session_state:
    st.session_state.page = 0

if st.session_state.get("last_search") != search_term:
    st.session_state.page = 0
    st.session_state.last_search = search_term

if st.session_state.get("last_selected") != tuple(selected_labels):
    st.session_state.page = 0
    st.session_state.last_selected = tuple(selected_labels)

if st.session_state.get("last_status") != status_choice:
    st.session_state.page = 0
    st.session_state.last_status = status_choice

# 篩選
if selected_labels:
    filtered_df = df[df["Category (20-class)"].isin(selected_labels)]
else:
    filtered_df = df

if "僅未報告" in status_choice:
    filtered_df = filtered_df[~filtered_df["Read"]]
elif "僅已報告" in status_choice:
    filtered_df = filtered_df[filtered_df["Read"]]

filtered_df = filtered_df.sort_values("Date", ascending=False)

# 顯示列表
if search_term:
    mask = (
        filtered_df["Title"].astype(str).str.contains(search_term, case=False, na=False)
        | filtered_df["Subtitle"].astype(str).str.contains(search_term, case=False, na=False)
    )
    search_df = filtered_df[mask]
    st.subheader(f"搜尋結果（共 {len(search_df)} 筆）")
    if not search_df.empty:
        display_paginated_articles(search_df)
    else:
        st.info("無符合搜尋結果。")
else:
    display_paginated_articles(filtered_df)

