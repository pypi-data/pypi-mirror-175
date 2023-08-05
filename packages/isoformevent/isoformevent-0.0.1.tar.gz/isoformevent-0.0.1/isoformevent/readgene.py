import os
import pickle
from pandas import pd

def read_gene_object(gene_name, path='GeneObjects'):
    return pd.read_pickle(path+'/'+gene_name+'.pkl')
