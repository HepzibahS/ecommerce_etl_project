import pandas as pd
import os

# Set data directory path
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# Load raw CSVs
products_df = pd.read_csv(os.path.join(data_dir, 'products.csv'))
customers_df = pd.read_csv(os.path.join(data_dir, 'customers.csv'))
sales_df = pd.read_csv(os.path.join(data_dir, 'sales.csv'))

# --- Data Cleaning ---
# Normalize column names
def normalize_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

# Strip white spaces in string fields
def strip_strings(df):
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    return df

# Apply normalization and stripping
products_df = strip_strings(normalize_columns(products_df))
customers_df = strip_strings(normalize_columns(customers_df))
sales_df = strip_strings(normalize_columns(sales_df))

# Clean 'payment_type' if it exists
if 'payment_mode' in sales_df.columns:
    sales_df['payment_mode'] = sales_df['payment_mode'].str.title().replace({
        'Credit': 'Credit Card',
        'Cc': 'Credit Card',
        'Creditcard': 'Credit Card',
        'Debit': 'Debit Card',
        'Cash': 'Cash',
        'Upi': 'UPI',
        'Wallet': 'Wallet'
    })
else:
    print("⚠️ Warning: 'payment_type' column not found in sales_df")


# Fill missing payment_type
sales_df['payment_mode'] = sales_df['payment_mode'].fillna('Unknown')

# Standardize product category title case
if 'category' in products_df.columns:
    products_df['category'] = products_df['category'].str.title()

# --- Data Joins and Merges ---
sales_product_df = pd.merge(sales_df, products_df, on='product_id', how='left')
final_df = pd.merge(sales_product_df, customers_df, on='customer_id', how='left')

# print("Columns in final_df:", final_df.columns.tolist())
# print(final_df.head())


# --- Calculated Fields ---
if 'quantity' in final_df.columns and 'unit_price' in final_df.columns:
    final_df['total_price'] = final_df['quantity'] * final_df['unit_price']

if 'first_name' in final_df.columns and 'last_name' in final_df.columns:
    final_df['customer_full_name'] = final_df['first_name'].str.title() + ' ' + final_df['last_name'].str.title()

# --- Date Handling ---
if 'sale_date' in final_df.columns:
    final_df['sale_date'] = pd.to_datetime(final_df['sale_date'], errors='coerce')
    final_df['sale_year'] = final_df['sale_date'].dt.year
    final_df['sale_month'] = final_df['sale_date'].dt.month
    final_df['day_of_sale'] = final_df['sale_date'].dt.day

# --- Aggregation: Monthly Summary ---
# final_df['profit'] = final_df['total_price'] - final_df['cost_price']

monthly_summary = final_df.groupby(['sale_year', 'sale_month']).agg({
    'total_price': 'sum',
    # 'profit': 'sum'
}).reset_index()

# Output the summary
print("\nMonthly Sales Summary:")
print(monthly_summary)

#remove duplicates
final_df=final_df.drop_duplicates()
final_df=final_df.drop_duplicates(subset=['sale_id','customer_id','product_id'],keep='first')

# Sort by date for time-series operations
final_df = final_df.sort_values(by='sale_date')

# Rolling 3-month average sales (based on sale date)
monthly_summary['rolling_3mo_avg_sales'] = monthly_summary['total_price'].rolling(window=3, min_periods=1).mean()

# # Rank of months by profit (within each year)
# monthly_summary['monthly_profit_rank'] = monthly_summary.groupby('sale_year')['profit'].rank(ascending=False, method='dense')

print("\nMonthly Summary with Advanced Metrics:")
print(monthly_summary)

