import plotly.express as px
import pandas as pd

if __name__ == '__main__':
    pd.set_option('display.width', None)
    df = pd.read_csv('defined_metro.csv', dtype=str)
    types = {"GetOn":int, "GetOff":int, "Latitude":float, "Longitude":float}
    for key, typename in types.items():
        df[key] = df[key].astype(typename)

    sub = df[df['Year'] == '2019']
    print(sub.head(10))
    fig = px.bar(sub, x='Month', y='GetOn')
    fig.show()