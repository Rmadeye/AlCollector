import pandas as pd

def get_statistics():
    df = pd.read_csv('./src/db.csv')
    grouped_summary = df.groupby('name')
    summary = grouped_summary.agg({'bottles': 'sum', 'volume': 'sum', 'strength': 'mean'})
    #round strenght to 1 decimal
    summary['strength'] = summary['strength'].round(1)
    summary = summary.rename(columns={'bottles': 'total_bottles', 'volume': 'total_volume'})
    # add total sum of bottles and volume
    summary.loc['Total'] = summary.sum()
    # and mean the strength in total
    summary.loc['Total', 'strength'] = summary['strength'].mean().round(1)
    print(summary)
    return summary

get_statistics()