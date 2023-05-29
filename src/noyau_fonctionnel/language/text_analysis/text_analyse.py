# to split sentence
import spacy
# to have the list of stop words
from nltk.corpus import stopwords

test = "Oui, j'ai passé une bonne nuit, merci"

def return_token(sentence):
    # split sentence to list of token
    doc = nlp(sentence)
    # return each token
    return [X.text for X in doc]

def clean_tokens(stopW, tokens):
    clean_tok = []
    for token in tokens:
        if token not in stopW:
            clean_tok.append(token)

    return clean_tok


nlp = spacy.load("fr_core_news_sm")
stopW = set(stopwords.words('french'))
tok = return_token(test)

clean_tok = clean_tokens(stopW,tok)

print(clean_tok)