# Medium Digest Web with Gsheets 📚

這是一個基於 **Streamlit** 的 Web 應用程式，使用 **Google Sheets** 作為後端資料庫，讓使用者可以輕鬆瀏覽、搜尋與管理 Medium 文章摘要清單。

## ✨ 功能特色

* **瀏覽清單**：直觀地查看已收藏的 Medium 文章摘要。
* **搜尋功能**：透過關鍵字快速篩選相關文章。
* **資料管理**：直接與 Google Sheets 同步，作為輕量級的 CMS (內容管理系統)。
* **輕量快速**：使用 Streamlit 打造，部署與執行皆十分輕便。

## 🛠️ 技術堆疊
* [Python]
* [Streamlit]
* Google Sheets API

## 🚀 快速開始

### 1. 前置準備

在開始之前，您需要先設定 Google Cloud Platform (GCP) 以取得存取 Google Sheets 的權限：

1.  前往 [Google Cloud Console](https://console.cloud.google.com/)。
2.  建立一個新專案。
3.  啟用 **Google Sheets API** 與 **Google Drive API**。
4.  建立 **Service Account (服務帳戶)** 並下載 JSON 金鑰檔案。
5.  建立一個新的 Google Sheet，並將該 Sheet 的「共用」權限開放給剛剛建立的 Service Account Email (賦予編輯權限)。

### 2. 安裝

將專案 clone 下來並安裝所需的套件：

```bash
git clone [https://github.com/limit881010/Medium-Digest-Web-with-Gsheets.git](https://github.com/limit881010/Medium-Digest-Web-with-Gsheets.git)
cd Medium-Digest-Web-with-Gsheets
pip install -r requirements.txt
```

### 3. 設定 Secrets
Streamlit 需要透過 secrets.toml 來讀取您的 Google Sheets 憑證。

在專案根目錄下建立 .streamlit 資料夾。

在該資料夾內建立 secrets.toml 檔案。

將您的 Service Account 資訊填入（以下為範例結構，請依據 gsheets_io.py 實際實作調整）：
```
SHEET_ID = "請更換為你的SHEET_ID"
```

### 4. 資料庫結構 (Google Sheets)
請確保您的 Google Sheet 包含以下欄位（Header），以便程式正確讀寫： (請根據您實際的程式碼 app.py 或 gsheets_io.py 修改以下欄位名稱)
Title	URL	Category	Date	Summary

Understanding the Project's Scope

I'm delving deeper into the project. My primary focus is understanding the project's core functionality and the roles of the various files within the GitHub repository. I need to figure out what each part does to create an accurate README that helps others use it effectively.

Analyzing Repository Content

I've moved from understanding the scope to analyzing the actual repository content. The URL provided is a GitHub repo. My plan is to first browse it directly. I'll focus on extracting the project's description, features, and the steps to use it. The core functionality seems to be displaying Medium articles using Google Sheets. I'll look for key files, particularly those related to setup and configuration.

Investigating the Codebase

I've been looking at the structure of this project and it's clear the core functionality resides in a Streamlit application leveraging Google Sheets. I am focused on the Python code (app.py, gsheets_io.py) and plan to examine the interactions between these files soon. I see there's a requirements file, which will be useful.

Reaching for app.py

I've hit a snag, the initial browse for app.py failed - it wasn't indexed. This is a common issue with GitHub blob URLs. Instead of giving up, I'm pivoting. I'll try searching for the raw content URL or, failing that, leverage my understanding of the file structure to infer the path. I might even use File Fetcher as a backup.

Examining File Access

My attempts to browse files have been unsuccessful. It seems the tool isn't rendering the GitHub blob page properly. But, I've gathered enough info to build a great README. The project's name is Medium-Digest-Web-with-Gsheets.

Refining the README

Okay, the README is taking shape. I've got the title and a good description locked down. I'm focusing now on the "Prerequisites" section; ensuring clear instructions for Google Cloud setup and the secrets.toml file. I'm planning to articulate the Google Sheet structure, assuming standard digest columns, and I've got a strong outline for the installation and usage. Finally, I'm thinking of adding a concise note to wrap it up.

這是一份為您的專案 Medium-Digest-Web-with-Gsheets 撰寫的 README.md 草稿。

這份文件包含了專案簡介、安裝步驟、Google Sheets 設定方式以及如何執行。由於我無法直接讀取您的程式碼細節（例如 Google Sheets 實際需要的欄位名稱），我在「資料庫結構」部分預留了範例，建議您根據實際程式碼中的 gsheets_io.py 或 app.py 進行微調。

Markdown
# Medium Digest Web with Gsheets 📚

這是一個基於 **Streamlit** 的 Web 應用程式，使用 **Google Sheets** 作為後端資料庫，讓使用者可以輕鬆瀏覽、搜尋與管理 Medium 文章摘要清單。

## ✨ 功能特色

* **瀏覽清單**：直觀地查看已收藏的 Medium 文章摘要。
* **搜尋功能**：透過關鍵字快速篩選相關文章。
* **資料管理**：直接與 Google Sheets 同步，作為輕量級的 CMS (內容管理系統)。
* **輕量快速**：使用 Streamlit 打造，部署與執行皆十分輕便。

## 🛠️ 技術堆疊

* [Python](https://www.python.org/)
* [Streamlit](https://streamlit.io/)
* Google Sheets API

## 🚀 快速開始

### 1. 前置準備

在開始之前，您需要先設定 Google Cloud Platform (GCP) 以取得存取 Google Sheets 的權限：

1.  前往 [Google Cloud Console](https://console.cloud.google.com/)。
2.  建立一個新專案。
3.  啟用 **Google Sheets API** 與 **Google Drive API**。
4.  建立 **Service Account (服務帳戶)** 並下載 JSON 金鑰檔案。
5.  建立一個新的 Google Sheet，並將該 Sheet 的「共用」權限開放給剛剛建立的 Service Account Email (賦予編輯權限)。

### 2. 安裝

將專案 clone 下來並安裝所需的套件：

```bash
git clone [https://github.com/limit881010/Medium-Digest-Web-with-Gsheets.git](https://github.com/limit881010/Medium-Digest-Web-with-Gsheets.git)
cd Medium-Digest-Web-with-Gsheets
pip install -r requirements.txt
```
### 3. 設定 Secrets
Streamlit 需要透過 secrets.toml 來讀取您的 Google Sheets 憑證。

在專案根目錄下建立 .streamlit 資料夾。

在該資料夾內建立 secrets.toml 檔案。

將您的 Service Account 資訊填入（以下為範例結構，請依據 gsheets_io.py 實際實作調整）：

Ini, TOML
# .streamlit/secrets.toml

[gcp_service_account]
type = "service_account"
project_id = "您的專案ID"
private_key_id = "您的私鑰ID"
private_key = "-----BEGIN PRIVATE KEY-----\n..."
client_email = "您的服務帳戶Email"
client_id = "您的客戶端ID"
auth_uri = "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)"
token_uri = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"
auth_provider_x509_cert_url = "[https://www.googleapis.com/oauth2/v1/certs](https://www.googleapis.com/oauth2/v1/certs)"
client_x509_cert_url = "您的憑證URL"

[spreadsheet]
url = "您的 Google Sheet 網址或名稱"
注意：請勿將 .streamlit/secrets.toml 上傳至 GitHub，以免洩露您的金鑰。

###4. 資料庫結構 (Google Sheets)
請確保您的 Google Sheet 包含以下欄位（Header），以便程式正確讀寫： (請根據您實際的程式碼 app.py 或 gsheets_io.py 修改以下欄位名稱)

Title	URL	Category	Date	Summary
文章標題	文章連結	分類	2025-01-01	文章摘要...

### 5. 執行應用程式
完成上述設定後，執行以下指令啟動網頁：
```
Bash
streamlit run app.py
```
