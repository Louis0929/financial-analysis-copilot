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
# STEP 2 PROMPT: Analyze the extracted financial statements
# ======================================================================================

TEN_K_ANALYSIS_PROMPT = """
You are a senior financial analyst with 20+ years of experience. You have been given the financial statements section of a 10-K report.
Your task is to conduct a thorough analysis based ONLY on the provided text.

**TASK 1: EXTRACT KEY FINANCIAL DATA**
- Scour the text for the following figures for the most recent fiscal year.
- Present the extracted data clearly. If a figure is not found, state that explicitly.
  - **Total Revenue** (or Net Sales)
  - **Cost of Revenue** (or Cost of Sales)
  - **Gross Profit**
  - **Operating Income**
  - **Net Income** (or Net Earnings)
  - **Total Assets**
  - **Total Liabilities**
  - **Total Equity**
  - **Cash and Cash Equivalents**
  - **Net Cash from Operating Activities**

**TASK 2: CALCULATE KEY FINANCIAL RATIOS**
- Using the data you extracted in TASK 1, calculate the following ratios.
- Show your calculations. If data is missing for a ratio, state that it cannot be calculated.
  - **Gross Profit Margin** = (Gross Profit / Total Revenue) * 100%
  - **Net Profit Margin** = (Net Income / Total Revenue) * 100%
  - **Return on Assets (ROA)** = (Net Income / Total Assets) * 100%
  - **Return on Equity (ROE)** = (Net Income / Total Equity) * 100%
  - **Debt-to-Equity Ratio** = Total Liabilities / Total Equity

**TASK 3: PROVIDE AN EXECUTIVE-LEVEL ANALYSIS**
- Based on your findings, provide a concise analysis.
- What do the ratios tell you about the company's profitability, operational efficiency, and financial health?
- Highlight any standout numbers or trends (e.g., significant year-over-year changes if data is available).
- Identify 1-2 potential red flags or areas for further investigation based on the numbers.

**FORMATTING REQUIREMENTS:**
- Use HTML formatting: `<strong>`, `<em>`, `<ul>`, `<li>`, `<br>`.
- Present the analysis in a clear, structured way, following the three tasks above.
- Be professional and direct in your language.

**FINANCIAL STATEMENTS TEXT TO ANALYZE:**
---
{report_text}
---
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
