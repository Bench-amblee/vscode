import pandas as pd
from sodapy import Socrata
import matplotlib.pyplot as plt
from collections import Counter
import math

client = Socrata("data.sfgov.org", None)
results = client.get("4542-gpa3", limit = 11000)

results_df = pd.DataFrame.from_records(results)
results_list = results_df['direction']

cleaned_list = [item for item in results_list if not (isinstance(item, float) and math.isnan(item))]


item_counts = Counter(cleaned_list)

items = list(item_counts.keys())
counts = list(item_counts.values())

plt.bar(items, counts)
plt.xlabel('Items')
plt.ylabel('Counts')
plt.title('Item Counts in the List')
plt.show()
