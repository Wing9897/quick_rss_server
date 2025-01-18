# 速食RSS

這是一個基於 Flask 的簡單 RSS 生成應用程序，允許用戶提交科研資訊，並生成對應的 RSS Feed。應用會隨機生成一張圖片並與每個提交的項目一同顯示。

## 功能

- 用戶可以提交標題和內容，並生成新的 RSS 項目。
- 每個 RSS 項目都可以包含一張隨機圖片。
- 應用支持生成 RSS Feed，並提供給用戶查看。

## 技術棧

- Python
- Flask
- SQLAlchemy
- SQLite
- HTML/CSS

## 安裝步驟

1. **克隆此倉庫**

   ```bash
   git clone https://github.com/你的用戶名/速食RSS.git
   cd 速食RSS
   ```

2. **創建虛擬環境**

   ```bash
   python -m venv venv
   source venv/bin/activate  # 在 Windows 上：venv\Scripts\activate
   ```

3. **安裝依賴**

   ```bash
   pip install -r requirements.txt
   ```

4. **初始化資料庫**

   在 Python shell 中運行以下命令：

   ```python
   from app import init_db
   init_db()
   ```

5. **運行應用**

   ```bash
   python app.py
   ```

   打開瀏覽器並訪問 `http://127.0.0.1:5000`。

## 使用說明

- 在主頁輸入科研資訊的標題和內容，然後提交。
- 所有提交的項目將顯示在頁面上，並且每個項目會隨機顯示一張圖片。
- 點擊「查看 RSS Feed」鏈接以查看生成的 RSS Feed。

## 貢獻

歡迎任何形式的貢獻！請提交問題或拉取請求。

## 授權

此項目採用 MIT 授權，詳情請參見 `LICENSE` 文件。 

## 聯繫

如有問題或建議，請隨時發送郵件或通過 GitHub 聯繫我。
