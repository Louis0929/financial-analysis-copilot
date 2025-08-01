#!/bin/bash

echo "🔧 Setting up Google Cloud SDK in Codespaces..."

# Install Google Cloud SDK
if ! command -v gcloud &> /dev/null; then
    echo "Installing Google Cloud SDK..."
    curl -sSL https://sdk.cloud.google.com | bash
    
    # Add to PATH
    echo 'export PATH="$HOME/google-cloud-sdk/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    
    echo "✅ Google Cloud SDK installed!"
else
    echo "✅ Google Cloud SDK already installed!"
fi

echo ""
echo "🚀 Ready for deployment!"
echo ""
echo "Next steps:"
echo "1. gcloud auth login"
echo "2. export GOOGLE_API_KEY='your-api-key'"
echo "3. ./deploy-to-cloudrun.sh"