"""
Financial Statement Analysis Co-Pilot - Web Application
Flask backend with file upload and Gemini API integration

Author: [Your Name]
Date: [Current Date]
Purpose: University project - Web-based financial statement analysis
"""

import os
import json
import uuid
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import signal

# Import our existing analysis modules
from analysis.config import gemini_model
from analysis.prompts import FINANCIAL_ANALYSIS_PROMPT, TEN_K_ANALYSIS_PROMPT, LOCATE_FINANCIALS_PROMPT
from analysis.file_reader import read_report

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Supported file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'xlsx', 'xls', 'csv'}

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('analysis', exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_analysis_id():
    """Generate a unique analysis ID"""
    return str(uuid.uuid4())[:8]

def clean_old_files():
    """Clean up old uploaded files (older than 1 hour)"""
    try:
        upload_dir = app.config['UPLOAD_FOLDER']
        current_time = datetime.now().timestamp()
        
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)
                # Delete files older than 1 hour (3600 seconds)
                if current_time - file_time > 3600:
                    os.remove(file_path)
    except Exception as e:
        print(f"Error cleaning old files: {e}")

@app.route('/')
def index():
    """Main page with file upload interface"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and return analysis results"""
    start_time = time.time()
    
    try:
        # Clean old files periodically
        clean_old_files()
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file selected for upload'
            }), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected for upload'
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not supported. Allowed types: {", ".join(ALLOWED_EXTENSIONS).upper()}'
            }), 400
        
        # Get analysis type
        analysis_type = request.form.get('analysisType', 'general')
        
        # Generate unique filename
        analysis_id = generate_analysis_id()
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        filename = f"{analysis_id}_{original_filename}"
        
        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"[{analysis_id}] File saved: {original_filename}")
        
        # Read file content
        file_content = read_report(filepath)
        
        if file_content is None or not file_content.strip():
            os.remove(filepath)
            return jsonify({
                'success': False,
                'error': 'Unable to read the uploaded file or the file is empty. Please check the file format.'
            }), 400
        
        print(f"[{analysis_id}] Read {len(file_content)} characters from file.")

        # Perform analysis with raw content
        analysis_result = analyze_financial_report(file_content, analysis_id, analysis_type)
        
        # Clean up the uploaded file after analysis
        os.remove(filepath)
        
        if analysis_result is None:
            return jsonify({
                'success': False,
                'error': 'Analysis failed. This might be due to API rate limits or quota exceeded. Please try again later.'
            }), 500
        
        processing_time = time.time() - start_time
        print(f"[{analysis_id}] Total processing time: {processing_time:.2f}s")
        
        return jsonify({
            'success': True,
            'data': {
                'analysis_id': analysis_id,
                'filename': original_filename,
                'file_type': file_extension.upper(),
                'content_length': len(file_content),
                'processing_time': round(processing_time, 2),
                'analysis_result': analysis_result,
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except RequestEntityTooLarge:
        return jsonify({
            'success': False,
            'error': 'File too large. Maximum size allowed is 16MB.'
        }), 413
        
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({
            'success': False,
            'error': f'An unexpected error occurred: {str(e)}'
        }), 500

def _call_gemini_api(prompt, analysis_id, timeout_seconds=180): # Increased timeout for long docs
    """
    A helper function to call the Gemini API with a given prompt and timeout.
    """
    if gemini_model is None:
        print(f"[{analysis_id}] Gemini model not initialized")
        return None, "Gemini model not initialized. Check API key."

    print(f"[{analysis_id}] Calling Gemini API... (prompt length: {len(prompt)} chars)")
    start_time = time.time()

    generation_config = {
        'temperature': 0.3,
        'top_p': 0.9,
        'top_k': 20,
        'max_output_tokens': 8000,
    }

    def timeout_handler(signum, frame):
        raise TimeoutError(f"API call timed out after {timeout_seconds} seconds")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)

    try:
        response = gemini_model.generate_content(
            prompt,
            generation_config=generation_config
        )
        signal.alarm(0)  # Cancel the alarm
        api_time = time.time() - start_time
        print(f"[{analysis_id}] API response time: {api_time:.2f}s")

        if response.text:
            return response.text, None
        else:
            error_message = "API returned an empty response. The model may be unable to process the request."
            print(f"[{analysis_id}] {error_message}")
            return None, error_message

    except TimeoutError as e:
        signal.alarm(0)
        print(f"[{analysis_id}] {e}")
        return None, str(e)
    except Exception as api_error:
        signal.alarm(0)
        print(f"[{analysis_id}] API error: {api_error}")
        error_str = str(api_error)
        if "quota" in error_str.lower():
            return None, "Analysis temporarily unavailable due to API quota limits."
        return None, f"API error: {error_str[:150]}"


def analyze_financial_report(report_text, analysis_id, analysis_type='general'):
    """
    Analyze financial report using a two-step process for 10-K reports.
    """
    try:
        if analysis_type == '10k':
            # --- STEP 1: LOCATE AND EXTRACT FINANCIAL STATEMENTS ---
            # We now pass the ENTIRE document text to the AI, trusting it to find the statements.
            print(f"[{analysis_id}] 10-K Analysis Step 1: Locating financials in the full document...")
            locate_prompt = LOCATE_FINANCIALS_PROMPT.format(report_text=report_text)
            # Use a longer timeout for the location step as it now processes the full document
            extracted_text, error = _call_gemini_api(locate_prompt, analysis_id, timeout_seconds=120)

            if error:
                return f"Error during financial statement location (Step 1): {error}"

            # --- DIAGNOSTIC LOGGING ---
            print("\n" + "="*80)
            print(f"[{analysis_id}] [DIAGNOSTIC LOG] Start of Extracted Text from Step 1:")
            print("-" * 80)
            print(extracted_text[:3000] if extracted_text else "No text was extracted.")
            print("-" * 80)
            print(f"[{analysis_id}] [DIAGNOSTIC LOG] End of Extracted Text. Total length: {len(extracted_text) if extracted_text else 0} chars.")
            print("="*80 + "\n")
            # --- END DIAGNOSTIC LOGGING ---

            if not extracted_text or len(extracted_text) < 200 or "FINANCIAL_STATEMENTS_NOT_FOUND" in extracted_text:
                print(f"[{analysis_id}] Location failed or returned minimal/no content. Unable to perform analysis.")
                return ("<h3>Analysis Failed: Could Not Locate Financial Statements</h3>"
                        "<p>The AI was unable to locate the core financial statements within the document. "
                        "This can happen with non-standard 10-K formats or scanned documents. "
                        "Please try a different file.</p>")
            
            print(f"[{analysis_id}] Successfully extracted financial data for Step 2.")
            final_analysis_text = extracted_text

            # --- STEP 2: ANALYZE THE EXTRACTED FINANCIAL DATA ---
            print(f"[{analysis_id}] 10-K Analysis Step 2: Analyzing extracted financial data...")
            analysis_prompt = TEN_K_ANALYSIS_PROMPT.format(report_text=final_analysis_text)
            analysis_result, error = _call_gemini_api(analysis_prompt, analysis_id, timeout_seconds=120)

            if error:
                return f"Error during financial analysis (Step 2): {error}"
            
            return analysis_result

        else: # General Analysis
            print(f"[{analysis_id}] Performing General Analysis...")
            # Truncate for general analysis to keep it quick
            general_prompt = FINANCIAL_ANALYSIS_PROMPT.format(report_text=report_text[:150000])
            analysis_result, error = _call_gemini_api(general_prompt, analysis_id, timeout_seconds=120)
            
            if error:
                return f"Error during general analysis: {error}"
            
            return analysis_result

    except Exception as e:
        print(f"[{analysis_id}] Analysis error in main function: {e}")
        return f"Analysis failed due to a system error. Please try again. Error: {str(e)[:100]}"


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'gemini_model': 'available' if gemini_model else 'unavailable',
        'timestamp': datetime.now().isoformat(),
        'version': '3.0.0' # Final version with full text processing
    })

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size allowed is 16MB.'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error. Please try again later.'
    }), 500

if __name__ == '__main__':
    if gemini_model is None:
        print("⚠️ Warning: Gemini model not initialized. Check your .env configuration.")
    else:
        print("✅ Gemini model ready for analysis")
    
    print("🚀 Starting Financial Analysis Co-Pilot Web App v3.0...")
    print("🤖 Now processing full document context for maximum accuracy!")
    
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 8080))
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
