import pandas as pd
import json
import os
from logging_config import logger  # Import the logger

# Load dataset
logger.info("Loading dataset...")
print("Loading dataset...")
file_path = "structured_trades.csv"

if os.path.exists(file_path):
    logger.info("Loaded existing structured trade data.")
    print("Loaded existing structured trade data.")
    df = pd.read_csv(file_path)
else:
    raw_data = pd.read_csv("trade_history.csv")
    df = pd.json_normalize(raw_data["Trade_History"].apply(json.loads))
    df["Port_IDs"] = raw_data["Port_IDs"]
    df.to_csv(file_path, index=False)
    logger.info("Structured trade data saved as 'structured_trades.csv'.")
    print("Structured trade data saved as 'structured_trades.csv'.")

# Calculate financial metrics
def calculate_metrics(df):
    account_groups = df.groupby("Port_IDs")
    
    account_metrics = account_groups.agg(
        PnL=("realizedProfit", "sum"),
        Total_Investment=("quantity", "sum"),
        PnL_StdDev=("realizedProfit", "std"),
        Win_Positions=("realizedProfit", lambda x: (x > 0).sum()),
        Total_Positions=("realizedProfit", "count")
    )
    
    account_metrics["ROI"] = (account_metrics["PnL"] / account_metrics["Total_Investment"]) * 100
    account_metrics["Sharpe_Ratio"] = account_metrics["PnL"] / account_metrics["PnL_StdDev"]
    account_metrics["Sharpe_Ratio"] = account_metrics["Sharpe_Ratio"].fillna(0)  # Handle division by zero
    
    # Maximum Drawdown (MDD) Placeholder
    account_metrics["MDD"] = 100  # Set to 100 for now
    
    # Calculate Win Rate
    account_metrics["Win_Rate"] = (account_metrics["Win_Positions"] / account_metrics["Total_Positions"]) * 100
    
    return account_metrics

# Compute account metrics
account_metrics = calculate_metrics(df)
logger.info("Calculated account metrics successfully.")

# Normalize metrics for ranking
account_metrics["MDD_Score"] = 1 / (1 + account_metrics["MDD"])  # Inverse MDD (lower is better)
account_metrics["Normalized_ROI"] = (account_metrics["ROI"] - account_metrics["ROI"].min()) / (account_metrics["ROI"].max() - account_metrics["ROI"].min())
account_metrics["Normalized_Sharpe"] = (account_metrics["Sharpe_Ratio"] - account_metrics["Sharpe_Ratio"].min()) / (account_metrics["Sharpe_Ratio"].max() - account_metrics["Sharpe_Ratio"].min())
account_metrics["Normalized_PnL"] = (account_metrics["PnL"] - account_metrics["PnL"].min()) / (account_metrics["PnL"].max() - account_metrics["PnL"].min())
account_metrics["Normalized_Win_Rate"] = (account_metrics["Win_Rate"] - account_metrics["Win_Rate"].min()) / (account_metrics["Win_Rate"].max() - account_metrics["Win_Rate"].min())

# Composite Score (Weighted Sum)
account_metrics["Score"] = (
    (account_metrics["Normalized_ROI"] * 0.3) +
    (account_metrics["Normalized_Sharpe"] * 0.2) +
    (account_metrics["Normalized_PnL"] * 0.2) +
    (account_metrics["Normalized_Win_Rate"] * 0.2) +
    (account_metrics["MDD_Score"] * 0.1)
)

# Save overall metrics to CSV
account_metrics.to_csv("account_metrics.csv")
logger.info("Account metrics saved as 'account_metrics.csv'.")

# Get Top 20 Accounts
top_20_accounts = account_metrics.sort_values("Score", ascending=False).head(20)

# Save Top 20 Accounts to CSV
top_20_accounts.to_csv("top_20_accounts.csv")
logger.info("Top 20 accounts saved as 'top_20_accounts.csv'.")
print("\nTop 20 accounts saved as 'top_20_accounts.csv'.")

# Print top accounts
logger.info("Displaying top accounts based on ROI, Sharpe Ratio, and MDD.")
print("\nTop 5 Accounts by ROI:")
print(account_metrics.sort_values("ROI", ascending=False).head())

print("\nTop 5 Accounts by Sharpe Ratio:")
print(account_metrics.sort_values("Sharpe_Ratio", ascending=False).head())

print("\nTop 5 Accounts with Lowest MDD (Lower Risk):")
print(account_metrics.sort_values("MDD").head())

# Print Summary
print("\nSummary of Key Metrics:")
print(f"Highest ROI: {account_metrics['ROI'].max():.2f}%")
print(f"Highest Sharpe Ratio: {account_metrics['Sharpe_Ratio'].max():.2f}")
print(f"Lowest MDD: {account_metrics['MDD'].min():.2f}%")
print(f"Highest Win Rate: {account_metrics['Win_Rate'].max():.2f}%")

logger.info(f"Summary - Highest ROI: {account_metrics['ROI'].max():.2f}%")
logger.info(f"Summary - Highest Sharpe Ratio: {account_metrics['Sharpe_Ratio'].max():.2f}")
logger.info(f"Summary - Lowest MDD: {account_metrics['MDD'].min():.2f}%")
logger.info(f"Summary - Highest Win Rate: {account_metrics['Win_Rate'].max():.2f}%")

print("\nAccount metrics saved as 'account_metrics.csv'.")
logger.info("Execution completed successfully.")

input("Press Enter to exit...")
