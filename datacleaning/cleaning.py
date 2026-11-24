import os
import pandas as pd

# --- CONFIGURATION ---
BASE_DATASET_DIR = r"E:/Avishkar/datasets"
OUTPUT_MASTER_FILE = os.path.join(BASE_DATASET_DIR, "merged_master_trade_data2.csv")

# Columns we want to keep and rename from raw Comtrade data
KEEP_COLUMNS = {
    'refYear': 'Year',
    'refMonth': 'Month',
    'cmdCode': 'HS_Code',
    'partnerCode': 'CountryCode',
    'partnerDesc': 'Country',
    'cmdDesc': 'Commodity',
    'primaryValue': 'Trade_Value_USD',
    'netWgt':'Weight'
}

all_dataframes = []

print("Scanning directories for CSV files...")

# --- 1. LOOP THROUGH ALL FOLDERS AND CLEAN DATA ---
# os.walk all commodity folders
for root, dirs, files in os.walk(BASE_DATASET_DIR):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)
            print(f" -> Processing: {file}")
            
            try:
                # Read raw CSV
                df = pd.read_csv(file_path, index_col=False, low_memory=False)
                
                # only isolate Import data ('M')
                if 'flowCode' in df.columns:
                    df = df[df['flowCode'] == 'M']
                
                #Remove invalid global aggregates or null partners
                if 'partnerCode' in df.columns:
                    df = df[df['partnerCode'] != 0]
                if 'partnerDesc' in df.columns:
                    df = df[df['partnerDesc'].str.lower() != 'world']
                
                # Keep and rename only the columns relevant to Database
                existing_cols = {k: v for k, v in KEEP_COLUMNS.items() if k in df.columns}
                df = df[list(existing_cols.keys())].rename(columns=existing_cols)
                
                # Standardize data types
                if 'Trade_Value_USD' in df.columns:
                    df['Trade_Value_USD'] = pd.to_numeric(df['Trade_Value_USD'], errors='coerce').fillna(0.0)
                    df = df[df['Trade_Value_USD'] > 0]
                
                if 'HS_Code' in df.columns:
                    df['HS_Code'] = df['HS_Code'].astype(str)

                if 'Weight' in df.columns:
                    df['Weight'] = df['Weight'].fillna(0)
                # Append valid data chunk to our master list
                if not df.empty:
                    all_dataframes.append(df)
                    
            except Exception as e:
                print(f"[ERROR] Could not parse file {file}: {e}")

# --- 2. CONSOLIDATE AND CALCULATE SHARES ---
if all_dataframes:
    print("\nMerging files and calculating market share percentages...")
    # Combine all individual years and commodities together
    master_df = pd.concat(all_dataframes, ignore_index=True)
    
    master_df.to_csv(OUTPUT_MASTER_FILE, index=False)
    print(f"\nSuccess! Consolidated master dataset saved to: {OUTPUT_MASTER_FILE}")
    print(f"Total entries ready for Neo4j injection: {len(master_df)}")
else:
    print("\nNo valid CSV files were processed. Check your file paths.")
