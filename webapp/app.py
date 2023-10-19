from flask import Flask, render_template, redirect, request, jsonify
import sys
sys.path.append('~/websites/liquor-base/src')
from src.db_handler import Assortiment
from src.alculator import Calculations
import pandas as pd

app = Flask(__name__)
Assortiment = Assortiment('./src/db.csv')
# def remove_product_from_csv_by_index(index):
#     df = pd.read_csv('./src/db.csv')
#     df = df.drop(index)
#     # df = df.reset_index(drop=True)
#     df.to_csv('./src/adb.csv', index=False)

@app.route('/')
def index():
    df =  Assortiment.db
    summary = Assortiment.get_statistics()
    print(summary)
    rows_summary = summary.to_dict('records')
    names = df['name'].unique().tolist()
    rows = df.to_dict('records')
    return render_template('index.html', names=names, rows=rows, rows_summary=rows_summary)

@app.route('/remove/<int:index>')
def remove(index):
    return Assortiment.remove(index)

@app.route('/add/<name>/<volume>/<strength>/<date_of_production>/<bottles>/<comments>')
def add(name, volume, strength, date_of_production, bottles, comments):
    Assortiment.add(name, volume, strength, date_of_production, bottles, comments)
    return redirect('/')

@app.route('/calculate', methods=['GET'])
def calculate():
    volume = float(request.args.get('volume'))
    conc = float(request.args.get('conc'))
    desired = float(request.args.get('desired'))

    alculator = Calculations()
    result = alculator.calc_dil(volume, desired, conc)[0]
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run()

