# Medium Digest Web with Gsheets 📚

這是一個基於 **Streamlit** 的 Web 應用程式，使用 **Google Sheets** 作為後端資料庫，讓使用者可以輕鬆瀏覽、搜尋與管理 Medium 文章摘要清單，並且於[freedium](https://freedium.cfd/)上觀看。

## ✨ 功能特色

* **瀏覽清單**：直觀地查看已收藏的 Medium 文章摘要。
* **搜尋功能**：透過關鍵字快速篩選相關文章。
* **資料管理**：直接與 Google Sheets 同步，作為輕量級的 CMS (內容管理系統)。
* **輕量快速**：使用 Streamlit 打造，部署與執行皆十分輕便。

## 🛠️ 技術堆疊
* [Python]
* [Streamlit]
* Google Sheets API

## 📂 檔案結構
app.py: Streamlit 應用程式的主入口，負責 UI 顯示與邏輯。

gsheets_io.py: 負責與 Google Sheets API 進行串接與資料處理。

requirements.txt: 專案所需的 Python 套件清單。

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
#### .streamlit/secrets.toml

```[gcp_service_account]
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
```
[spreadsheet]
url = "您的 Google Sheet 網址或名稱"
注意：請勿將 .streamlit/secrets.toml 上傳至 GitHub，以免洩露您的金鑰。

將您的 Service Account 資訊填入（以下為範例結構，請依據 gsheets_io.py 實際實作調整）：

#### app.py中
```
SHEET_ID = "請更換為你的SHEET_ID"
```

### 4. 資料庫結構 (Google Sheets)
請確保您的 Google Sheet 包含以下欄位（Header），以便程式正確讀寫： (請根據您實際的程式碼 app.py 或 gsheets_io.py 修改以下欄位名稱)

Title	URL	Category	Date	Summary
文章標題	文章連結	分類	2025-01-01	文章摘要...

### 5. 執行應用程式
完成上述設定後，執行以下指令啟動網頁：
```
Bash
streamlit run app.py
```
瀏覽器應會自動開啟 http://localhost:8501。


<img width="1919" height="887" alt="image" src="https://github.com/user-attachments/assets/04a2718e-43aa-4f44-a602-9bb19f60450b" />

# Enjoy it !!!🎉🎉🎉
