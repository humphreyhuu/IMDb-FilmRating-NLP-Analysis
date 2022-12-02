import pickle
import pandas as pd
import warnings
import datetime
warnings.filterwarnings('ignore')
with open('film_info_df_v3.pkl', 'rb') as f:
    df = pickle.load(f)
pd.set_option('display.max_columns', 500)
import re

def data_clean(df):
    def data_tans1(Duration_minute):
        if Duration_minute is None:
            return None
        a = Duration_minute.replace("h", '*60').replace(' ','+').replace('m','*1')
        return eval(a)

    def data_tans2(Rating_popularity):
        if Rating_popularity is None:
            return None
        a = Rating_popularity.replace("K","*1e3")
        a = a.replace("M","*1e6")
        return eval(a)

    def data_tans3(Release_date):
        if Release_date is None:
            return None
        a = Release_date[Release_date.find("(")+1:Release_date.find(")")]
        return a

    def data_tran5(Release_date):
        if Release_date is None:
            return None
        if len(Release_date.split(' ')) == 4:
            a = Release_date.split(' ')[-2] + '-' + data_dict[Release_date.split(' ')[0]] + '-' + Release_date.split(' ')[1].split(',')[0]
            a = datetime.datetime.strptime(a,'%Y-%m-%d')
            return a
        if len(Release_date.split(' ')) == 3:
            a = Release_date.split(' ')[1] + '-' + data_dict[Release_date.split(' ')[0]]
            a = datetime.datetime.strptime(a,'%Y-%m')
            return a
        if len(Release_date.split(' ')) == 2:
            a = Release_date.split(' ')[0]
            a = datetime.datetime.strptime(a,'%Y')
            return a
    data_dict = {'January':'01','February':'02','March':'03','April':'04','May':'05',
             'June':'06','July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}
             
    df['Duration_minute']=  df['Duration_minute'].apply(lambda x:data_tans1(x))
    df["Rating_popularity"] = df["Rating_popularity"].apply(lambda x:data_tans2(x))
    df[['Win', 'Nomination']] = df['Awards'].str.split('&', 1, expand=True)
    # seperate Awards into Win and Nomination
    df['Win'] = df['Win'].str.replace(r'\D', '')
    df['Nomination'] = df['Nomination'].str.replace(r'\D', '')
    df = df.drop('Awards',axis = 1)
    df['Release_location'] = df['Release_date'].apply(lambda st: data_tans3(st))
    #get the release location from release date 
    df['Release_date'] = df['Release_date'].str.replace(r"\(.*\)","")
    #drop release location from release date
    df['Filming_locations'] = df['Filming_locations'].str.rsplit(',').str[-1] 
    df['Budget'] = df['Budget'].str.replace('$', '')
    df['Budget'] = df['Budget'].str.replace(r"\(.*\)","")
    df['Gross_US_Canada'] = df['Gross_US_Canada'].str.replace('$', '')
    df['Opening_weekend'] = df['Opening_weekend'].str.replace('$', '')
    df['Gross_worldwide'] = df['Gross_worldwide'].str.replace('$', '')
    #delete $ and text in parentheses 
    df['Color'] = df['Color'].str.replace(
        'Black and White(original release)Black and White','Black and White').replace(
        'ColorBlack and White','Color, Black and White').replace(
        'Black and WhiteColor','Color, Black and White')
    
    df['Release_date'] = df['Release_date'].apply(lambda x:data_tran5(x))
    df['Rating_popularity'] = df['Rating_popularity'].apply(lambda x:int(x))
    df['Duration_minute'] = df['Duration_minute'].apply(lambda x:int(x))
    return df