import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Dataset with openpyxl engine
df = pd.read_excel('Sample data (1).xlsx', engine='openpyxl')

# Clean column headers by stripping trailing/leading spaces
df.columns = df.columns.str.strip()

# 2. Compute Executive Key Performance Indicators
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_units = df['Units Sold'].sum()
overall_margin = (total_profit / total_sales) * 100

print("==========================================")
print("       EXECUTIVE KPI SUMMARY             ")
print("==========================================")
print(f"Total Net Sales:       ${total_sales:,.2f}")
print(f"Total Net Profit:      ${total_profit:,.2f}")
print(f"Total Units Sold:      {total_units:,.0f} units")
print(f"Overall Profit Margin: {overall_margin:.2f}%\n")

# 3. Breakdown by Business Segment
segment_summary = df.groupby('Segment')[['Sales', 'Profit', 'Units Sold']].sum().reset_index()
segment_summary['Profit Margin (%)'] = (segment_summary['Profit'] / segment_summary['Sales']) * 100
segment_summary = segment_summary.sort_values(by='Sales', ascending=False)

print("==========================================")
print("    PERFORMANCE BY BUSINESS SEGMENT      ")
print("==========================================")
print(segment_summary.to_string(index=False))
print("\n")

# 4. Save Cleaned Dataset for Power BI / Tableau Import
df.to_csv('cleaned_financial_sample.csv', index=False)
print("Success! Cleaned dataset exported as 'cleaned_financial_sample.csv'.")

# 5. Generate Visual Charts
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(15, 11))

fig.suptitle('Global Financial Performance & Executive Summary Dashboard', fontsize=16, fontweight='bold')

# Chart 1: Net Sales by Segment
sns.barplot(ax=axes[0, 0], data=segment_summary, x='Segment', y='Sales', palette='Blues_d')
axes[0, 0].set_title('Net Sales by Business Segment', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Sales ($)', fontsize=10)
axes[0, 0].tick_params(axis='x', rotation=15)
for p in axes[0, 0].patches:
    axes[0, 0].annotate(f"${p.get_height()/1e6:.1f}M", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

# Chart 2: Net Profit / Loss by Segment
colors = ['green' if val > 0 else 'red' for val in segment_summary['Profit']]
sns.barplot(ax=axes[0, 1], data=segment_summary, x='Segment', y='Profit', palette=colors)
axes[0, 1].set_title('Net Profit / (Loss) by Business Segment', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Profit ($)', fontsize=10)
axes[0, 1].tick_params(axis='x', rotation=15)
axes[0, 1].axhline(0, color='black', linewidth=0.8)
for p in axes[0, 1].patches:
    val = p.get_height()
    axes[0, 1].annotate(f"${val/1e6:.2f}M", (p.get_x() + p.get_width() / 2., val if val > 0 else val - 0.5e6),
                        ha='center', va='bottom' if val > 0 else 'top', fontsize=9)

# Chart 3: Net Sales by Country
country_summary = df.groupby('Country')[['Sales']].sum().reset_index().sort_values(by='Sales', ascending=False)
sns.barplot(ax=axes[1, 0], data=country_summary, x='Country', y='Sales', palette='Greens_d')
axes[1, 0].set_title('Net Sales by Country', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Sales ($)', fontsize=10)
axes[1, 0].tick_params(axis='x', rotation=15)
for p in axes[1, 0].patches:
    axes[1, 0].annotate(f"${p.get_height()/1e6:.1f}M", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

# Chart 4: Net Sales by Product Line
product_summary = df.groupby('Product')[['Sales']].sum().reset_index().sort_values(by='Sales', ascending=False)
sns.barplot(ax=axes[1, 1], data=product_summary, x='Product', y='Sales', palette='Purples_d')
axes[1, 1].set_title('Net Sales by Product Line', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Sales ($)', fontsize=10)
axes[1, 1].tick_params(axis='x', rotation=15)
for p in axes[1, 1].patches:
    axes[1, 1].annotate(f"${p.get_height()/1e6:.1f}M", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()