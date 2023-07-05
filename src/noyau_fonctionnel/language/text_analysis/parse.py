import spacy
#import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import numpy as np

#nltk.download('stopwords')

class parse():

    def __init__(self):
        self.stop_word = set(stopwords.words('french')) # french stop words
        self.snowball_stemmer = SnowballStemmer(language='french')
        self.nlp = spacy.load("fr_core_news_sm")

    def return_token_word(self, sentence):
        # split sentence to list of token (1 token = 1 word)
        doc =  self.nlp(sentence)
        return [X.text for X in doc]

    def clean_tokens_word(self, tokens):
        # remove stop words on token list
        clean_tok = []
        for token in tokens:
            if token not in self.stop_word:
                clean_tok.append(token)
        return clean_tok
    
    def return_stem(self, sentence):
        doc =  self.nlp(sentence)
        return [self.snowball_stemmer.stem(X.text) for X in doc]

    def return_token_sentence(self, sentence):
        seq_sentence = []
        token = ""
        previous_ponctuation = False
        for i in sentence:
            if i == "." or i == "!" or i == "?":
                token = token+i
                if not previous_ponctuation:
                    previous_ponctuation = True
            else:
                if previous_ponctuation:
                    seq_sentence.append(token)
                    previous_ponctuation = False
                    token = ""
                else:
                    token = token+i
        seq_sentence.append(token)
        return seq_sentence
    
    def return_NER(self, sentence):
        # Named Entity Recognise
        doc =  self.nlp(sentence)
        return [(X.text, X.label_) for X in doc.ents]
    
    def return_POS(self, sentence):
        # Part Of Speech
        doc =  self.nlp(sentence)
        return [(X, X.pos_) for X in doc]

    def return_word_embedding(self, sentence):
        # value of tokens
        doc =  self.nlp(sentence)
        return [(X.vector) for X in doc]
    
    def return_mean_embedding(self, sentence):
        # value of sentence
        doc =  self.nlp(sentence)
        return np.mean([(X.vector) for X in doc])
    
    def compare_sentences(self, sentence1, sentence2, dist):
        calc_dist = self.return_mean_embedding(sentence1)-self.return_mean_embedding(sentence2)
        print(calc_dist)
        #if(calc_dist > -dist and calc_dist < dist):
        #    return True
        #else:
        #    return False

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

    mean_sentences = par.return_mean_embedding(test)

    mean_word = par.return_word_embedding("hello")

    print(mean_word)