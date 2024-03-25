import pandas as pd
import numpy as np
from pecanpy import node2vec
from gensim.models import Word2Vec

from Constants import Constants
from tqdm import tqdm
from joblib import load, dump

GRAPH_FILE_NAME = Constants.GRAPH_FILE_NAME.value
WEIGHTED = Constants.WEIGHTED.value
DIRECTED = Constants.DIRECTED.value
NUM_WALK = Constants.NUM_WALK.value
WALK_LEN = Constants.WALK_LEN.value


def saveAsEdg(graph):
    edg_graph_path = '../Data/Edg_Graphs_DataFile/' + \
        GRAPH_FILE_NAME.split('.')[0]+'.edg'
    graph.to_csv(edg_graph_path, sep='\t', index=False, header=False)
    print("Edg Graph Saved")
    return edg_graph_path


def walkgenerator(edg_graph_path):
    g = node2vec.SparseOTF(p=1, q=0.5, workers=-1, verbose=True, extend=True)
    g.read_edg(edg_graph_path, weighted=WEIGHTED, directed=DIRECTED)

    walks = g.simulate_walks(num_walks=NUM_WALK, walk_length=WALK_LEN)
    return walks


def train_word2vec(walks):
    model = Word2Vec(walks,  # previously generated walks
                     hs=1,  # tells the model to use hierarchical softmax
                     sg=1,  # tells the model to use skip-gram
                     vector_size=128,  # size of the embedding
                     window=5,
                     min_count=1,
                     workers=4,
                     seed=42)
    model.save('../Model/node2vec_graph_embedding_' +
               GRAPH_FILE_NAME.split('.')[0]+'.model')
    print("Model Weights Saved")
    return model


def saveEmbeddings(graph, model):
    pid_set = set(graph['pid_1'].unique()).union(graph['pid_2'].unique())
    payload = []
    for pid in tqdm(pid_set):
        try:
            payload.append(
                {'pid': pid, 'embedding_vector': model.wv[str(pid)]})
        except:
            print(pid, "Not Exist")
            pass

    embedding_df = pd.DataFrame(payload)
    embedding_df.to_parquet('../Data/Embedding_Data/node2vec_embedding_df_' +
                            GRAPH_FILE_NAME.split('.')[0]+'.parquet', index=False)
    print("Embedding Saved")
    return embedding_df


graph_path = '../Data/ConstructedGraph/{}'.format(GRAPH_FILE_NAME)
graph = pd.read_parquet(graph_path)

print("Graph Read from {}".format(graph_path))
edg_graph_path = saveAsEdg(graph)
walks = walkgenerator(edg_graph_path)
model = train_word2vec(walks)
embedding_df = saveEmbeddings(graph, model)
print(embedding_df.head())
