from keras.models import Sequential, load_model, save_model
from keras.layers import Dense
from keras import optimizers


def get_model(filename):
    try:
        model = load_model(filename)
        return model
    except FileNotFoundError:
        return create_model(filename)


def create_model(filename):
    model = Sequential()
    model.add(Dense(1024, input_dim=769))
    model.add(Dense(1024, activation='sigmoid'))
    model.add(Dense(3, activation='softmax'))
    sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='mean_squared_error', optimizer=sgd)

    if(filename):
        save_model(model, filename)

    return model
