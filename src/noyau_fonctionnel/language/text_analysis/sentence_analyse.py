from parse import parse

class sentence_analyse():
    def __init__(self, check_list_word=[], check_list_sentence=[]):
        self.par = parse()
        self.check_list_word = check_list_word
        self.check_list_sentence = check_list_sentence

    def count_same_word(self, sentence):
        cpt_same_word = 0
        list_sentence = self.par.return_token_sentence(sentence = sentence)
        stem_check_list = []
        for i in self.check_list_word:
            list_int = self.par.return_stem(i)
            for j in list_int:
                stem_check_list.append(j)
        for i in list_sentence:
            token_sentence_stem = self.par.return_stem(i)
            for j in token_sentence_stem:
                for k in stem_check_list:
                    if j == k:
                        cpt_same_word += 1 
        return cpt_same_word
    
    def count_similar_sentence(self, sentence):
        cpt_similar_sentence = 0
        list_sentence = self.par.return_token_sentence(sentence = sentence)
        for i in list_sentence:
            for j in self.check_list_sentence:
                if self.par.compare_sentences(i, j, 0.1):
                    cpt_similar_sentence += 1
        return cpt_similar_sentence

if __name__ == '__main__':
    sentences = "Bonjour, je vais super bien ! Et toi ? Tu me manques..."
    list_word = ["bien", "super", "top", "oui"]
    list_sentence = ["Bien", "je vais bien, merci", "Oui, ca va", "J'ai passe une bonne nuit"]
    analyse = sentence_analyse(check_list_word=list_word, check_list_sentence=list_sentence)
    nb_word = analyse.count_same_word(sentences)
    print("nombre de mots identiques :", nb_word)
    nb_sentence = analyse.count_similar_sentence(sentences)
    print("nombre de phrases similaires :", nb_sentence)