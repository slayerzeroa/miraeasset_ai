import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('./matching_system/data/test_data.csv')

print(df.head())


plt.plot(df['job'], df['asset'], 'o')
plt.xlabel('age')
plt.ylabel('asset')
plt.show()