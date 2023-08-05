import spacy

nlp = spacy.load('en_core_web_sm')


def spacy_process(text):
    doc = nlp(text)

    # Tokenization and lemmatization are done with the spacy nlp pipeline commands
    lemma_list = []
    for token in doc:
        lemma_list.append(token.lemma_)

    # Filter the stopword
    filtered_sentence = []
    for word in lemma_list:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence.append(word)

    # Remove punctuation
    punctuations = "?:!.,,;'()®_--$%^&*#@<>/\\"
    for word in filtered_sentence:
        if word in punctuations:
            filtered_sentence.remove(word)

    rm_special = []
    for tk in filtered_sentence:
        tk = tk.strip()
        if tk != '"' and len(tk) > 0 and not tk.isnumeric():
            rm_special.append(tk)
    return rm_special
