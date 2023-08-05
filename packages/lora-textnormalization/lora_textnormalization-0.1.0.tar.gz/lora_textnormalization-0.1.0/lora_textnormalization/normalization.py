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
    punctuations = "?:!.,;"
    for word in filtered_sentence:
        if word in punctuations:
            filtered_sentence.remove(word)

    return filtered_sentence


if __name__ == '__main__':
    filtered = spacy_process("More and more financial services organizations are leaning on AWS's scale, performance, and breadth of AI capabilities to drive innovation and customer success, said Vasi Philomin, vice president of AI Services, Amazon Web Services. Establishing highly efficient contact centers requires significant automation, the ability to scale, and a mechanism for active learning through customer feedback. By using Amazon Lex, in collaboration with Talkdesk, WaFd has built a strong foundation of providing excellent customer service by helping them respond to customers faster, resolve requests more easily, and improve overall customer experiences.")
    print(filtered)
