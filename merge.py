import pandas as pd
import glob
csv_files = glob.glob("data/*.csv")
dfs = [pd.read_csv(f) for f in csv_files]
merged_ds = pd.concat(dfs, ignore_index=True)

merged_ds.to_csv("merged_output.csv", index=False)
print('Success')
df = pd.read_csv('merged_output.csv')

df['date'] = pd.to_datetime(df['date'])
df_sorted = df.sort_values(by='date', ascending=True)
df_sorted.to_csv('sorted.csv' , index=False)
print('Sorting Success')

fd =pd.read_csv('sorted.csv')
pink_morsel_fd = fd[fd['product'] == 'pink morsel']
pink_morsel_fd.to_csv('filtered_pink_morsel.csv', index=False)
print("Pink Morsel Filtered")
pmfd = pd.read_csv('filtered_pink_morsel.csv')
pmfd['price'] = pmfd['price'].replace('[\$,]', '', regex=True).astype(float)
pmfd['sales'] = pmfd['price'] * pmfd['quantity']
pmfd = pmfd.drop(columns=['price', 'quantity'])
pmfd['sales'] = pmfd['sales'].apply(lambda x: f"${x:.2f}")
pmfd = pmfd[[ 'sales', 'date', 'region']]
pmfd.to_csv("Sales.csv", index=False)
print('Successfylly converted the sales')

print(pmfd.head())

