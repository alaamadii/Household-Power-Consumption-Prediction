import pandas as pd
def load_data(file_path):
    df = pd.read_csv(file_path, sep=";" , na_values="?", low_memory=False)
    #print(df.head())
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst=True)
    df.drop(columns=['Date', 'Time'], inplace=True)

    df.fillna(df.mean(), inplace=True)

    y= df['Global_active_power']
    x = df.drop(columns=['Global_active_power', 'Datetime'])
    return x,y
