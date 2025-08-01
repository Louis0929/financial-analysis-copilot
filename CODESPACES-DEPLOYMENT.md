# 🚀 GitHub Codespaces 部署指南

這是最簡單嘅部署方法！用GitHub Codespaces避免本地SDK問題。

## 📋 部署步驟

### 1. 開啟 GitHub Codespaces
1. 去你嘅GitHub倉庫：https://github.com/Louis0929/financial-analysis-copilot
2. 撳綠色 "Code" 按鈕
3. 選擇 "Codespaces" 標籤
4. 撳 "Create codespace on main"

### 2. 等待環境準備
- Codespaces會自動安裝：
  - ✅ Google Cloud SDK
  - ✅ Python依賴
  - ✅ Docker支援

### 3. 設置Google Cloud
```bash
# 登入Google Cloud
gcloud auth login

# 設定項目ID（如果未有，先創建）
gcloud config set project YOUR_PROJECT_ID

# 或者創建新項目
gcloud projects create financial-analysis-app-$(date +%s)
gcloud config set project financial-analysis-app-$(date +%s)
```

### 4. 設定API Key
```bash
# 設定你嘅Gemini API Key
export GOOGLE_API_KEY="your-gemini-api-key-here"
```

### 5. 部署到Cloud Run
```bash
# 直接執行部署腳本
chmod +x deploy-to-cloudrun.sh
./deploy-to-cloudrun.sh
```

## 🎯 完成！

你嘅app就會部署到Google Cloud Run，有：
- ⏰ 5分鐘超時（vs Heroku嘅30秒）
- 💾 2GB記憶體
- 🚀 自動縮放到零
- 💰 免費額度：每月200萬請求

## 🔧 故障排除

如果遇到問題：
1. 確保Google Cloud項目已啟用計費
2. 檢查GOOGLE_API_KEY環境變數
3. 確保已登入gcloud：`gcloud auth list`