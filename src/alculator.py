import  csv

import pandas as pd

class Calculations:


    def __init__(self):
        pass

    def calc_dil(self, volume: float, final: float, solution: float):

        data = []
        with open('src/density.csv', 'r', encoding='utf-8') as file:
            readCSV = csv.reader(file, delimiter=';')

            for row in readCSV:
                data.append(row)

        df = pd.DataFrame(data[1:], columns=data[0][0:2])
        data = df.set_index('percent')['density'].to_dict()
        initial_density = data[str(int(solution))]
        final_density = data[str(int(final))]

        answer = ((float(volume)*float(solution)*float(initial_density))-(volume*float(final)*float(final_density)))/(final*float(final_density))
        pure = volume*(float(solution)/100)*float(initial_density)
        
        return round(answer,0), str(round(pure,2))