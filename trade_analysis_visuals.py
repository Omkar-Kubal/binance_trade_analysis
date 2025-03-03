import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load computed metrics
df = pd.read_csv("account_metrics.csv")

# Set Seaborn style
sns.set_style("whitegrid")

# 1️⃣ ROI Distribution
plt.figure(figsize=(10, 5))
sns.histplot(df["ROI"], bins=30, kde=True, color="blue")
plt.xlabel("ROI (%)")
plt.ylabel("Frequency")
plt.title("Distribution of ROI across Accounts")
plt.savefig("roi_distribution.png")
plt.show()

# 2️⃣ Sharpe Ratio vs. ROI
plt.figure(figsize=(10, 5))
sns.scatterplot(x=df["Sharpe_Ratio"], y=df["ROI"], alpha=0.7)
plt.xlabel("Sharpe Ratio")
plt.ylabel("ROI (%)")
plt.title("Sharpe Ratio vs. ROI")
plt.savefig("sharpe_vs_roi.png")
plt.show()

# 3️⃣ Win Rate vs. PnL
plt.figure(figsize=(10, 5))
sns.scatterplot(x=df["Win_Rate"], y=df["PnL"], alpha=0.7, color="green")
plt.xlabel("Win Rate (%)")
plt.ylabel("Total PnL")
plt.title("Win Rate vs. PnL")
plt.savefig("winrate_vs_pnl.png")
plt.show()

# 4️⃣ Top 20 Accounts Ranking
top_20 = df.sort_values("Score", ascending=False).head(20)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_20["Score"], y=top_20["Port_IDs"], palette="coolwarm")
plt.xlabel("Score")
plt.ylabel("Account ID")
plt.title("Top 20 Accounts by Performance Score")
plt.savefig("top20_accounts.png")
plt.show()

print("Visualizations saved as PNG files.")
