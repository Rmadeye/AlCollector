from datetime import datetime
from typing import List, Optional
import pandas as pd

# Class for handling the database
class Assortiment:
    def __init__(self, db):
        self.db = pd.read_csv(db)

    # Get all products
    def remove_product_from_csv_by_index(self, index):

        self.db = self.db.drop(index)
        # df = df.reset_index(drop=True)
        self.db.to_csv('./src/db.csv', index=False)
        return 'Product removed successfully.'
    

    def remove(self,index):
        self.db.drop(index=index-1, inplace=True)
        # df  = df.reset_index()
        self.db.to_csv('./src/db.csv', index=False)
        print("here")
        return 'Product removed successfully.'
    
    def add(self, name, volume, strength, date_of_production, bottles, comment):
        new_product = {'index':  len(self.db) + 1,
            'name': name,
            'volume': volume,
            'strength': strength,
            'date_of_production': date_of_production,
            'bottles': bottles,
            'comments': comment,
        }

        self.db = pd.concat([self.db, pd.DataFrame([new_product])], ignore_index=True)
        return self.db.to_csv('./src/db.csv', index=False)
    
    def get_statistics(self):
        df = self.db
        grouped_summary = df.groupby('name')
        summary = grouped_summary.agg({'bottles': 'sum', 'volume': 'sum', 'strength': 'mean'})
        #round strenght to 1 decimal
        summary['strength'] = summary['strength'].round(1)
        summary = summary.rename(columns={'bottles': 'total_bottles', 'volume': 'total_volume'})
        # add total sum of bottles and volume
        summary.loc['Total'] = summary.sum()
        summary['total_volume'] = (summary.total_volume/1000).round(2)
        summary['total_bottles'] = summary.total_bottles.astype(int)
        # and mean the strength in total
        summary.loc['Total', 'strength'] = summary['strength'].mean().round(1)
        summary = summary.reset_index()
        # return summary.to_csv('./src/summary.csv', index=False)
        return summary

