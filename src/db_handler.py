import mysql.connector
import pandas as pd
import json

# Read database connection details from the JSON file
with open('db/db_config.json', 'r') as f:
    config = json.load(f)

# Connect to the database
mydb = mysql.connector.connect(**config)

class DBHandler:


    def  __init__(self, table='', create_table=False):
        self.table = table
        self.mycursor = mydb.cursor()
        self.mycursor.execute("USE liqour")
        if create_table:
            self.mycursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table} (id INT AUTO_INCREMENT PRIMARY KEY,\
                name VARCHAR(255),\
                voltage INT,\
                volume INT,\
                prod_date DATE,\
                num_bottles INT,\
                description VARCHAR(255))")

    def get_all(self):
        self.mycursor.execute(f"SELECT * FROM {self.table}")
        data = self.mycursor.fetchall()
        df = pd.DataFrame(data, columns=['id', 'name', 'voltage', 'volume', 'prod_date', 'num_bottles', 'description'])
        return df
    
    def get_product(self, feature, value):
        query = f"SELECT * FROM {self.table} WHERE {feature} = %s"
        self.mycursor.execute(query, (value,))
        data = self.mycursor.fetchall()
        
        if data is None:
            return "No record found with the provided id."
        else:
            return pd.DataFrame(data, columns=['id', 'name', 'voltage', 'volume', 'prod_date', 'num_bottles', 'description'])

        
    def add_entry(self, name, voltage, volume, prod_date, num_bottles, description):
        sql = f"INSERT INTO {self.table} (name, voltage, volume, prod_date, num_bottles, description) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name, voltage, volume, prod_date, num_bottles, description)
        self.mycursor.execute(sql, val)
        mydb.commit()
        print(self.mycursor.rowcount, "record inserted.")
        return "Added successfully."

    def delete_entry(self, id):
        self.mycursor.execute(f"DELETE FROM {self.table} WHERE id = {id}")
        mydb.commit()
        if self.mycursor.rowcount > 0:
            return "Deleted"
        else:
            return "No record found with the provided id."


    def update_entry(self, id, feature, value):
        sql = f"UPDATE {self.table} SET {feature} = %s WHERE id = {id}"
        self.mycursor.execute(sql, (value,))
        mydb.commit()
        if self.mycursor.rowcount == 0:
            return "No record found with the provided id."
        else:
            return f"{self.mycursor.rowcount} record(s) affected"
