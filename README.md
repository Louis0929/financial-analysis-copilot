# 🚀 Financial Analysis Co-Pilot

A professional, AI-powered web application designed to analyze corporate financial statements. This tool leverages the Google Gemini API to deliver deep, actionable insights from complex documents like 10-K reports, transforming dense financial data into clear, digestible analysis.

*Created by Louis Yeung for a university project, showcasing modern web development and applied AI.*

---

## ✨ Key Features

- **Advanced AI Analysis**: Utilizes the Google Gemini API for nuanced understanding of financial texts.
- **Multi-Format Document Support**: Seamlessly handles PDF, DOCX, XLSX, TXT, and CSV files.
- **Intelligent 10-K Analysis**: A specialized two-step process first locates the core financial statements within lengthy 10-K reports and then performs a detailed analysis.
- **Full-Text Processing**: Trusts the AI to analyze the entire document context, ensuring no data is missed, regardless of its position in the file.
- **Professional Report Generation**: Presents analysis in a clean, card-based UI for enhanced readability.
- **PDF Report Downloads**: Exports the beautifully formatted analysis into a downloadable PDF document.
- **Secure & Ephemeral**: Ensures user privacy by deleting uploaded files immediately after analysis.

---

## 💻 Tech Stack

- **Backend**: Python 3.12, Flask
- **AI Engine**: Google Gemini API
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **File Parsing**: `PyPDF2`, `python-docx`, `openpyxl`, `pandas`
- **Deployment**: Google Cloud Run, Docker
- **PDF Generation**: `jsPDF`, `html2canvas`

---

## 🖼️ Screenshots

*(It is highly recommended to add a few screenshots of your application here. For example: the upload interface, the loading screen, and the final analysis report.)*

**Upload Interface**
`![Upload UI](link_to_your_screenshot.png)`

**Analysis Report**
`![Report UI](link-to-your_screenshot.png)`

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python 3.10+
- A Google Gemini API Key. You can obtain one from [Google AI Studio](https://makersuite.google.com/app/apikey).
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and authenticated (for deployment).

### Local Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Louis0929/financial-analysis-copilot.git
    cd financial-analysis-copilot
    ```

2.  **Create a Virtual Environment & Install Dependencies**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Install packages
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**
    Create a file named `.env` in the project root and add your API key:
    ```
    GOOGLE_API_KEY="your_google_api_key_here"
    ```

4.  **Run the Application**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

---

## ☁️ Deployment to Google Cloud Run

This project is configured for easy deployment to Google Cloud Run.

1.  **Authenticate with Google Cloud**
    Make sure you have authenticated your gcloud CLI.
    ```bash
    gcloud auth login
    gcloud auth application-default login
    ```

2.  **Run the Deployment Script**
    The `deploy-to-cloudrun.sh` script handles the entire process: setting the project, enabling necessary APIs, building the Docker container with Cloud Build, and deploying the service.

    > **Note:** You may need to edit the script to set your own `PROJECT_ID`.

    ```bash
    # Make the script executable
    chmod +x deploy-to-cloudrun.sh

    # Run the deployment
    ./deploy-to-cloudrun.sh
    ```

3.  **Access Your Deployed App**
    The script will output the URL of your deployed service upon successful completion.

---

## 📂 Project Structure

```
financial-analysis-copilot/
├── app.py                  # Main Flask application logic
├── deploy-to-cloudrun.sh   # Deployment script for Google Cloud Run
├── Dockerfile              # Container configuration for deployment
├── requirements.txt        # Python dependencies
├── .env                    # Local environment variables (gitignored)
├── analysis/               # Core AI and file processing modules
│   ├── config.py           # Gemini API model configuration
│   ├── file_reader.py      # Utilities for reading different file formats
│   └── prompts.py          # Prompt templates for the Gemini API
├── static/                 # Frontend assets
│   ├── css/style.css       # Main stylesheet
│   └── js/app.js           # Frontend interactivity and PDF generation
└── templates/              # HTML files
    ├── index.html          # Main application page
    └── 404.html            # 404 error page
```
