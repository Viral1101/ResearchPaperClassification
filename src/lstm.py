import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from keras.wrappers.scikit_learn import KerasClassifier

from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
import re
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder

stop = stopwords.words('english')

data = pd.read_csv('training.csv')
data = data[['abstract', 'mesh']]

data = data[data['mesh'].isin(['Epitopes', 'Immunity, Cellular', 'Staining and Labeling', 'Antibody Formation', 'Genes',
                               'Hydrogen-Ion Concentration', 'Histocompatibility Antigens', 'Electroencephalography',
                               'Antigens', 'HLA Antigens', 'Aging'])]

data['abstract'] = data['abstract'].apply(lambda x: x.lower())
data['mesh'] = data['mesh'].apply(lambda x: x.lower())

data['abstract'] = data['abstract'].apply((lambda x: re.sub('[^a-zA-z0-9\s]', '', x)))
data['abstract'] = data['abstract'].apply((lambda x: ' '.join([word for word in x.split() if word not in stop])))

max_features = 5000
tokenizer = Tokenizer(num_words=max_features, split=' ')
tokenizer.fit_on_texts(data['abstract'].values)
X = tokenizer.texts_to_sequences(data['abstract'].values)
print(X)
X = pad_sequences(X)
print(X)

labelencoder = LabelEncoder()
integer_encoded = labelencoder.fit_transform(data['mesh'])
y = to_categorical(integer_encoded)
X_train, X_test, Y_train, Y_test = train_test_split(X,y, test_size = 0.33, random_state = 42)
print(X_train.shape,Y_train.shape)
print(X_test.shape,Y_test.shape)

embed_dim = 128
lstm_out = 512
out_shape = Y_train.shape[1]

def createmodel():
    model = Sequential()
    model.add(Embedding(max_features, embed_dim,input_length = X.shape[1]))
    model.add(SpatialDropout1D(0.4))
    model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(out_shape, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


labelencoder = LabelEncoder()
integer_encoded = labelencoder.fit_transform(data['mesh'])
y = to_categorical(integer_encoded)
X_train, X_test, Y_train, Y_test = train_test_split(X,y, test_size = 0.33, random_state = 42)
print(X_train.shape,Y_train.shape)
print(X_test.shape,Y_test.shape)

epochs = 10
batch_size = 30

model = createmodel()
model.fit(X_train, Y_train, epochs=epochs, batch_size=batch_size, verbose = 1)
score,acc = model.evaluate(X_test,Y_test,verbose=2,batch_size=batch_size)

model.save('lstm_model.h5')
print(score)
print(acc)
