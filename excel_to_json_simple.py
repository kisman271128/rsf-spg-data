#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SIMPLE Excel to JSON Converter
File: C:\rsf-spg-app\rsf-spg-data\DSourceSPGApp.xlsb
Output: C:\rsf-spg-app\rsf-spg-data\data\*.json
"""

import pandas as pd
import json
import os
from datetime import datetime

# HARD-CODED PATHS
EXCEL_FILE = r"D:\rsf-spg-app\rsf-spg-data\DSourceSPGApp.xlsb"
OUTPUT_DIR = r"D:\rsf-spg-app\rsf-spg-data\data"

def main():
    print("=" * 60)
    print("EXCEL TO JSON - SIMPLE VERSION")
    print("=" * 60)
    print()
    
    # Check Excel file
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ Excel not found: {EXCEL_FILE}")
        return False
    
    print(f"📂 Reading: {EXCEL_FILE}")
    print()
    
    try:
        # Read Excel
        excel = pd.ExcelFile(EXCEL_FILE, engine='pyxlsb')
        sheets = excel.sheet_names
        
        print(f"📄 Total sheets: {len(sheets)}")
        
        # Filter sheets starting with "d_"
        target_sheets = [s for s in sheets if s.startswith('d_')]
        
        if not target_sheets:
            print("⚠️  No sheets starting with 'd_' found!")
            return False
        
        print(f"✅ Target sheets: {', '.join(target_sheets)}")
        print()
        
        # Create output directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Process each sheet
        for sheet in target_sheets:
            print(f"🔄 Processing: {sheet}...", end=" ")
            
            # Read sheet
            df = pd.read_excel(excel, sheet_name=sheet)
            
            # Convert to records
            records = df.to_dict('records')
            
            # Clean NaN
            for record in records:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
            
            # Create JSON
            json_data = {
                "sheet": sheet,
                "updated": datetime.now().isoformat(),
                "rows": len(records),
                "columns": list(df.columns),
                "data": records
            }
            
            # Save JSON
            json_file = os.path.join(OUTPUT_DIR, f"{sheet}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            file_size = os.path.getsize(json_file) / 1024
            print(f"✅ ({len(records)} rows, {file_size:.1f} KB)")
        
        print()
        print("=" * 60)
        print(f"✅ SUCCESS! {len(target_sheets)} files created")
        print("=" * 60)
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
