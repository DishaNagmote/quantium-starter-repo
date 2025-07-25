import pandas as pd
import glob
import os

# Define the path where CSV files are stored
data_folder = "data/"

# Collect all CSV files
csv_files = glob.glob(os.path.join(data_folder, "*.csv"))

# Read all files and concatenate them into a single DataFrame
all_data = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

# Convert price and quantity columns to numeric types
all_data['price'] = pd.to_numeric(all_data['price'], errors='coerce')
all_data['quantity'] = pd.to_numeric(all_data['quantity'], errors='coerce')

# Filter the DataFrame for product = pink_morsel
filtered_df = all_data[all_data['product'] == "pink_morsel"].copy()

# Create a new 'sales' column
filtered_df["sales"] = filtered_df["quantity"] * filtered_df["price"]

# Optional: Remove any rows with missing data (NaN)
filtered_df = filtered_df.dropna(subset=["sales"])

# Save the filtered and processed data to a new CSV
filtered_df.to_csv("pink_morsel_sales.csv", index=False)

print("✅ Data processed and saved to pink_morsel_sales.csv")
