class sep_token:
    def __init__(self, sentence):
        self.sentence = sentence
    def sentence_token(self):
        seq_sentence = []
        token = ""
        previous_ponctuation = False
        for i in self.sentence:
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

if __name__ == '__main__':
    test = "Oui, j'ai passé une bonne nuit, merci... Et toi ?"
    toto = sep_token(test)
    print(toto.sentence_token())
            
