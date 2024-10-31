# -*- coding: utf-8 -*-
"""Fake new detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_MGQwl8NmiUq8Len3Ke7Cclidvl1_Q1s
"""

!pip install tensorflow pandas numpy nltk scikit-learn

!pip install tensorflow

import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load datasets
true_news_df = pd.read_csv('true.csv')
fake_news_df = pd.read_csv('fake.csv')

# Label and combine data
true_news_df['label'] = 1
fake_news_df['label'] = 0
combined_df = pd.concat([true_news_df, fake_news_df], ignore_index=True).sample(frac=1, random_state=42)
combined_df = combined_df[['text', 'label']]

# Clean text
nltk.download('stopwords')
stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

combined_df['cleaned_text'] = combined_df['text'].apply(clean_text)

# Tokenization and Padding
MAX_NB_WORDS = 10000  # Increased vocabulary size
MAX_SEQUENCE_LENGTH = 150  # Increased sequence length

tokenizer = Tokenizer(num_words=MAX_NB_WORDS)
tokenizer.fit_on_texts(combined_df['cleaned_text'])
X = tokenizer.texts_to_sequences(combined_df['cleaned_text'])
X = pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)
y = combined_df['label'].values

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam

# Define fine-tuned LSTM model
model = Sequential()
model.add(Embedding(input_dim=MAX_NB_WORDS, output_dim=128, input_length=MAX_SEQUENCE_LENGTH))
model.add(Dropout(0.3))  # Higher dropout to prevent overfitting
model.add(LSTM(128, return_sequences=True))  # First LSTM layer with return_sequences
model.add(BatchNormalization())
model.add(LSTM(64))  # Second LSTM layer
model.add(Dropout(0.3))
model.add(Dense(1, activation='sigmoid'))

# Compile model with lower learning rate
model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.0005), metrics=['accuracy'])
print(model.summary())

# Set early stopping criteria
early_stop = EarlyStopping(monitor='val_accuracy', patience=3, restore_best_weights=True)

# Train the model
history = model.fit(X_train, y_train, epochs=2, batch_size=64, validation_data=(X_test, y_test), callbacks=[early_stop], verbose=1)

from sklearn.metrics import accuracy_score, classification_report

# Predict and evaluate
y_pred = (model.predict(X_test) > 0.5).astype("int32")

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))