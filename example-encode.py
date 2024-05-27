import time
print('getting get_model')
from make_embeddings import get_model
print('getting model')
model = get_model()
print('encoding')

t0 = time.time()
embedding = model.encode(['hellow world'])
t1 = time.time()
print(embedding)
print(f'time to encode: {t1-t0}')
