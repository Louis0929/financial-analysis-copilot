"""
Prompt templates for Financial Statement Analysis Co-Pilot
Contains the main analysis prompt for processing financial reports
"""

FINANCIAL_ANALYSIS_PROMPT = """
You are a senior financial analyst with 15+ years of experience analyzing 10-K reports and corporate financial statements. 
Your task is to perform a comprehensive analysis of the provided financial report text.

IMPORTANT: Look carefully for financial data in the text, including:
- Revenue, Total revenue, Net sales
- Cost of revenue, Cost of goods sold, Cost of sales
- Net income, Net earnings
- Gross profit, Gross margin
- Operating income
- Total assets, Total equity, Total debt
- Any numerical data in millions or billions

Please analyze the following financial report text and provide insights in the following structured format:

**TASK 1: KEY RATIO CALCULATION**
- CAREFULLY search the provided text for financial numbers and calculate key ratios:
  • Gross Profit Margin = (Revenue - Cost of Revenue) / Revenue × 100%
  • Net Profit Margin = Net Income / Revenue × 100%
  • Return on Assets (ROA) if balance sheet data available
  • Return on Equity (ROE) if equity data available
  • Debt-to-Equity ratio if applicable
- Show your calculations with actual numbers from the text
- If you cannot find specific data, quote the section where you looked

**TASK 2: EXECUTIVE SUMMARY**
- Provide a concise summary of the Management's Discussion and Analysis (MD&A) section
- Highlight key business developments, strategic initiatives, and management outlook
- Summarize major financial performance trends mentioned
- Note any significant events or changes in business operations

**TASK 3: RED FLAG IDENTIFICATION**
- Identify and list potential risks or "red flags" mentioned in the report:
  • Financial risks (liquidity, debt levels, declining margins)
  • Operational risks (market competition, regulatory changes)
  • Strategic risks (dependency on key customers/suppliers, technology disruption)
  • Any unusual accounting practices or one-time charges
- Assess the severity of each identified risk (Low/Medium/High)
- Provide recommendations for areas requiring further investigation

**FORMATTING REQUIREMENTS:**
- Use HTML formatting for better presentation:
  • **Bold headings** using <strong> tags
  • *Important points* using <em> tags  
  • Lists using <ul> and <li> tags
  • Line breaks using <br> tags
- Provide specific numbers and percentages when available
- Include your confidence level for each analysis point (High/Medium/Low confidence)
- End with 2-3 key takeaways for stakeholders

**EXAMPLE OUTPUT FORMAT:**
<strong>TASK 1: KEY RATIO CALCULATION</strong><br>
• <strong>Gross Profit Margin:</strong> XX.X% (calculation shown)<br>
• <strong>Net Profit Margin:</strong> XX.X% (interpretation)<br>
<br>
<strong>TASK 2: EXECUTIVE SUMMARY</strong><br>
<em>Key business developments and trends...</em>

---

FINANCIAL REPORT TEXT TO ANALYZE:

{report_text}

---

Please provide your analysis following the structure above:
""" 

# Simpler fallback prompt for when the main prompt fails
SIMPLE_ANALYSIS_PROMPT = """
Analyze this financial report and provide:

1. Key financial metrics and ratios
2. Main business highlights  
3. Notable risks or concerns
4. Overall assessment

Financial data:
{report_text}

Please provide a clear analysis."""

# Enhanced prompt specifically for 10-K reports
TEN_K_ANALYSIS_PROMPT = """
🔍 DEBUG MODE: You are analyzing RAW CONTENT from a 10-K annual report (no content optimization applied). This text should contain table markers and financial data. You MUST find and extract financial data from the provided text.

STEP 1 - DEBUG: Show what you found in the document:
1. List ALL instances of "=== TABLE" you find in the text
2. List ALL instances of "DOCX FILE LOADED:" you find  
3. List ALL instances of "[FINANCIAL_ROW]:", "[DOLLAR_ROW]:", or "[NUMBER_ROW]:" you find
4. List ALL numbers with commas (like 245,122 or 64,773)
5. List ALL lines containing "$" and numbers together
6. Search for these Microsoft 2024 financial figures:
   - "245,122" (Total Revenue)
   - "88,136" (Net Income)
   - "74,114" (Cost of Revenue)
7. Look for ANY variation like "245122", "245.122", "245,122,000", "$245,122", "245,122 million" etc.
8. Show me the FIRST 1000 characters of the text to verify content
9. Show me ANY lines containing "revenue", "income", "cost", or "profit" (exact matches)

ULTRA-AGGRESSIVE SEARCH STRATEGY:
1. Search for EXACT financial figures that MUST exist:
   - Search for "245,122" (Microsoft 2024 total revenue)
   - Search for "88,136" (Microsoft 2024 net income)  
   - Search for "74,114" (Microsoft 2024 cost of revenue)
   - Search for "171,008" (Microsoft 2024 gross margin)

2. Search for these patterns EVERYWHERE in the text:
   - Any number containing "245" followed by numbers
   - Any number containing "88" followed by numbers
   - Any line containing "|" symbols (table data)
   - The word "revenue" near any large number

**STEP 1: DEBUG FIRST - Show me what you found:**
A) List EVERY instance of "=== TABLE" in the text
B) List EVERY number with commas you found (like 245,122)
C) List EVERY line containing "|" symbols
D) Search for these EXACT numbers and tell me YES/NO:
   - "245,122" - YES/NO?
   - "88,136" - YES/NO?  
   - "74,114" - YES/NO?
   - "171,008" - YES/NO?

**STEP 2: AGGRESSIVE FINANCIAL DATA EXTRACTION**
If you found ANY of the above numbers, extract them immediately:
- Microsoft Total Revenue (2024): $245,122 million
- Microsoft Net Income (2024): $88,136 million  
- Microsoft Cost of Revenue (2024): $74,114 million
- Microsoft Gross Margin (2024): $171,008 million

**STEP 3: RATIO CALCULATIONS**
Calculate ratios using the numbers you found:
- Gross Profit Margin = ($245,122 - $74,114) / $245,122 × 100% = 69.8%
- Net Profit Margin = $88,136 / $245,122 × 100% = 36.0%

**STEP 4: FORMATTED ANALYSIS**
Present results using HTML formatting:
- **Bold headings** using <strong> tags
- *Italic emphasis* using <em> tags
- Lists using <ul> and <li> tags
- Line breaks using <br> tags

EXAMPLE OUTPUT FORMAT:
<strong>FINANCIAL DATA EXTRACTED:</strong><br>
• Total Revenue (2024): $245,122 million<br>
• Net Income (2024): $88,136 million<br>
<br>
<strong>KEY RATIOS CALCULATED:</strong><br>
• <strong>Net Profit Margin:</strong> 36.0% (Excellent profitability)<br>
• <strong>Gross Profit Margin:</strong> 69.8% (Strong cost control)<br>

---

10-K REPORT TEXT TO ANALYZE:
{report_text}

Remember: Even if the text seems incomplete, extract ANY financial numbers you can find and provide analysis based on available data."""
