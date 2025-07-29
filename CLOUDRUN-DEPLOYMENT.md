# 🚀 Google Cloud Run Deployment Guide

This guide will help you migrate your Financial Analysis app from Heroku to Google Cloud Run for **5-minute timeouts** and **better performance**.

## ✅ Benefits of Cloud Run vs Heroku

| Feature | Heroku | Google Cloud Run |
|---------|--------|------------------|
| **Timeout** | 30 seconds (fixed) | 5 minutes (configurable) |
| **Free Tier** | 550 hours/month | 2 million requests/month |
| **Auto-scaling** | Manual | Automatic (scales to zero) |
| **Memory** | 512MB | Up to 8GB |
| **Cost** | $7/month after free tier | Pay-per-use (usually free) |

## 🛠️ Step-by-Step Deployment

### 1. Prerequisites

**Install Google Cloud SDK:**
```bash
# macOS
brew install google-cloud-sdk

# Windows/Linux
# Download from: https://cloud.google.com/sdk/docs/install
```

**Authenticate:**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Set Up Google Cloud Project

**Create a new project (or use existing):**
```bash
# Create new project
gcloud projects create financial-analysis-app-XXXX
gcloud config set project financial-analysis-app-XXXX

# Enable billing (required for Cloud Run)
# Go to: https://console.cloud.google.com/billing
```

### 3. Set Environment Variables

**Set your Gemini API key:**
```bash
export GOOGLE_API_KEY="your-gemini-api-key-here"
```

### 4. Deploy to Cloud Run

**Option A: Use the automated script (recommended):**
```bash
chmod +x deploy-to-cloudrun.sh
./deploy-to-cloudrun.sh
```

**Option B: Manual deployment:**
```bash
# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com

# Build and submit
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/financial-analysis-app

# Deploy
gcloud run deploy financial-analysis-app \
    --image gcr.io/YOUR_PROJECT_ID/financial-analysis-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --timeout 300 \
    --memory 2Gi \
    --cpu 1 \
    --max-instances 10 \
    --concurrency 1 \
    --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY
```

### 5. Configure Domain (Optional)

**Map a custom domain:**
```bash
gcloud run domain-mappings create \
    --service financial-analysis-app \
    --domain your-domain.com \
    --region us-central1
```

## 🎯 What's Changed for Cloud Run

### ⏰ **Increased Timeouts:**
- **Analysis timeout**: 10 seconds → **2 minutes**
- **Content processing**: 6K → **25K characters**  
- **Output tokens**: 2K → **8K tokens**

### 🔧 **Better Configuration:**
- **Memory**: 2GB (vs Heroku's 512MB)
- **CPU**: 1 vCPU dedicated
- **Concurrency**: 1 request per instance (for AI processing)
- **Auto-scaling**: Scales to zero when unused

### 💰 **Cost Comparison:**

**Heroku:**
- Free: 550 hours/month, then $7/month
- Fixed cost regardless of usage

**Cloud Run:**
- Free: 2 million requests/month
- Pay-per-use after free tier
- Scales to zero = no cost when unused

## 🔍 Monitoring & Logs

**View logs:**
```bash
gcloud logs tail --service=financial-analysis-app
```

**Monitor performance:**
```bash
gcloud run services describe financial-analysis-app --region=us-central1
```

## 🚨 Troubleshooting

### Common Issues:

**1. API Key not set:**
```bash
gcloud run services update financial-analysis-app \
    --set-env-vars GOOGLE_API_KEY=your-key-here \
    --region us-central1
```

**2. Billing not enabled:**
- Go to [Google Cloud Console](https://console.cloud.google.com/billing)
- Enable billing for your project

**3. Memory issues:**
```bash
# Increase memory if needed
gcloud run services update financial-analysis-app \
    --memory 4Gi \
    --region us-central1
```

## 📊 Expected Performance

With Cloud Run, you should now be able to:
- ✅ **Analyze large Microsoft 10-K reports** (vs timing out on Heroku)
- ✅ **Complete full 3-section analysis** with interpretations
- ✅ **Process 25K characters** of financial data
- ✅ **Generate detailed recommendations** with 8K token output

## 🔄 Future Updates

To update your app:
```bash
# Make code changes, then:
./deploy-to-cloudrun.sh
```

Your Cloud Run service will automatically update with zero downtime!

---

## 🎉 Migration Complete!

Your Financial Analysis app now runs on Google Cloud Run with:
- **5-minute timeout** (vs 30 seconds)
- **2GB memory** (vs 512MB)  
- **Auto-scaling** (vs fixed dynos)
- **Better free tier** (vs limited hours)

Test it with your largest financial documents! 🚀 