"""L49 练习 3: 参考答案"""

from __future__ import annotations

import matplotlib.pyplot as plt
import seaborn as sns

df = sns.load_dataset("mpg")
numeric = df.select_dtypes(include="number")
corr = numeric.corr()
sns.heatmap(corr, annot=True, cmap="RdBu_r", fmt=".2f")
plt.tight_layout()
plt.show()
max_pair = corr.unstack().sort_values(ascending=False)
print(f"最强正相关: {max_pair.index[1]} = {max_pair.iloc[1]:.2f}")
print(f"最强负相关: {max_pair.index[-1]} = {max_pair.iloc[-1]:.2f}")
