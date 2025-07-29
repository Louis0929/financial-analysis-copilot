# Financial Statement Analysis Co-Pilot 🚀

A professional web application that uses Google Gemini Pro API to analyze financial statements and provide comprehensive insights including key ratios, executive summaries, and risk assessments.

![Demo](https://img.shields.io/badge/Demo-Live-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.3+-red) ![AI](https://img.shields.io/badge/AI-Gemini%20Pro-purple)

## 🎯 Features

- **Multi-Format Support**: Upload PDF, XLSX, DOCX, TXT, and CSV files
- **AI-Powered Analysis**: Uses Google Gemini 2.5 Pro for comprehensive financial analysis
- **Professional UI**: Business-style, responsive design with drag-and-drop functionality
- **Real-time Processing**: Live analysis with loading indicators and status updates
- **Downloadable Reports**: Export analysis results as formatted text files
- **Secure File Handling**: Automatic cleanup and secure file processing

## 📊 Analysis Capabilities

### 🧮 Key Ratio Calculation
- Gross Profit Margin
- Net Profit Margin  
- Return on Assets (ROA)
- Return on Equity (ROE)
- Debt-to-Equity ratio

### 📋 Executive Summary
- Management Discussion & Analysis (MD&A) highlights
- Business developments and strategic initiatives
- Financial performance trends

### 🚨 Risk Assessment
- Financial risks identification
- Operational risk analysis
- Strategic risk evaluation
- Severity classification (Low/Medium/High)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/financial-analysis-copilot.git
   cd financial-analysis-copilot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google Gemini API key
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   ```
   http://localhost:5000
   ```

## 🌐 Deployment

### Heroku Deployment

1. **Install Heroku CLI** and login
   ```bash
   heroku login
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set GOOGLE_API_KEY=your_api_key_here
   heroku config:set FLASK_DEBUG=False
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Railway Deployment

1. **Connect your GitHub repository** to Railway
2. **Set environment variables** in Railway dashboard:
   - `GOOGLE_API_KEY`: Your Gemini API key
   - `FLASK_DEBUG`: False
3. **Deploy automatically** on push to main branch

### Docker Deployment

```bash
# Build the image
docker build -t financial-analysis-copilot .

# Run the container
docker run -p 5000:5000 -e GOOGLE_API_KEY=your_api_key financial-analysis-copilot
```

## 🏗️ Project Structure

```
financial-analysis-copilot/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── Procfile               # Heroku deployment config
├── analysis/              # Analysis modules
│   ├── __init__.py
│   ├── config.py          # Gemini API configuration
│   ├── prompts.py         # Analysis prompts
│   └── file_reader.py     # File processing utilities
├── templates/             # HTML templates
│   ├── index.html         # Main page
│   └── 404.html          # Error page
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── app.js        # Frontend JavaScript
└── uploads/              # Temporary file storage (gitignored)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here
PORT=5000
```

### API Rate Limits

The application uses Gemini 2.5 Pro with the following considerations:
- Free tier: Limited requests per minute
- Automatic retry logic for rate limit errors
- Graceful error handling with user feedback

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Drag & Drop**: Intuitive file upload experience
- **Loading States**: Visual feedback during processing
- **Error Handling**: Clear error messages and retry options
- **Professional Styling**: Business-appropriate design language
- **Accessibility**: Keyboard navigation and screen reader support

## 🔒 Security Features

- **File Validation**: Strict file type and size checking
- **Automatic Cleanup**: Uploaded files deleted after processing
- **Secure Headers**: CSRF protection and secure file handling
- **Environment Variables**: Sensitive data stored securely

## 📈 Performance

- **Optimized Loading**: Lazy loading and efficient file processing
- **Memory Management**: Automatic file cleanup prevents memory leaks
- **Caching**: Strategic caching for better performance
- **Error Recovery**: Robust error handling and recovery mechanisms

## 🛠️ Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=.
```

### Code Style
```bash
# Install formatting tools
pip install black flake8

# Format code
black .

# Check style
flake8
```

## 📝 API Documentation

### POST /upload
Upload and analyze a financial statement.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (PDF, XLSX, DOCX, TXT, or CSV)

**Response:**
```json
{
  "success": true,
  "data": {
    "analysis_id": "abc123",
    "filename": "report.pdf",
    "file_type": "PDF",
    "content_length": 15000,
    "analysis_result": "...",
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "gemini_model": "available",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational purposes as a university project.

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/yourusername/financial-analysis-copilot/issues) page
2. Review the troubleshooting section below
3. Create a new issue with detailed information

### Troubleshooting

**API Key Issues:**
- Ensure your Gemini API key is valid and active
- Check your API quotas and billing in Google AI Studio

**File Upload Issues:**
- Verify file format is supported (PDF, XLSX, DOCX, TXT, CSV)
- Check file size is under 16MB limit
- Ensure file is not corrupted

**Deployment Issues:**
- Verify all environment variables are set
- Check application logs for detailed error messages
- Ensure Python version compatibility (3.8+)

## 🎓 University Project Context

This project demonstrates:
- Modern web application development with Flask
- AI API integration and prompt engineering
- Professional UI/UX design principles
- Cloud deployment and DevOps practices
- Security best practices for web applications

## 📚 Technologies Used

- **Backend**: Python, Flask, Werkzeug
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI**: Google Gemini 2.5 Pro API
- **File Processing**: PyPDF2, pandas, python-docx, openpyxl
- **Deployment**: Heroku, Railway, Docker
- **Development**: Git, GitHub, pytest

---

Built with ❤️ for financial analysis automation 