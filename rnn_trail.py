# -*- coding: utf-8 -*-
"""RNN_Trail.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JXvCktcKK5jBlfRNBO3ESAMrUERbnQ4c
"""

import numpy as np
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense, Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical

# Generating some example sequential data
sentences = ['I love learning','I love python','I hate school',
             'Recurrent Neural Networks are powerful']
# Tokenizing the words
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)
total_words = len(tokenizer.word_index) + 1

# Creating input sequences and their corresponding next words
input_sequences = []
for sentence in sentences:
    tokenized_sentence = tokenizer.texts_to_sequences([sentence])[0]
    for i in range(1, len(tokenized_sentence)):
        n_gram_sequence = tokenized_sentence[:i+1]
        input_sequences.append(n_gram_sequence)

# Padding sequences for consistent input size
max_sequence_length = max([len(seq) for seq in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre')

# Creating input and output data
X, y = input_sequences[:, :-1], input_sequences[:, -1]
y = to_categorical(y, num_classes=total_words)

# Building a simple RNN model
model = Sequential()
model.add(Embedding(input_dim=total_words, output_dim=50, input_length=max_sequence_length-1))
model.add(SimpleRNN(100, return_sequences=True))
model.add(SimpleRNN(100))
model.add(Dense(total_words, activation='softmax'))

# Compiling the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Training the model
model.fit(X, y, epochs=50, verbose=2)

# Generating text using the trained model
seed_text = input("Enter the starting word: ")
next_words = int(input("Enter how many words to predict: "))

for _ in range(next_words):
    tokenized_seed = tokenizer.texts_to_sequences([seed_text])[0]
    tokenized_seed = pad_sequences([tokenized_seed], maxlen=max_sequence_length-1, padding='pre')
    predicted_word_index = np.argmax(model.predict(tokenized_seed), axis=-1)
    predicted_word = tokenizer.index_word[predicted_word_index[0]]
    seed_text += " " + predicted_word

print(seed_text)