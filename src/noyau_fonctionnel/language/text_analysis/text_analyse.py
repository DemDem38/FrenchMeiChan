import spacy
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sep_token import sep_token
import numpy as np

class parse():

    def __init__(self):
        self.stop_word = set(stopwords.words('french')) # french stop words
        self.snowball_stemmer = SnowballStemmer(language='french')
    
    def return_token_word(self, sentence):
        # split sentence to list of token (1 token = 1 word)
        doc = nlp(sentence)
        return [X.text for X in doc]

    def clean_tokens_word(self, tokens):
        # remove stop words on token list
        clean_tok = []
        for token in tokens:
            if token not in self.stop_word:
                clean_tok.append(token)
        return clean_tok
    
    def return_stem(self, sentence):
        doc = nlp(sentence)
        return [self.snowball_stemmer.stem(X.text) for X in doc]

    def return_token_sentence(self, sentence):
        # 1 token = 1 sentence
        tok = sep_token(sentence)
        return tok.sentence_token()
    
    def return_NER(self, sentence):
        # Named Entity Recognise
        doc = nlp(sentence)
        return [(X.text, X.label_) for X in doc.ents]
    
    def return_POS(self, sentence):
        # Part Of Speech
        doc = nlp(sentence)
        return [(X, X.pos_) for X in doc]

    def return_word_embedding(self, sentence):
        # value of tokens
        doc = nlp(sentence)
        return [(X.vector) for X in doc]
    
    def return_mean_embedding(self, sentence):
        # value of sentence
        doc = nlp(sentence)
        return np.mean([(X.vector) for X in doc], axis=0)
    
    def compare_sentences(self, sentence1, sentence2, dist):
        dist = self.return_mean_embedding(sentence1)-self.return_mean_embedding(sentence2)
        if(dist > -dist and dist < dist):
            return True
        else:
            return False

if __name__ == '__main__':
    test = "oui, MeiChan, j'ai passé une bonne nuit dans mon lit a Kobe, merci... Et toi ?"
    nlp = spacy.load("fr_core_news_sm")

    stopW = set(stopwords.words('french'))

    par = parse()

    sep_sentence = par.return_token_sentence(test)

    tok0 = par.return_token_word(sep_sentence[0])
    tok1 = par.return_token_word(sep_sentence[1])
    #tok2 = par.return_token_word(sep_sentence[2])

    clean_tok0 = par.clean_tokens_word(tok0)
    clean_tok1 = par.clean_tokens_word(tok1)
    #clean_tok2 = par.clean_tokens_word(tok2)

    stem_tok0 = par.return_stem(sep_sentence[0])
    stem_tok1 = par.return_stem(sep_sentence[1])
    #stem_tok2 = par.return_stem(sep_sentence[2])

    ner = par.return_NER(test)

    pos = par.return_POS(test)

    print(ner)