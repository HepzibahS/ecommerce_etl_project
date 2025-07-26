import pandas as pd
import os

# Define file paths (adjust if needed)
DATA_DIR = "../data"
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.csv")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.csv")
SALES_FILE = os.path.join(DATA_DIR, "sales.csv")

def extract_products():
    try:
        products_df = pd.read_csv(PRODUCTS_FILE)
        print(f"[✓] Loaded {len(products_df)} products.")
        return products_df
    except Exception as e:
        print(f"[!] Error loading products: {e}")
        return pd.DataFrame()

def extract_customers():
    try:
        customers_df = pd.read_csv(CUSTOMERS_FILE)
        print(f"[✓] Loaded {len(customers_df)} customers.")
        return customers_df
    except Exception as e:
        print(f"[!] Error loading customers: {e}")
        return pd.DataFrame()

def extract_sales():
    try:
        sales_df = pd.read_csv(SALES_FILE)
        print(f"[✓] Loaded {len(sales_df)} sales records.")
        return sales_df
    except Exception as e:
        print(f"[!] Error loading sales: {e}")
        return pd.DataFrame()

# Optional: Test run
if __name__ == "__main__":
    extract_products()
    extract_customers()
    extract_sales()
