
import pandas as pd
import numpy as np
import os
import glob
import re

input_folder = r"E:/Avishkar/SUT"

output_file = r"E:/Avishkar/SUT/MoSPI_Industry_Input_Output_Matrices23.xlsx"

skip_rows = 1

first_product_row = 0
last_product_row = 141

first_industry_col = 2
last_industry_col = 68


def find_sut_sheets(xls):

    supply_candidates = []
    use_candidates = []

    for sheet in xls.sheet_names:

        name = sheet.lower().strip()

        # Detect Supply sheet
        if "supply" in name:
            supply_candidates.append(sheet)

        # Detect Use sheet
        elif "use" in name:
            use_candidates.append(sheet)

    if not supply_candidates:
        raise ValueError("Supply sheet not found")

    if not use_candidates:
        raise ValueError("Use sheet not found")

    if len(supply_candidates) > 1:
        raise ValueError(
            f"Multiple Supply sheets found: {supply_candidates}"
        )

    if len(use_candidates) > 1:
        raise ValueError(
            f"Multiple Use sheets found: {use_candidates}"
        )

    return supply_candidates[0], use_candidates[0]



def process_sut(excel_path):

    print("\nReading:", os.path.basename(excel_path))

    xls = pd.ExcelFile(excel_path)

    # Automatically detect sheets
    supply_sheet, use_sheet = find_sut_sheets(xls)

    print("Supply sheet:", supply_sheet)
    print("Use sheet:", use_sheet)

    # Read sheets
    supply = pd.read_excel(
        xls,
        sheet_name=supply_sheet,
        skiprows=skip_rows
    )

    use = pd.read_excel(
        xls,
        sheet_name=use_sheet,
        skiprows=skip_rows
    )

    # Industry names
    industries = supply.columns[
        first_industry_col:last_industry_col
    ].tolist()

    # Extract Supply matrix V
    V = supply.iloc[
        first_product_row:last_product_row,
        first_industry_col:last_industry_col
    ].apply(
        pd.to_numeric,
        errors="coerce"
    ).fillna(0).to_numpy().T

    # Extract Use matrix U
    U = use.iloc[
        first_product_row:last_product_row,
        first_industry_col:last_industry_col
    ].apply(
        pd.to_numeric,
        errors="coerce"
    ).fillna(0).to_numpy()

    # Check dimensions
    if V.shape[0] != len(industries):
        raise ValueError("Supply industry dimension mismatch")

    if U.shape[1] != len(industries):
        raise ValueError("Use industry dimension mismatch")

    if V.shape[1] != U.shape[0]:
        raise ValueError(
            f"Product dimension mismatch: V={V.shape}, U={U.shape}"
        )

    print("Supply matrix:", V.shape)
    print("Use matrix:", U.shape)


    # Total output per industry
    g = V.sum(axis=1)

    # Total supply per product
    q = V.sum(axis=0)

    # Safe inverse
    g_inv = np.divide(
        1.0,
        g,
        out=np.zeros_like(g, dtype=float),
        where=g != 0
    )

    q_inv = np.divide(
        1.0,
        q,
        out=np.zeros_like(q, dtype=float),
        where=q != 0
    )

    # B matrix: Product x Industry
    B = U * g_inv[np.newaxis, :]

    # D matrix: Industry x Product
    D = V * q_inv[np.newaxis, :]

    # A matrix: Industry x Industry
    A = D @ B

 
    A_df = pd.DataFrame(
        A,
        index=industries,
        columns=industries
    )

    B_df = pd.DataFrame(
        B,
        columns=industries
    )

    D_df = pd.DataFrame(
        D,
        index=industries
    )

    return A_df, B_df, D_df



excel_files = glob.glob(
    os.path.join(input_folder, "*.xlsx")
)

excel_files = [
    f for f in excel_files
    if os.path.abspath(f) != os.path.abspath(output_file)
    and not os.path.basename(f).startswith("~$")
]

if not excel_files:
    raise FileNotFoundError(
        "No Excel files found in the input folder"
    )

summary = []


with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    try:
        year = "2023"
        filename="SUT_2023-24"
        A_df, B_df, D_df = process_sut("E:/Avishkar/SUT/SUT_2023-24.xlsx")

        # Excel sheet names limited to 31 characters
        A_df.to_excel(
        writer,
        sheet_name=f"A_{year}"
        )

        B_df.to_excel(
        writer,
        sheet_name=f"B_{year}"
        )

        D_df.to_excel(
        writer,
        sheet_name=f"D_{year}"
        )

        summary.append({
                "Year": year,
                "File": filename,
                "Industries": A_df.shape[0],
                "Products": B_df.shape[0],
                "A_Dimensions": str(A_df.shape),
                "Status": "Success",
                "Error": ""
            })

        print("Successfully completed:", year)

    except Exception as e:

        print("ERROR:", year, str(e))

        summary.append({
                "Year": year,
                "File": filename,
                "Industries": None,
                "Products": None,
                "A_Dimensions": None,
                "Status": "Failed",
                "Error": str(e)
            })

    # Save summary
    pd.DataFrame(summary).to_excel(
        writer,
        sheet_name="Summary",
        index=False
    )



print("\n================================")
print("ALL AVAILABLE YEARS PROCESSED!")
print("================================")

print("Output saved at:")
print(output_file)

print("\nProcessing summary:")

print(
    pd.DataFrame(summary)[
        ["Year", "Status", "A_Dimensions"]
    ].to_string(index=False)
)
