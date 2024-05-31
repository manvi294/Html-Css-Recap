import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.optim as optim
from torchcrf import CRF
from torch.utils.data import DataLoader, Dataset

# Download necessary NLTK data
nltk.download('punkt')

# Load GloVe embeddings
def load_glove_embeddings(glove_path):
    embeddings_index = {}
    with open(glove_path, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
    return embeddings_index

glove_path = 'glove.6B.100d.txt'  # Adjust path as necessary
embeddings_index = load_glove_embeddings(glove_path)

# Tokenize and encode the dataset
def tokenize_and_encode(texts, labels, embeddings_index, max_len=50):
    X, y = [], []
    for text, label in zip(texts, labels):
        tokens = word_tokenize(text)
        token_ids = [embeddings_index.get(token, np.zeros(100)) for token in tokens]
        if len(token_ids) < max_len:
            token_ids += [np.zeros(100)] * (max_len - len(token_ids))
        X.append(token_ids[:max_len])
        y.append(label.split()[:max_len])
    return np.array(X), y

# Example dataset (replace with your actual data)
data = pd.DataFrame({
    'text': ["number of poor performing ATM in Arizona", "how are my ATM doing today"],
    'labels': ["O O O O B-ATM O B-REGION", "O O O O B-ATM O B-TIME"]
})

# Encode data
X, y = tokenize_and_encode(data['text'].values, data['labels'].values, embeddings_index)
label_map = {"O": 0, "B-ATM": 1, "I-ATM": 2, "B-REGION": 3, "I-REGION": 4, "B-TIME": 5, "I-TIME": 6}
y = [[label_map.get(lbl, 0) for lbl in seq] for seq in y]

# Split data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
