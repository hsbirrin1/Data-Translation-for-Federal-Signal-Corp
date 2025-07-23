import requests 
import pandas as pd 
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# Step 1: Configure API connection using CIK and retrieve data (Retrieve Data from the SEC API)
CIK_fss = '0000277509'  # Federal Signal Corp
headers = {'User-Agent': "hbirring@seattleu.edu"}

# Get company data from SEC Company Facts API
url = f'http://data.sec.gov/api/xbrl/companyfacts/CIK{CIK_fss.zfill(10)}.json'
companyFacts = requests.get(url, headers=headers).json()

# Step 2: Tag the data & Extract and Filter Data (Tag, Extract, and Filter Data)
def get_tag_df(tag):
    try:
        df = pd.DataFrame(companyFacts['facts']['us-gaap'][tag]['units']['USD'])
        df['end'] = pd.to_datetime(df['end'])  # convert to datetime
        df = df[df['form'] == '10-K']          # filter for 10-Ks
        return df
    except KeyError:
         # Just return empty DataFrame if data for this tag is missing
        return pd.DataFrame(columns=['accn', 'end', 'val', 'form', 'fy'])
    
# Step 3: Load financial DataFrames and filter for the last 5 years
cutoff_date = datetime.now() - timedelta(days=5*365)

#load the dataframes
revenues_df = get_tag_df('Revenues')
net_income_df = get_tag_df('NetIncomeLoss')
cost_of_revenue_df = get_tag_df('CostOfGoodsAndServicesSold')
total_assets_df = get_tag_df('Assets')
current_assets_df = get_tag_df('AssetsCurrent')
current_liabilities_df = get_tag_df('LiabilitiesCurrent')
inventory_df = get_tag_df('InventoryNet')
total_liabilities_df = get_tag_df('Liabilities')
total_equity_df = get_tag_df('StockholdersEquity')

# Sort and keep the most recent 10-K per accession number
revenues_df = revenues_df.sort_values('end').drop_duplicates('accn', keep='last')
net_income_df = net_income_df.sort_values('end').drop_duplicates('accn', keep='last')
cost_of_revenue_df = cost_of_revenue_df.sort_values('end').drop_duplicates('accn', keep='last')
total_assets_df = total_assets_df.sort_values('end').drop_duplicates('accn', keep='last')
current_assets_df = current_assets_df.sort_values('end').drop_duplicates('accn', keep='last')
current_liabilities_df = current_liabilities_df.sort_values('end').drop_duplicates('accn', keep='last')
inventory_df = inventory_df.sort_values('end').drop_duplicates('accn', keep='last')
total_liabilities_df = total_liabilities_df.sort_values('end').drop_duplicates('accn', keep='last')
total_equity_df = total_equity_df.sort_values('end').drop_duplicates('accn', keep='last')

# Apply 5-year cutoff on 'end' date
revenues_df = revenues_df[revenues_df['end'] >= cutoff_date]
net_income_df = net_income_df[net_income_df['end'] >= cutoff_date]
cost_of_revenue_df = cost_of_revenue_df[cost_of_revenue_df['end'] >= cutoff_date]
total_assets_df = total_assets_df[total_assets_df['end'] >= cutoff_date]
current_assets_df = current_assets_df[current_assets_df['end'] >= cutoff_date]
current_liabilities_df = current_liabilities_df[current_liabilities_df['end'] >= cutoff_date]
inventory_df = inventory_df[inventory_df['end'] >= cutoff_date]
total_liabilities_df = total_liabilities_df[total_liabilities_df['end'] >= cutoff_date]
total_equity_df = total_equity_df[total_equity_df['end'] >= cutoff_date]

# Step 4 Merge DataFrames on 'accn' and 'end'
# Start from required financials
df = revenues_df[['accn', 'end', 'val']].rename(columns={'val': 'revenue'})
df = df.merge(net_income_df[['accn', 'end', 'val']].rename(columns={'val': 'net_income'}), on=['accn', 'end'], how='inner')
df = df.merge(cost_of_revenue_df[['accn', 'end', 'val']].rename(columns={'val': 'cost_of_revenue'}), on=['accn', 'end'], how='inner')
df = df.merge(total_assets_df[['accn', 'end', 'val']].rename(columns={'val': 'total_assets'}), on=['accn','end'], how='left')
df = df.merge(current_assets_df[['accn', 'end', 'val']].rename(columns={'val': 'current_assets'}), on=['accn','end'], how='left')
df = df.merge(current_liabilities_df[['accn', 'end', 'val']].rename(columns={'val': 'current_liabilities'}), on=['accn','end'], how='left')
df = df.merge(inventory_df[['accn', 'end', 'val']].rename(columns={'val': 'inventory'}), on=['accn','end'], how='left')
df = df.merge(total_liabilities_df[['accn', 'end', 'val']].rename(columns={'val': 'total_liabilities'}), on=['accn','end'], how='left')
df = df.merge(total_equity_df[['accn', 'end', 'val']].rename(columns={'val': 'total_equity'}), on=['accn','end'], how='left')

# Step 5: Calculate Financial Ratios

# Calculate gross profit (Revenue - Cost of Revenue)
df['gross_profit'] = df['revenue'] - df['cost_of_revenue']

# Calculate gross profit margin: shows percent of revenue left after cost of goods sold
# Formula: (Revenue - Cost of Revenue) / Revenue
df['gross_profit_margin'] = df['gross_profit'] / df['revenue'] 

# Calculate net profit margin: shows percent of revenue that is net income
# Formula: Net Income / Revenue
df['net_profit_margin'] = df['net_income'] / df['revenue']

# Calculate quick assets for liquidity ratios
# Formula: Current Assets - Inventory
df['quick_assets'] = df['current_assets'] - df['inventory']

# Calculate current ratio: ability to cover short-term obligations
# Formula: Current Assets / Current Liabilities
df['current_ratio'] = df['current_assets'] / df['current_liabilities']

# Calculate quick ratio: stricter test of liquidity (excludes inventory)
# Formula: (Current Assets - Inventory) / Current Liabilities
df['quick_ratio'] = df['quick_assets'] / df['current_liabilities']

# Calculate debt to equity ratio: degree of financial leverage
# Formula: Total Liabilities / Total Equity
df['debt_to_equity'] = df['total_liabilities'] / df['total_equity']

# Calculate return on equity (ROE): profitability for shareholders
# Formula: Net Income / Total Equity
df['roe'] = df['net_income'] / df['total_equity']

# Calculate return on assets (ROA): efficiency using assets
# Formula: Net Income / Total Assets
df['roa'] = df['net_income'] / df['total_assets']


# Step 6: Print Results
# Set display options to show all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

# Select and rename columns
output_df = df[['end', 'revenue', 'net_income', 'cost_of_revenue', 'gross_profit', 
                'gross_profit_margin', 'net_profit_margin', 
                'current_assets', 'current_liabilities', 'inventory',
                'current_ratio', 'quick_ratio', 'debt_to_equity', 'roe', 'roa']].copy()

output_df.columns = [
    'Year-End', 'Revenue', 'Net Income', 'Cost of Revenue', 'Gross Profit',
    'Gross Margin', 'Net Margin', 'Current Assets', 'Current Liabilities', 'Inventory',
    'Current Ratio', 'Quick Ratio', 'Debt/Equity', 'ROE', 'ROA'
]

print(output_df)

# Step 7: Visualize Key Financial Ratios

# Sort the data by end date
df = df.sort_values('end')

# Define the ratios you want to plot
ratios = {
    'gross_profit_margin': 'Gross Profit Margin',
    'net_profit_margin': 'Net Profit Margin',
    'current_ratio': 'Current Ratio',
    'quick_ratio': 'Quick Ratio',
    'debt_to_equity': 'Debt-to-Equity Ratio',
    'roe': 'Return on Equity (ROE)',
    'roa': 'Return on Assets (ROA)'
}

# Plot each ratio in its own figure
for column, title in ratios.items():
    plt.figure(figsize=(10, 6))
    plt.plot(df['end'], df[column], marker='o')
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(title)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
