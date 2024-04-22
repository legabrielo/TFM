import pandas as pd

# Crear los DataFrames de ejemplo
df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [4, 5, 6], 'D': [4, 5, 6]})
df2 = pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})
df3 = pd.DataFrame({'A': [7, 8, 9], 'C': [16, 17, 18]})
df4 = pd.DataFrame({'A': [7, 8, 9], 'D': [19, 20, 21]})

dataframes = [df2, df3, df4]  # Include df3 for adding new rows

for df in dataframes:
    df1 = pd.concat([df1, df], ignore_index=True)  # Concatenate with new index
    df1 = df1.groupby('A').sum().reset_index()  # Sum rows with same 'A' value

print(df1)