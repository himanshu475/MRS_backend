import pandas as pd
import os
import ast

file_path='../data/tmdb_5000_movies.csv'


df=pd.read_csv(file_path)

credits_df="../data/tmdb_5000_credits.csv"
credits_df=pd.read_csv(credits_df)

print("Dataset Preview:")
print(df.head())


print("\nDataset Information:")
print(df.info())


print("\nMissing Values:")
print(df.isnull().sum)


print("\nBasic Statistics for Numeric Columns: ")
print(df.describe())

if 'genres' in df.columns:
    print("\nUnique Genres: ")
    print(df['genres'].unique())
    
# processing keywords of movies 
def parse_keywords(text):
    try:
        keywords_list=ast.literal_eval(text)
        return [item['name'] for item in keywords_list]
    except:
        return []


def parse_column(text):
    try:
        data=ast.literal_eval(text)
        return [item['name'] for item in data]
    except:
        return []

df['genres']=df['genres'].apply(parse_column)

print("\nParsed Genres:")
print(df['homepage'].head(15))


# calling funtion for movie keywords extraction
# df['parsed_keywords']=df['keywords'].apply(parse_keywords)

# print("\nKeywords")
# print(df[['title', 'parsed_keywords']].head(5))
# # print(df['keywords'].head(10))


# print("\nDataset Information:")
# print(credits_df.info())