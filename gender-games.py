#!/usr/bin/env python3
from gender import gender_words
from make_embeddings import get_model
from data import Data
import numpy as np

model = get_model()
masculine_words = [w[0] for w in gender_words]
masculine_embs = model.encode(masculine_words)
feminine_words = [w[1] for w in gender_words]
feminine_embs = model.encode(feminine_words)

all_embeddings = [*masculine_embs, *feminine_embs]
all_words = [*masculine_words, * feminine_words]

data = Data(all_words, all_embeddings)
data.initialize_faiss()

feminine_to_masculine = masculine_embs - feminine_embs
f2m_avg = np.mean(feminine_to_masculine, axis=0)
sims = data.find_similar_verse_ids(feminine_embs[0])

print(sims)
sims = data.find_similar_verse_ids(feminine_embs[0] + f2m_avg)

print(sims)
