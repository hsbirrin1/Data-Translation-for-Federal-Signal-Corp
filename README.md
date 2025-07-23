# Data-Translation-for-Federal-Signal-Corp

This project is a Python-based tool that pulls and analyzes financial data for Federal Signal Corporation (CIK: 0000277509) using the SEC’s API. It focuses on gathering key financial information from the company’s 10-K annual reports over the last 5 years, and then calculating several important financial ratios. These ratios help give insight into the company's profitability, liquidity, efficiency, and financial health.

The script works by first connecting to the SEC’s EDGAR database using the company’s unique identifier (CIK). It then pulls detailed financial figures like revenue, net income, total assets, liabilities, inventory, and more. Once the data is collected, it is cleaned and filtered to ensure only the most recent and relevant yearly data is used.

From this data, I calculated useful financial ratios including gross profit margin, net profit margin, return on assets (ROA), return on equity (ROE), the current ratio, quick ratio, and the debt-to-equity ratio. These metrics can help you better understand how well a company is managing its operations, paying down debt, or returning profits to shareholders.

Once the metrics are calculated, the it prints out a clean table showing the raw numbers and ratios by year. It also generates visual graphs for each ratio so you can quickly spot any trends or performance changes over time. These graphs are helpful for spotting things like improving profitability, growing efficiency, or increasing financial risk.

I have used standard Python libraries: pandas, matplotlib, and requests.
