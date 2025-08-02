"""
Configuration module for Financial Analysis Co-Pilot
Handles Google Gemini API setup and initialization
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def configure_gemini():
    """
    Configure and initialize the Google Gemini model
    Returns the configured model instance
    """
    # Get API key from environment variables
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # Try 1.5-flash first (faster), fallback to 1.5-pro (more reliable for large docs)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("Using Gemini 1.5 Flash model")
        return model
    except Exception as e:
        print(f"Flash model failed: {e}, trying Pro model...")
        model = genai.GenerativeModel('gemini-1.5-pro')
        print("Using Gemini 1.5 Pro model")
        return model

# Initialize the model instance for import
try:
    gemini_model = configure_gemini()
    print("✅ Google Gemini model initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Gemini model: {e}")
    gemini_model = None 