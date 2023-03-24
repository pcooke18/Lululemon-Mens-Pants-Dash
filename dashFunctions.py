import collections
from wordcloud import WordCloud
from datetime import datetime
import pandas as pd
import re


def add_data():
    reviews = pd.read_csv('/Users/piersoncooke/GitHub Practice Repos/lululemon-scrape/Data/reviews_tokenized3.csv', index_col=False, parse_dates=['Date of Review'])
    reviews['Review Text Token'] = [re.sub(r'[^A-Za-z\s]', '', x).split() for x in reviews['Review Text Token']]

    products = pd.read_csv('/Users/piersoncooke/GitHub Practice Repos/lululemon-scrape/Data/all_products_updated3.csv', index_col = False)
    products = products[['Product_ID', 'Product Family', 'Product Design', 'Product Fabric']]

    data = pd.merge(reviews, products, left_on = 'Product ID', right_on = 'Product_ID', suffixes=('', '_y'))
    data = data.drop('Product_ID', axis = 1)
    data = data.drop('Customer Name', axis = 1)

    data['Date of Review'] = pd.to_datetime(data['Date of Review'])
    data['Year of Review'] = data['Date of Review'].fillna(datetime.now()).apply(lambda x: x.strftime('%Y'))
    data['Year of Review'] = pd.to_numeric(data['Year of Review']) 

    return data


def generate_bigrams(tokens):
    return list(zip(tokens[:-1], tokens[1:]))

def generate_trigrams(tokens):
    return list(zip(tokens[:-2], tokens[1:-1], tokens[2:]))

def generate_plot(token_list, ngram_type = 'token', top_ngrams = 10):
    if ngram_type == 'token':
        flat_token_list = [token for sublist in token_list for token in sublist]
        token_counter = collections.Counter(flat_token_list)
        most_common = token_counter.most_common(top_ngrams)

    elif ngram_type == 'bigram':
        bigram_list = [generate_bigrams(tokens) for tokens in token_list]
        flat_bigram_list = [bigram for sublist in bigram_list for bigram in sublist]
        bigram_counter = collections.Counter(flat_bigram_list)
        most_common = bigram_counter.most_common(top_ngrams)

    elif ngram_type == 'trigram':
        trigram_list = [generate_trigrams(tokens) for tokens in token_list]
        flat_trigram_list = [trigram for sublist in trigram_list for trigram in sublist]
        trigram_counter = collections.Counter(flat_trigram_list)
        most_common = trigram_counter.most_common(top_ngrams)
    
    else:
        print('Please provide a n-gram type between 1 and 3')

    word_counts = {}

    for gram,count in most_common:
        word_counts[' '.join(gram)] = count
        
    wordcloud = WordCloud(background_color="white").generate_from_frequencies(word_counts)
    return wordcloud.to_image()