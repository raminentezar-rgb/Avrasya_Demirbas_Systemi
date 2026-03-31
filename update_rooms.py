import pandas as pd
import os

def update_inventory():
    file_path = 'inventory.xlsx'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    print("Loading inventory.xlsx...")
    df = pd.read_excel(file_path)

    updates = {
        'KA_': ['KAŞÜSTÜ', 'Kaşüstü'],
        'YA_': ['YALINCAK'],
        'YO_': ['YOMRA', 'yomra'],
        'P_':  ['Pelitli']
    }

    modified_count = 0
    total_rows = len(df)

    for idx, row in df.iterrows():
        campus = str(row['Campus'])
        room = str(row['Room']) if pd.notna(row['Room']) else ""
        
        updated = False
        for prefix, keywords in updates.items():
            if any(kw in campus for kw in keywords):
                if not room.startswith(prefix):
                    room = prefix + room
                    df.at[idx, 'Room'] = room
                    modified_count += 1
                    updated = True
                break # Only one prefix per row
        
    if modified_count > 0:
        print(f"Modified {modified_count} out of {total_rows} rows.")
        print("Saving updated Excel file...")
        df.to_excel(file_path, index=False)
        print("Success!")
    else:
        print("No changes needed. All rooms already have correct prefixes.")

if __name__ == "__main__":
    update_inventory()
