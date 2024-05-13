import umap.umap_ as umap
import plotly.express as px
from pathlib import Path
import pandas as pd
import sys
import re
from book import Book
from data import data_from_file

colors = [
    "Bisque",
    "CadetBlue",
    "Chocolate",
    "CornflowerBlue",
    "Crimson",
    "DarkOliveGreen",
    "DarkOrchid",
    "DarkSalmon",
    "DarkSeaGreen",
    "DarkSlateBlue",
    "DarkSlateGray",
    "DarkTurquoise",
    "DeepPink",
    "DeepSkyBlue",
    "FireBrick",
    "GoldenRod",
    "Indigo",
    "LavenderBlush",
    "MediumAquaMarine",
    "MediumOrchid"
]

def verse_id_to_color(verse_id):
    splits = re.split(r'-|:',verse_id)
    index = int(splits[0])
    return colors[index % len(colors)]

def plot_umap_with_labels(data, texts, n_neighbors=10, min_dist=0.1):

    reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, random_state=42, n_jobs=1, n_components=3)

    # Fit and transform the data
    embedding = reducer.fit_transform(data)

    df = pd.DataFrame({
        'embedding_x': embedding[:, 0],
        'embedding_y': embedding[:, 1],
        'embedding_z': embedding[:, 2],
        #'text': texts
        'text': map(lambda x: x[:80], texts), # Truncate strings to the first 10 characters
        'color': [verse_id_to_color(t) for t in texts]
    })

    fig = px.scatter_3d(df, x='embedding_x', y='embedding_y', z='embedding_z', 
                        color='color',
                        # color= [colors[i%20] for i in range(0, len(embedding[:,0]))],
                        # color_continuous_scale=px.colors.sequential.Viridis,
                     hover_data={'embedding_x': False, 'embedding_y': False, 'embedding_z': False, 'text': True},
                    )
    fig.update_layout(
        title={
            'text': "Embeddings grouping",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
    )
    
    fig.show()
    
# fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
# fig.show()
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('viz all books')
        all_embeddings_file = Path('embeddings/embeddings-all.mpk')
        data = data_from_file(all_embeddings_file)
        verses = data.ids
    else:
        book_idx = int(sys.argv[1])
        book = Book(book_idx)
        print(f'viz {book.title}')
        book.init_embeddings()
        data = book.data
        verses = [f'{id} {book.verses[id]}' for id in data.ids]
    plot_umap_with_labels(data.embeddings, verses)