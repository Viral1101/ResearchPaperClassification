# I3-RA : Raxter-PublicationClassifier

The user is able to upload a .pdf file that will be assigned 3 different descritipons : Core, Peripheral, and Other.
The file will be parsed and split into smaller phrases to be designated their descriptions based on how relevant the phrase is to the topic.


Relevancy to each description is determined by a network with input layer size 1024, 2 dense hidden layers also 1024. Output is size 3 with softmax activation. The model searches for the highest used n-grams inside the pdf and seperates them into 3 topics using an LDA (Latent Dirichlet allocation). To obtain n-grams word embedding is used on each sentence to encode and store into a 256 vector. The same is done for the LDA topics. All data is passed through the input layer and results are returned.
