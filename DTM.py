import pandas as pd

# df has columns: 'ID', 'Tweet', 'Hashtags'
df = pd.read_excel('Book1.xlsx')

def clean_input(input_string):
    # Remove parentheses and spaces
    cleaned = input_string.replace('(', '').replace(')', '').replace(' ', '')
    # Replace 'and' and 'or' with ','
    cleaned = cleaned.replace('and', ',').replace('or', ',').replace('not', '')
    return cleaned

query = input("Search: ")
chosen_hashtags = clean_input(query).split(",") # Cleaned input for showing DTM


# Clean the Hashtags column by removing occurrences of "\\u200"
df['hashtags'] = df['hashtags'].str.replace('\\u200c', '', regex=False)

# Initialize an empty list to store the hashtag sets


chosen_hashtags = sorted(chosen_hashtags)


doc_term_matrix = []


for index, row in df.iterrows():
    tweet_hashtags = [s.strip("[']") for s in row['hashtags'].split(', ')]
    binary_row = [1 if hashtag in tweet_hashtags else 0 for hashtag in chosen_hashtags]
    doc_term_matrix.append(binary_row)


dtm_df = pd.DataFrame(doc_term_matrix, columns=chosen_hashtags, index=df['ID'])


print(dtm_df)