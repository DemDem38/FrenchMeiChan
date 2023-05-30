# to split sentence
import spacy
# to have the list of stop words
from nltk.corpus import stopwords

class parse():

    def __init__(self):
        self.stop_word = set(stopwords.words('french')) # french stop words

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

    def return_token_sentence(self, sentence):
        # 1 token = 1 sentence
        doc = nlp(sentence)
        return [X.text for X in doc.sents]

if __name__ == '__main__':
    test = "oui, j'ai passé une bonne nuit, merci... Et toi ?"
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

    print(sep_sentence[0])