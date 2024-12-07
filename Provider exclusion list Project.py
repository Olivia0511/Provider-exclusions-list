import pandas as pd
import sqlite3

# file locations
georgia_exclusions_path = r'C:\Users\18378\OneDrive\桌面\provider exclusion project\Georgia OIG Exclusions List.csv'
leie_exclusions_path = r'C:\Users\18378\OneDrive\桌面\provider exclusion project\LEIE Exclusions Database.csv'

# read data
georgia_exclusions = pd.read_csv(georgia_exclusions_path)
leie_exclusions = pd.read_csv(leie_exclusions_path)

# Clean files
georgia_exclusions_cleaned = georgia_exclusions.iloc[2:, [0, 1, 2, 3, 4, 5]].copy()
georgia_exclusions_cleaned.columns = ["LASTNAME", "FIRSTNAME", "BUSNAME", "GENERAL", "STATE", "EXCLDATE"]
georgia_exclusions_cleaned = georgia_exclusions_cleaned.dropna(subset=["LASTNAME", "FIRSTNAME", "EXCLDATE"])

leie_exclusions_cleaned = leie_exclusions[
    ["LASTNAME", "FIRSTNAME", "BUSNAME", "GENERAL", "STATE", "EXCLDATE"]
].copy()
leie_exclusions_cleaned = leie_exclusions_cleaned.dropna(subset=["EXCLDATE"])

# Combine datasets
excluded_providers = pd.concat([georgia_exclusions_cleaned, leie_exclusions_cleaned], ignore_index=True)

# Create database
database_path = "excluded_providers.db"
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ExcludedProviders (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    LASTNAME TEXT,
    FIRSTNAME TEXT,
    BUSNAME TEXT,
    GENERAL TEXT,
    STATE TEXT,
    EXCLDATE TEXT
)
""")

excluded_providers.to_sql('ExcludedProviders', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

print(f"Database created and saved to: {database_path}")
