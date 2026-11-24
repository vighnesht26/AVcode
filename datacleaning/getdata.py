

import os
import requests

# 1. Choose your custom storage paths

TARGET_DIR = r"E:/Avishkar/datasets/NG2711"  
FILE_NAME = "TradeData_2711_201.csv"
FULL_PATH = os.path.join(TARGET_DIR, FILE_NAME)

# 2. Base API string (without parameters)
api_base_url = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

# 3. Mirroring the exact parameters from your URL string
query_parameters = {
    'period': '201701,201702,201703,201704,201705,201706,201707,201708,201709,201710,201711,201712',
    'reporterCode': '699',
    'flowCode': 'M',
    'cmdCode': '2711',
    'customsCode': 'C00',
    'motCode': '0',
    'partner2Code': '0',
    'breakdownMode': 'classic',
    'includeDesc': 'True',
    'format': 'csv' 
}

# Replace this with your token from the Comtrade Developer Settings page
headers_config = {
    'Ocp-Apim-Subscription-Key': 'b093b6f11d476134bbbd5a4e66585f2b'
}

# 4. Trigger download mechanics
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

print("Fetching requested dataset...")
api_response = requests.get(api_base_url, params=query_parameters, headers=headers_config)

if api_response.status_code == 200:
    with open(FULL_PATH, "wb") as csv_file:
        csv_file.write(api_response.content)
    print(f"Success! Data saved smoothly to: {FULL_PATH}")
else:
    print(f"API Error. Server responded with error status: {api_response.status_code}")
    print("Double check that your subscription key is active and spelled correctly.")
