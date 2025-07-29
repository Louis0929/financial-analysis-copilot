#!/bin/bash

echo "🚀 Financial Analysis App - Google Cloud Run Deployment Script"
echo "============================================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: Google Cloud SDK not found. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No Google Cloud project selected."
    echo "   Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📋 Using Google Cloud Project: $PROJECT_ID"
echo ""

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

echo ""
echo "🏗️  Building and deploying to Cloud Run..."

# Submit build to Cloud Build
gcloud builds submit \
    --tag gcr.io/$PROJECT_ID/financial-analysis-app \
    --project=$PROJECT_ID

# Deploy to Cloud Run
gcloud run deploy financial-analysis-app \
    --image gcr.io/$PROJECT_ID/financial-analysis-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --timeout 300 \
    --memory 2Gi \
    --cpu 1 \
    --max-instances 10 \
    --concurrency 1 \
    --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY \
    --project=$PROJECT_ID

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Your app is now running on Google Cloud Run with:"
echo "   ⏰ 5-minute timeout (vs Heroku's 30 seconds)"
echo "   💾 2GB memory"
echo "   🚀 Auto-scaling to zero when not used"
echo "   💰 Free tier: 2 million requests/month"
echo ""
echo "🔧 Next steps:"
echo "   1. Set your GOOGLE_API_KEY environment variable"
echo "   2. Your app URL will be displayed above"
echo "   3. Test with a large financial document!"
echo "" 