import pandas as pd

print("Loading dataset...")  

df = pd.read_csv(r"D:\binance_trade_analysis\trades.csv")

print("Dataset loaded successfully!")

# Drop rows where Trade_History is missing
df = df.dropna(subset=['Trade_History'])

print("First 5 rows:\n", df.head())  
print("\nDataset Info:")
print(df.info())
print("\nMissing Values:\n", df.isnull().sum())
print("Missing values after cleaning:\n", df.isnull().sum())

input("\nPress Enter to exit...")  

