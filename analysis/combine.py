import pandas as pd

df=pd.read_csv('bmovie.csv')

df['movies']= df['movies'].map(lambda x:x.replace('[','').replace(']','').replace('"',''))
print("共抓取 ",len(df['user_mid'].unique())," 个B站用户")

mov=df.groupby(by=['user_mid','user_uname']).agg({'movies':sum}).reset_index()
mov.to_csv('combined_movies.csv',columns=['user_mid','user_uname','movies'],index=None)
