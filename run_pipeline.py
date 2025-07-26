# run_pipeline.py

from scripts.transform import final_df, customers_df, products_df, sales_df
from scripts.load import run_pipeline

run_pipeline(final_df, customers_df, products_df, sales_df)
