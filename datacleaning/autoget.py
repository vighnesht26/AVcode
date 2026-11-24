import os
import time
import requests

# --- CONFIGURATION ---
# Define the mapping between your custom subfolders and the exact HS Commodity codes
COMMODITY_MAPPING = {
    "NG2711" :"2711",
    "solidf2701": "2701",   
    "ele85": "85",
    "nu84" : "84",
   
    "premetal71":"71",
    "orgchem29":"29",
    "plasPolymer39":"39",
    "inorganic28":"28",
    "fertilizers31":"31",
    "festeel72":"72",
    "vehicles87":"87",
    "vegeanioil15":"15",
    "ediblevegoil07":"07"
    
         
}


BASE_TARGET_DIR = r"E:/Avishkar/datasets"
API_BASE_URL = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

HEADERS = {
    'Ocp-Apim-Subscription-Key': 'b093b6f11d476134bbbd5a4e66585f2b'
}



yearly_periods = {}
for year in range(2011, 2026):
    months = [f"{year}{month:02d}" for month in range(1, 13)]
    yearly_periods[year] = ",".join(months)

# --- EXECUTION LOOP ---
for folder_name, cmd_code in COMMODITY_MAPPING.items():
    commodity_dir = os.path.join(BASE_TARGET_DIR, folder_name)
    if not os.path.exists(commodity_dir):
        os.makedirs(commodity_dir)
        
    print(f"\n=== Starting download loop for Commodity: {cmd_code} into folder: {folder_name} ===")

    for year, period_string in yearly_periods.items():
        custom_file_name = f"TradeData_{cmd_code}_{year}.csv"
        full_save_path = os.path.join(commodity_dir, custom_file_name)
        
        # Build payload dynamically per iteration
        query_parameters = {
            'period': period_string,
            'reporterCode': '699',     # India
            'flowCode': 'M',          
            'cmdCode': cmd_code,
            'customsCode': 'C00',
            'motCode': '0',
            'partner2Code': '0',
            'breakdownMode': 'classic',
            'includeDesc': 'True',
            'format': 'csv' 
        }
        
        print(f" -> Pulling data for year {year}...")
        
        try:
            api_response = requests.get(API_BASE_URL, params=query_parameters, headers=HEADERS, timeout=30)
            
            if api_response.status_code == 200:
                with open(full_save_path, "wb") as csv_file:
                    csv_file.write(api_response.content)
                print(f"    Success: Saved to {custom_file_name}")
            else:
                print(f"    API Error [{api_response.status_code}] for year {year}. Skipping.")
                
        except requests.exceptions.RequestException as e:
            print(f"    Network Connection Error for year {year}: {e}")
            
        
        time.sleep(2)

print("\nAll commodity downloads processed completely!")
