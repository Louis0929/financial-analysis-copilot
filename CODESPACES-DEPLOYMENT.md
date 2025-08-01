# 🚀 GitHub Codespaces 部署指南 (簡化版)

最簡單嘅部署方法！無需複雜配置。

## 📋 部署步驟

### 1. 開啟 GitHub Codespaces
1. 去你嘅GitHub倉庫：https://github.com/Louis0929/financial-analysis-copilot
2. 撳綠色 "Code" 按鈕
3. 選擇 "Codespaces" 標籤
4. 撳 "Create codespace on main"

### 2. 等待基本環境準備 (約1-2分鐘)
- 會有基本嘅Ubuntu環境同Python

### 3. 設置Google Cloud SDK
```bash
# 執行設置腳本
./setup-gcloud.sh

# 重新載入環境
source ~/.bashrc
```

### 4. 設置Google Cloud
```bash
# 登入Google Cloud
gcloud auth login

# 設定項目ID（如果未有，先創建）
gcloud config set project YOUR_PROJECT_ID

# 或者創建新項目
gcloud projects create financial-analysis-app-$(date +%s)
gcloud config set project financial-analysis-app-$(date +%s)
```

### 5. 設定API Key
```bash
# 設定你嘅Gemini API Key
export GOOGLE_API_KEY="your-gemini-api-key-here"
```

### 6. 部署到Cloud Run
```bash
# 執行部署腳本
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