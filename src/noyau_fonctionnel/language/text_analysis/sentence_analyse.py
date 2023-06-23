from parse import parse

class sentence_analyse():
    def __init__(self, check_list):
        self.par = parse()
        self.check_list = check_list

    def compare_resonse(self, sentence):
        cpt_same_word = 0
        list_sentence = self.par.return_token_sentence(sentence = sentence)
        stem_check_list = []
        for i in self.check_list:
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



if __name__ == '__main__':
    sentences = "Bonjour, je vais super bien ! Et toi ? Tu me manques..."
    list = ["bien", "super", "top", "oui"]
    analyse = sentence_analyse(list)
    nb = analyse.compare_resonse(sentences)
    print(nb)