import Model
import Processing


if __name__ == '__main__':
    filename = 'example_4.pdf'
    preprocessed_file = Processing.preprocess_file(filename)
    x = Model.create_input_vector(filename)
    classifications = Model.classify(x)

    data = Processing.readPDF(filename)

    sentences = Processing.get_sentences(data)
    for i in range(0, len(sentences)):
        print(Processing.format_sentence(sentences[i]))
        print(classifications[i])

    # Model.train_model(x, classifications)
