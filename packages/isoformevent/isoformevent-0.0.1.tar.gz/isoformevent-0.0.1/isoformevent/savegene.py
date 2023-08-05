import os
import pickle

def save_gene_object(obj, gene_name, path='GeneObjects'):
    if not os.path.exists(path):
       os.makedirs(path)
    with open(path+'/'+gene_name+'.pkl', 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
