import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def calc_dil(volume: float, final_voltage: float, initial_voltage: float):

    data = []
    with open('src/density.csv', 'r', encoding='utf-8') as file:
        readCSV = csv.reader(file, delimiter=';')

        for row in readCSV:
            data.append(row)

    df = pd.DataFrame(data[1:], columns=data[0][0:2])
    data = df.set_index('percent')['density'].to_dict()
    initial_density = data[str(int(initial_voltage))]
    
    final_density = data[str(final_voltage)]

    answer = (
        (float(volume)*float(initial_voltage)*float(initial_density))-(volume*float(final_voltage)*float(final_density)
                                                                ))/(
                                                                    final_voltage*float(final_density)
                                                                    )
    pure = volume*(float(initial_voltage)/100)*float(initial_density)
    
    return round(answer,0), str(round(pure,2))

def plot_data(df: pd.DataFrame, x: str, y:str) -> plt:
    # set background color to grey
    plt.rcParams['axes.facecolor'] = 'grey'
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    plt.rcParams['figure.facecolor'] = 'grey'
    plt.rcParams['figure.edgecolor'] = 'grey'
    plt.rcParams['savefig.facecolor'] = 'grey'
    df = df[['name',y]].groupby(x).sum()

    fig, ax = plt.subplots()
    sns.barplot(df, x=x, y=y, ax=ax, color='red')

    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(f'{y} per {x}')
    sns.set(font_scale=1.5)
    plt.xticks(rotation=90)
    plt.tight_layout()
    return fig