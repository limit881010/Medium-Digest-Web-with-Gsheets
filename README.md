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
