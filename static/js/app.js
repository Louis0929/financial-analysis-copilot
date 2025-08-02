// Financial Analysis Co-Pilot - Frontend JavaScript
// Handles file upload, drag-and-drop, API communication, and UI interactions

class FinancialAnalysisApp {
    constructor() {
        this.currentFile = null;
        this.analysisInProgress = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupDragAndDrop();
    }

    setupEventListeners() {
        // File input
        const fileInput = document.getElementById('fileInput');
        const uploadArea = document.getElementById('uploadArea');
        const removeFile = document.getElementById('removeFile');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const newAnalysisBtn = document.getElementById('newAnalysisBtn');
        const retryBtn = document.getElementById('retryBtn');
        const downloadBtn = document.getElementById('downloadBtn');

        // File input change
        fileInput.addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files[0]);
        });

        // Upload area click
        uploadArea.addEventListener('click', () => {
            if (!this.analysisInProgress) {
                fileInput.click();
            }
        });

        // Remove file
        removeFile.addEventListener('click', (e) => {
            e.stopPropagation();
            this.removeFile();
        });

        // Analyze button
        analyzeBtn.addEventListener('click', () => {
            this.analyzeFile();
        });

        // New analysis button
        newAnalysisBtn.addEventListener('click', () => {
            this.resetApp();
        });

        // Retry button
        retryBtn.addEventListener('click', () => {
            this.retryAnalysis();
        });

        // Download button
        downloadBtn.addEventListener('click', () => {
            this.downloadReport();
        });
    }

    setupDragAndDrop() {
        const uploadArea = document.getElementById('uploadArea');

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults, false);
            document.body.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                if (!this.analysisInProgress) {
                    uploadArea.classList.add('dragover');
                }
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('dragover');
            }, false);
        });

        uploadArea.addEventListener('drop', (e) => {
            if (!this.analysisInProgress) {
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.handleFileSelect(files[0]);
                }
            }
        }, false);
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    handleFileSelect(file) {
        if (!file) return;

        // Validate file type
        const allowedTypes = ['text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel', 'text/csv'];
        
        if (!allowedTypes.includes(file.type) && !this.isValidFileExtension(file.name)) {
            this.showError('Invalid file type. Please upload a PDF, XLSX, DOCX, TXT, or CSV file.');
            return;
        }

        // Validate file size (16MB max)
        if (file.size > 16 * 1024 * 1024) {
            this.showError('File too large. Maximum size allowed is 16MB.');
            return;
        }

        this.currentFile = file;
        this.showFileInfo(file);
        this.enableAnalyzeButton();
    }

    isValidFileExtension(filename) {
        const validExtensions = ['.txt', '.pdf', '.docx', '.xlsx', '.xls', '.csv'];
        const extension = filename.toLowerCase().substring(filename.lastIndexOf('.'));
        return validExtensions.includes(extension);
    }

    showFileInfo(file) {
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const uploadArea = document.getElementById('uploadArea');
        const analysisOptions = document.getElementById('analysisOptions');

        fileName.textContent = file.name;
        fileSize.textContent = this.formatFileSize(file.size);
        
        uploadArea.style.display = 'none';
        fileInfo.style.display = 'block';
        analysisOptions.style.display = 'block';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    removeFile() {
        this.currentFile = null;
        const fileInfo = document.getElementById('fileInfo');
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const analysisOptions = document.getElementById('analysisOptions');

        fileInfo.style.display = 'none';
        uploadArea.style.display = 'block';
        analysisOptions.style.display = 'none';
        fileInput.value = '';
        this.disableAnalyzeButton();
    }

    enableAnalyzeButton() {
        const analyzeBtn = document.getElementById('analyzeBtn');
        analyzeBtn.disabled = false;
    }

    disableAnalyzeButton() {
        const analyzeBtn = document.getElementById('analyzeBtn');
        analyzeBtn.disabled = true;
    }

    async analyzeFile() {
        if (!this.currentFile || this.analysisInProgress) return;

        this.analysisInProgress = true;
        this.showLoadingSection();

        const formData = new FormData();
        formData.append('file', this.currentFile);
        
        // Get selected analysis type
        const analysisType = document.querySelector('input[name="analysisType"]:checked').value;
        formData.append('analysisType', analysisType);

        try {
            // Simulate loading steps
            await this.simulateLoadingSteps();

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.showResults(result.data);
            } else {
                this.showError(result.error || 'Analysis failed. Please try again.');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.showError('Network error. Please check your connection and try again.');
        } finally {
            this.analysisInProgress = false;
        }
    }

    async simulateLoadingSteps() {
        const steps = ['step1', 'step2', 'step3', 'step4'];
        
        for (let i = 0; i < steps.length; i++) {
            await new Promise(resolve => setTimeout(resolve, 500));
            const step = document.getElementById(steps[i]);
            if (step) {
                step.classList.add('active');
            }
        }
    }

    showLoadingSection() {
        this.hideAllSections();
        const loadingSection = document.getElementById('loadingSection');
        loadingSection.style.display = 'block';

        // Reset loading steps
        const steps = document.querySelectorAll('.step');
        steps.forEach(step => step.classList.remove('active'));
        
        // Activate first step
        const firstStep = document.getElementById('step1');
        if (firstStep) {
            firstStep.classList.add('active');
        }
    }

    showResults(data) {
        this.hideAllSections();
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.style.display = 'block';

        // Populate result data
        document.getElementById('analysisId').textContent = data.analysis_id;
        document.getElementById('analysisDate').textContent = new Date(data.timestamp).toLocaleString();
        document.getElementById('resultFileName').textContent = data.filename;
        document.getElementById('resultFileType').textContent = data.file_type;
        document.getElementById('contentLength').textContent = data.content_length.toLocaleString();
        
        // Format and display analysis text with HTML rendering
        const analysisText = document.getElementById('analysisText');
        analysisText.innerHTML = data.analysis_result;

        // Store data for download
        this.currentAnalysis = data;

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    showError(message) {
        this.hideAllSections();
        const errorSection = document.getElementById('errorSection');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.innerHTML = message;
        errorSection.style.display = 'block';
        
        // Scroll to error
        errorSection.scrollIntoView({ behavior: 'smooth' });
    }

    hideAllSections() {
        const sections = ['loadingSection', 'resultsSection', 'errorSection'];
        sections.forEach(sectionId => {
            const section = document.getElementById(sectionId);
            if (section) {
                section.style.display = 'none';
            }
        });
    }

    resetApp() {
        this.removeFile();
        this.hideAllSections();
        this.currentAnalysis = null;
        this.analysisInProgress = false;

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    retryAnalysis() {
        if (this.currentFile) {
            this.analyzeFile();
        } else {
            this.resetApp();
        }
    }

    downloadReport() {
        if (!this.currentAnalysis) return;

        const { jsPDF } = window.jspdf;
        const reportElement = document.getElementById('resultsSection');
        const analysisTextElement = document.getElementById('analysisText'); // The scrollable element
        const downloadBtn = document.getElementById('downloadBtn');
        const originalBtnText = downloadBtn.innerHTML;

        // Provide visual feedback
        downloadBtn.disabled = true;
        downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating PDF...';

        // Temporarily modify styles to capture full content
        const originalMaxHeight = analysisTextElement.style.maxHeight;
        const originalOverflow = analysisTextElement.style.overflowY;
        analysisTextElement.style.maxHeight = 'none';
        analysisTextElement.style.overflowY = 'visible';

        html2canvas(reportElement, {
            scale: 2,
            useCORS: true,
            logging: false,
        }).then(canvas => {
            try {
                const imgData = canvas.toDataURL('image/png');
                const pdf = new jsPDF({
                    orientation: 'p',
                    unit: 'px',
                    format: [canvas.width, canvas.height],
                });

                pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height, undefined, 'FAST');
                const fileName = `Financial_Analysis_${this.currentAnalysis.analysis_id}.pdf`;
                pdf.save(fileName);
            } catch (error) {
                console.error("Error generating PDF:", error);
                alert("Sorry, there was an error generating the PDF. Please try again.");
            } finally {
                // Restore original styles
                analysisTextElement.style.maxHeight = originalMaxHeight;
                analysisTextElement.style.overflowY = originalOverflow;
                // Restore button state
                downloadBtn.disabled = false;
                downloadBtn.innerHTML = originalBtnText;
            }
        }).catch(err => {
            // Also restore styles on html2canvas error
            analysisTextElement.style.maxHeight = originalMaxHeight;
            analysisTextElement.style.overflowY = originalOverflow;
            downloadBtn.disabled = false;
            downloadBtn.innerHTML = originalBtnText;
            console.error("html2canvas failed:", err);
            alert("Sorry, there was an error capturing the content for the PDF.");
        });
    }

    // This function is no longer needed as we are capturing the HTML content directly.
    /*
    formatReportForDownload(data) {
        return `Financial Statement Analysis Report
========================================

Analysis ID: ${data.analysis_id}
Date: ${new Date(data.timestamp).toLocaleString()}
File: ${data.filename} (${data.file_type})
Content Length: ${data.content_length.toLocaleString()} characters

Analysis Results:
----------------
${data.analysis_result}

Generated by Financial Analysis Co-Pilot
University Project - 2024`;
    }
    */
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FinancialAnalysisApp();
});

// Service Worker Registration (for future PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then((registration) => {
                console.log('SW registered: ', registration);
            })
            .catch((registrationError) => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
