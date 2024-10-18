import pandas as pd
import re

# Assume df has columns: 'ID', 'Tweet', 'Hashtags'
df = pd.read_excel('Book1.xlsx')

# Function to tokenize the query string
def tokenize_query(query):
    # Handle the logical operators and hashtags
    tokens = re.findall(r'\w+|[()]|and|or|not', query)
    return tokens

# Recursive function to evaluate the logical expression
def eval_expression(tokens, dtm):
    stack = []
    operator_stack = []

    # Operator precedence
    precedence = {'and': 2, 'or': 1, 'not': 3}

    def apply_operator():
        """Apply the top operator in operator_stack to the values in the stack."""
        operator = operator_stack.pop()
        if operator == 'not':
            operand = stack.pop()
            stack.append(~operand)
        else:
            right = stack.pop()
            left = stack.pop()
            if operator == 'and':
                stack.append(left & right)
            elif operator == 'or':
                stack.append(left | right)

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            operator_stack.append('(')
        elif token == ')':
            # Apply all operators till matching '('
            while operator_stack and operator_stack[-1] != '(':
                apply_operator()
            operator_stack.pop()  # Remove the '('
        elif token in precedence:
            # While there are operators with higher or equal precedence, apply them
            while (operator_stack and operator_stack[-1] != '(' and
                   precedence.get(operator_stack[-1], 0) >= precedence[token]):
                apply_operator()
            operator_stack.append(token)
        else:
            # It's a hashtag, append the DTM column
            stack.append(dtm[token])

        i += 1

    # Apply remaining operators
    while operator_stack:
        apply_operator()

    return stack[0]

query = input("Search: ")

# Clean the Hashtags column by removing occurrences of "\\u200c"
df['hashtags'] = df['hashtags'].str.replace('\\u200c', '', regex=False)

# Extract the hashtags from the query for DTM building
hashtags_in_query = re.findall(r'\w+', query)
chosen_hashtags = sorted(set(hashtags_in_query))

# Create the Document-Term Matrix (DTM)
doc_term_matrix = []
for index, row in df.iterrows():
    tweet_hashtags = [s.strip("[']") for s in row['hashtags'].split(', ')]
    binary_row = [1 if hashtag in tweet_hashtags else 0 for hashtag in chosen_hashtags]
    doc_term_matrix.append(binary_row)

dtm_df = pd.DataFrame(doc_term_matrix, columns=chosen_hashtags, index=df['ID'])

# Tokenize the query
tokens = tokenize_query(query)

# Evaluate the query on the DTM
result = eval_expression(tokens, dtm_df)

# Retrieve the matching documents
matching_docs = df[df['ID'].isin(result[result == 1].index)]
matching_docs.to_excel('output.xlsx', index=False)