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

# Import our existing analysis modules
from analysis.config import gemini_model
from analysis.prompts import FINANCIAL_ANALYSIS_PROMPT, SIMPLE_ANALYSIS_PROMPT
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

def optimize_content_for_analysis(content):
    """
    Optimize content for financial analysis while preserving important numerical data
    Prioritizes sections with financial numbers and maintains document structure
    """
    if len(content) <= 15000:  # More generous threshold
        return content
    
    import re
    
    # Enhanced financial keywords
    financial_keywords = [
        'revenue', 'profit', 'income', 'assets', 'liabilities', 'equity',
        'cash flow', 'margin', 'ratio', 'debt', 'earnings', 'financial',
        'management discussion', 'md&a', 'risk', 'outlook', 'performance',
        'quarter', 'annual', 'fiscal', 'operating', 'net income', 'gross profit',
        'ebitda', 'eps', 'diluted', 'basic', 'shares', 'dividend', 'acquisition',
        'consolidated', 'segment', 'geographic', 'business', 'tax', 'provision'
    ]
    
    # Split into paragraphs and score by financial relevance
    paragraphs = content.split('\n\n')
    scored_paragraphs = []
    
    for i, para in enumerate(paragraphs):
        if len(para.strip()) < 20:
            continue
            
        score = 0
        para_lower = para.lower()
        
        # HEAVILY prioritize sections with lots of numbers (financial data)
        # Enhanced regex for better financial number detection
        financial_numbers = re.findall(r'[\$€£¥][\d,]+(?:\.\d+)?[KMBkmb]?|\d+\.\d+%|\d+%|\d{1,3}(?:,\d{3})*(?:\.\d+)?[KMBkmb]?|\d+\.\d+|\d+,\d+', para)
        score += len(financial_numbers) * 25  # Much higher weight for numbers
        
        # Extra boost for dense numerical content
        if len(financial_numbers) > 3:
            score += 50  # High boost for number-rich sections
        
        # Score based on financial keywords
        for keyword in financial_keywords:
            score += para_lower.count(keyword) * 10
            
        # Extra boost for financial statement sections and headers
        statement_indicators = ['consolidated', 'statement', 'balance sheet', 'income statement', 
                              'cash flows', 'stockholders equity', 'comprehensive income',
                              'three months ended', 'six months ended', 'year ended', 'fiscal']
        if any(term in para_lower for term in statement_indicators):
            score += 40
            
        # Boost for important sections that appear early (preserve structure)
        if i < len(paragraphs) * 0.3:  # First 30% of document
            score += 15
            
        # Boost for sections with financial ratios and metrics
        ratio_terms = ['margin', 'ratio', 'return on', 'earnings per share', 'book value', 'debt to']
        if any(term in para_lower for term in ratio_terms):
            score += 30
        
        scored_paragraphs.append((score, i, para))  # Include original position
    
    # Sort by score but maintain some original order for high-scoring consecutive sections
    scored_paragraphs.sort(reverse=True, key=lambda x: x[0])
    
    # Build optimized content with much higher limits
    optimized_content = ""
    total_length = 0
    max_length = 15000  # Optimized for Heroku timeout while preserving key data
    
    selected_paragraphs = []
    
    for score, original_pos, para in scored_paragraphs:
        if total_length + len(para) <= max_length:
            selected_paragraphs.append((original_pos, para))
            total_length += len(para)
        elif score > 80 and total_length < max_length - 500:  # High-value content
            remaining = max_length - total_length - 100
            truncated = para[:remaining] + "... [content truncated]"
            selected_paragraphs.append((original_pos, truncated))
            break
    
    # Sort selected paragraphs by original position to maintain document flow
    selected_paragraphs.sort(key=lambda x: x[0])
    
    # Build final content
    for _, para in selected_paragraphs:
        optimized_content += para + "\n\n"
    
    return optimized_content.strip()

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
        
        # Generate unique filename
        analysis_id = generate_analysis_id()
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        filename = f"{analysis_id}_{original_filename}"
        
        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"[{analysis_id}] File saved: {original_filename}")
        
        # Read and optimize file content
        file_content = read_report(filepath)
        
        if file_content is None:
            # Clean up the uploaded file
            os.remove(filepath)
            return jsonify({
                'success': False,
                'error': 'Unable to read the uploaded file. Please check the file format.'
            }), 400
        
        # Optimize content for faster processing
        optimized_content = optimize_content_for_analysis(file_content)
        optimization_ratio = len(optimized_content) / len(file_content)
        
        print(f"[{analysis_id}] Content optimized: {len(file_content)} -> {len(optimized_content)} chars ({optimization_ratio:.1%})")
        
        # Perform analysis with optimized content
        analysis_result = analyze_financial_report(optimized_content, analysis_id)
        
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
                'optimized_length': len(optimized_content),
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

def analyze_financial_report(report_text, analysis_id):
    """
    Analyze financial report using Gemini API with optimizations
    
    Args:
        report_text (str): Content of the financial report
        analysis_id (str): Unique identifier for this analysis
        
    Returns:
        str: Analysis result or None if failed
    """
    try:
        if gemini_model is None:
            print(f"[{analysis_id}] Gemini model not initialized")
            return None
        
        # Format the optimized prompt
        formatted_prompt = FINANCIAL_ANALYSIS_PROMPT.format(report_text=report_text)
        
        print(f"[{analysis_id}] Starting analysis... (prompt length: {len(formatted_prompt)} chars)")
        
        # Configure generation settings optimized for Heroku 30s timeout
        
        generation_config = {
            'temperature': 0.3,  # Lower for faster, more focused responses
            'top_p': 0.8,       # Reduced for faster generation
            'top_k': 16,        # Reduced for faster generation
            'max_output_tokens': 4000,  # Balanced for complete analysis within timeout
        }
        
        start_time = time.time()
        
        # Generate analysis with timeout handling (optimized for Heroku 30s limit)
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("API call timed out")
        
        # Set a 22-second timeout to stay well within Heroku's 30s limit
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(22)
        
        try:
            response = gemini_model.generate_content(
                formatted_prompt,
                generation_config=generation_config
            )
            
            # Cancel the alarm
            signal.alarm(0)
            
            api_time = time.time() - start_time
            print(f"[{analysis_id}] API response time: {api_time:.2f}s")
            
            if response.text:
                print(f"[{analysis_id}] Analysis completed successfully")
                return response.text
            else:
                print(f"[{analysis_id}] Empty response from main prompt, trying simpler approach...")
                
                # Try simpler prompt as fallback
                simple_prompt = SIMPLE_ANALYSIS_PROMPT.format(report_text=report_text)
                print(f"[{analysis_id}] Trying simple prompt (length: {len(simple_prompt)} chars)")
                
                try:
                    fallback_response = gemini_model.generate_content(
                        simple_prompt,
                        generation_config=generation_config
                    )
                    
                    if fallback_response.text and fallback_response.text.strip():
                        print(f"[{analysis_id}] Simple prompt succeeded")
                        return fallback_response.text
                    else:
                        print(f"[{analysis_id}] Both prompts failed - checking response details")
                        if hasattr(response, 'candidates'):
                            print(f"[{analysis_id}] Main response candidates: {len(response.candidates) if response.candidates else 'None'}")
                        if hasattr(fallback_response, 'candidates'):
                            print(f"[{analysis_id}] Fallback response candidates: {len(fallback_response.candidates) if fallback_response.candidates else 'None'}")
                        return "Analysis completed but both main and fallback prompts generated no content. The AI model may be experiencing issues or the document format is not suitable. Please try a different document."
                except Exception as fallback_error:
                    print(f"[{analysis_id}] Fallback prompt failed: {fallback_error}")
                    return "Analysis completed but main prompt failed and fallback prompt encountered an error. Please try again later."
                
        except TimeoutError:
            signal.alarm(0)  # Cancel alarm
            print(f"[{analysis_id}] API call timed out after 22 seconds")
            return "Analysis timed out due to Heroku's 30-second limit. The document may be too complex. Please try with a smaller file or try again later."
            
        except Exception as api_error:
            signal.alarm(0)  # Cancel alarm
            print(f"[{analysis_id}] API error: {api_error}")
            
            # Handle specific error types
            if "quota" in str(api_error).lower():
                return "Analysis temporarily unavailable due to API quota limits. Please try again in a few minutes."
            elif "timeout" in str(api_error).lower():
                return "Analysis timed out. Please try with a smaller file or try again later."
            else:
                return f"Analysis failed due to API error. Please try again. Error: {str(api_error)[:100]}"
        
    except Exception as e:
        print(f"[{analysis_id}] Analysis error: {e}")
        return f"Analysis failed due to system error. Please try again. Error: {str(e)[:100]}"

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'gemini_model': 'available' if gemini_model else 'unavailable',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
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
    # Check if Gemini model is available
    if gemini_model is None:
        print("⚠️ Warning: Gemini model not initialized. Check your .env configuration.")
    else:
        print("✅ Gemini model ready for analysis")
    
    # Run the app
    print("🚀 Starting Financial Analysis Co-Pilot Web App...")
    print("📁 Supported file formats: TXT, PDF, DOCX, XLSX, CSV")
    print("⚡ Optimized for speed with intelligent content processing")
    
    # Use environment variables for production deployment
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port) 