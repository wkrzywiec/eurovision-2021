import pathlib
import pandas as pd
import os
from googleapiclient.discovery import build
from datetime import datetime

def fetch_data():

    api_key = os.getenv('YOUTUBE_API_KEY')
    if api_key is None:
        raise ValueError('api_key was not got from env variable')

    current_path = pathlib.Path().absolute()

    df=pd.read_csv(str(current_path) + '\\sources.csv', sep=',')
    ids = df['key'].str.cat(sep=',')

    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(id=ids, part='statistics')
    response = request.execute()

    new_line = [datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
    for index, row in df.iterrows():
        new_line.append(next((item for item in response['items'] if item['id'] == df['key'].at[index]), None)['statistics']['viewCount'])

    new_line_string = ','.join(map(str, new_line))

    with open(str(current_path) + '\\data.csv', 'a') as data:
        data.write(f'\n{new_line_string}')

if __name__ == "__main__":
    fetch_data()
