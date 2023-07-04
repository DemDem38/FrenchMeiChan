#from parse import parse

def count_same_word(check_list_word, sentence, par):
    cpt_same_word = 0
    list_sentence = par.return_token_sentence(sentence = sentence)
    stem_check_list = []
    for i in check_list_word:
        list_int = par.return_stem(i)
        for j in list_int:
            stem_check_list.append(j)
    for i in list_sentence:
        token_sentence_stem = par.return_stem(i)
        for j in token_sentence_stem:
            for k in stem_check_list:
                if j == k:
                    cpt_same_word += 1 
    return cpt_same_word

def count_similar_sentence(check_list_sentence, sentence, par):
    cpt_similar_sentence = 0
    list_sentence = par.return_token_sentence(sentence = sentence)
    for i in list_sentence:
        for j in check_list_sentence:
            if par.compare_sentences(i, j, 0.1):
                cpt_similar_sentence += 1
    return cpt_similar_sentence

if __name__ == '__main__':
    sentences = "Bonjour, je vais super bien ! Et toi ? Tu me manques..."
    list_word = ["bien", "super", "top", "oui"]
    list_sentence = ["Bien", "je vais bien, merci", "Oui, ca va", "J'ai passe une bonne nuit"]
    nb_word = count_same_word(list_word, sentences)
    print("nombre de mots identiques :", nb_word)
    #nb_sentence = count_similar_sentence(list_sentence, sentences)
    #print("nombre de phrases similaires :", nb_sentence)