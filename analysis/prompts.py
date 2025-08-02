"""
Prompt templates for Financial Analysis Co-Pilot
Contains prompts for a two-step 10-K analysis process.
"""

# ======================================================================================
# STEP 1 PROMPT: Locate the beginning of the financial statements in a 10-K report
# ======================================================================================

LOCATE_FINANCIALS_PROMPT = """
You are an expert document analyst. Your task is to find the beginning of the core financial statements section in this 10-K report.
The financial statements almost always begin with one of the following exact phrases (case-insensitive). Find the FIRST occurrence of any of these headers:

- "consolidated balance sheets"
- "consolidated statements of financial position"
- "consolidated statements of income"
- "consolidated statements of earnings"
- "consolidated statements of operations"
- "consolidated statements of comprehensive income"
- "consolidated statements of cash flows"
- "report of independent registered public accounting firm"

**Instructions:**
1.  Read the entire document provided below.
2.  Find the line that contains the **first occurrence** of any of the headers listed above.
3.  Return the **ENTIRE text of the document starting from that line**. Do not omit anything.
4.  If none of these headers are found, return the text "FINANCIAL_STATEMENTS_NOT_FOUND".

**DOCUMENT TEXT:**
---
{report_text}
---
"""

# ======================================================================================
# STEP 2 PROMPT: Analyze the extracted financial statements with improved formatting
# ======================================================================================

TEN_K_ANALYSIS_PROMPT = """
You are a top-tier financial analyst AI. Your task is to deliver a professional, clear, and visually appealing analysis of the provided financial statements.

**OUTPUT INSTRUCTIONS:**
- **Structure:** Present the entire analysis using self-contained HTML cards.
- **Styling:** Use the provided CSS classes (`analysis-card`, `card-header`, `card-body`, `kpi-grid`, `kpi-item`).
- **Clarity:** Be concise. Use bullet points (`<li>`) for lists and `<br>` for line breaks inside paragraphs. Avoid large empty spaces.

---

### Analysis Output BEGIN ###

<div class="analysis-card">
  <div class="card-header">
    <i class="fas fa-file-invoice-dollar"></i> Key Financial Data
  </div>
  <div class="card-body">
    <p>Extracted from the most recent fiscal year. All figures are as reported in the document.</p>
    <ul>
      <li><strong>Total Revenue:</strong> [Scour the text for Total Revenue or Net Sales, and place it here. If not found, state "Not Found".]</li>
      <li><strong>Cost of Revenue:</strong> [Find Cost of Revenue or Cost of Sales. If not found, state "Not Found".]</li>
      <li><strong>Gross Profit:</strong> [Calculate or find Gross Profit. If not found, state "Not Found".]</li>
      <li><strong>Operating Income:</strong> [Find Operating Income or Income from Operations. If not found, state "Not Found".]</li>
      <li><strong>Net Income:</strong> [Find Net Income or Net Earnings. If not found, state "Not Found".]</li>
      <li><strong>Cash from Operating Activities:</strong> [Find Net Cash from Operating Activities. If not found, state "Not Found".]</li>
    </ul>
  </div>
</div>

<div class="analysis-card">
  <div class="card-header">
    <i class="fas fa-balance-scale"></i> Balance Sheet Summary
  </div>
  <div class="card-body">
    <div class="kpi-grid">
      <div class="kpi-item">
        <strong>Total Assets</strong>
        <span>[Find Total Assets. If not found, state "N/A".]</span>
      </div>
      <div class="kpi-item">
        <strong>Total Liabilities</strong>
        <span>[Find Total Liabilities. If not found, state "N/A".]</span>
      </div>
      <div class="kpi-item">
        <strong>Total Equity</strong>
        <span>[Find Total Equity. If not found, state "N/A".]</span>
      </div>
    </div>
  </div>
</div>

<div class="analysis-card">
  <div class="card-header">
    <i class="fas fa-chart-pie"></i> Key Financial Ratios
  </div>
  <div class="card-body">
    <p>Calculated using the extracted data. Ratios provide insight into the company's performance.</p>
    <ul>
      <li><strong>Gross Profit Margin:</strong> [Calculate (Gross Profit / Total Revenue) * 100%. Show calculation: "(X / Y) * 100% = Z%". If data is missing, state "Cannot be calculated.".]</li>
      <li><strong>Net Profit Margin:</strong> [Calculate (Net Income / Total Revenue) * 100%. Show calculation. If data is missing, state "Cannot be calculated.".]</li>
      <li><strong>Return on Assets (ROA):</strong> [Calculate (Net Income / Total Assets) * 100%. Show calculation. If data is missing, state "Cannot be calculated.".]</li>
      <li><strong>Return on Equity (ROE):</strong> [Calculate (Net Income / Total Equity) * 100%. Show calculation. If data is missing, state "Cannot be calculated.".]</li>
      <li><strong>Debt-to-Equity Ratio:</strong> [Calculate Total Liabilities / Total Equity. Show calculation. If data is missing, state "Cannot be calculated.".]</li>
    </ul>
  </div>
</div>

<div class="analysis-card">
  <div class="card-header">
    <i class="fas fa-lightbulb"></i> Executive-Level Analysis
  </div>
  <div class="card-body">
    <p><strong>Profitability:</strong><br>[Analyze the company's profitability based on the margins. Is it strong, weak, or average for its industry? Use `<em>` for emphasis.]</p>
    <p><strong>Financial Health:</strong><br>[Assess the balance sheet. Does the Debt-to-Equity ratio indicate high leverage? What does ROA suggest about asset efficiency?]</p>
    <p><strong>Potential Red Flags:</strong><br>[Identify 1-2 potential concerns. Examples: negative cash flow, declining margins, or very high debt levels.]</p>
  </div>
</div>

### Analysis Output END ###

---

**FINANCIAL STATEMENTS TEXT TO ANALYZE:**
{report_text}
"""

# ======================================================================================
# GENERAL PURPOSE PROMPT (For non-10K or simple analysis)
# ======================================================================================

FINANCIAL_ANALYSIS_PROMPT = """
You are a senior financial analyst. Please provide a clear and concise analysis of the following financial report text.

**Key areas to focus on:**
1.  **Financial Health:** Identify key metrics like revenue, net income, and margins.
2.  **Profitability:** Assess the company's ability to generate profit.
3.  **Potential Risks:** Highlight any risks or concerns mentioned in the text.
4.  **Overall Summary:** Provide a brief executive summary of the report's findings.

Use HTML formatting (`<strong>`, `<ul>`, `<li>`, `<br>`) to structure your response.

**FINANCIAL REPORT TEXT:**
---
{report_text}
---
"""
