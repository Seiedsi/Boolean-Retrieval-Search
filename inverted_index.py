import pandas as pd  

# Step 1: Load the XLSX file  
df = pd.read_excel('Book1.xlsx')  

# df has columns: 'ID', 'Tweet', 'Hashtags'

# Initialize an empty dictionary to store the inverted index
inverted_index = {}

df['hashtags'] = df['hashtags'].str.replace('\\u200c', '', regex=False)

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    tweet_id = row['ID']
    # hashtags = row['hashtags'].split(', ')
    hashtags = [s.strip("[']") for s in row['hashtags'].split(', ')]

    # For each hashtag in the current row
    for hashtag in hashtags:
        if hashtag in inverted_index:
            inverted_index[hashtag].append(tweet_id)
        else:
            inverted_index[hashtag] = [tweet_id]

# Show the inverted index
for hashtag, tweet_ids in inverted_index.items():
    print(f"{hashtag}: {tweet_ids}")