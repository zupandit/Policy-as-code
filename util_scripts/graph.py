import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("final.csv")

# Remove 'checkov-yaml'
df = df[df["technology"] != "checkov-yaml"]

# Set consistent style and color
sns.set(style="white")
custom_color = "#a3a3a3"

### 1. Boxplot by Technology
plt.figure(figsize=(10, 6))
ax1 = sns.boxplot(
    data=df,
    x="technology",
    y="dev_percentage",
    color=custom_color,
    showfliers=False
)

sns.despine(top=True, right=True)

tick_labels = [tick.get_text() for tick in ax1.get_xticklabels()]
medians = df.groupby("technology")["dev_percentage"].median()
for i, label in enumerate(tick_labels):
    if label in medians:
        median_val = medians[label]
        ax1.text(i, median_val + 1, f"{median_val:.1f}%", ha='center', fontweight='normal')

ax1.set_ylabel("Percentage of development")
ax1.set_xlabel("")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

### 2. Histogram (Binned Distribution)
plt.figure(figsize=(10, 6))

bin_edges = [1] + list(range(10, 101, 10))  
bin_labels = [f"{bin_edges[i]}-{bin_edges[i+1]}%" for i in range(len(bin_edges)-1)]

df['bin'] = pd.cut(df['dev_percentage'], bins=bin_edges, right=False, labels=bin_labels)
bin_counts = df['bin'].value_counts().sort_index()

ax2 = bin_counts.plot(kind='bar', color=custom_color, edgecolor='none')

for i, val in enumerate(bin_counts):
    percent = val / len(df) * 100
    ax2.text(i, val + 2, f"{percent:.0f}%", ha='center')

plt.xticks(rotation=45, ha='right')

ax2.set_xlabel("Percentage of development elapsed at introduction")
ax2.set_ylabel("Number of repositories")

sns.despine(top=True, right=True)
plt.grid(False)

plt.tight_layout()
plt.show()
