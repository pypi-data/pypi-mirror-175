import pandas as pd
import numpy as np
from gene import Gene
from transcript import Transcript

def create_genes(dataset, transcript_id_dataset):
    list_of_genes = []
    genes = np.unique(test_dataset['gene_id'])
    for gene_id in genes:
        gene_dataset = dataset[dataset['gene_id'] == gene_id]
        gene_name = np.unique(transcript_id_dataset[transcript_id_dataset['gene_id'] == gene_id]['gene_name'])
        gene = Gene(gene_id, gene_name)
        transcripts = np.unique(gene_dataset['transcript_id'])
        for transcript_id in transcripts:
            transcript_dataset = gene_dataset[gene_dataset['transcript_id'] == transcript_id]
            chrom_loc = transcript_dataset[transcript_dataset['data_type'] == 'exon'][['x1','x2']].values
            if (transcript_id_dataset[transcript_id_dataset['transcript_id'] == transcript_id]['direction'].tolist()[0] == '-'):
                chrom_loc = np.flipud(chrom_loc)
            chrom_loc = chrom_loc.flatten().astype(int)
            protein_id = transcript_id_dataset[transcript_id_dataset['transcript_id'] == transcript_id]['protein_id'].values[0]
            CDS = transcript_dataset[(transcript_dataset['data_type'] == 'CDS') & (transcript_dataset['source_id'] == 'tappAS')]
            CDS = CDS[['x1','x2']].values[0].astype(int)
            transcript = Transcript(transcript_id, chrom_loc, protein_id, CDS)
            transcript.calculate_relative_loc()
            transcript.calculate_CDS_loc()
            gene.add_transcript(transcript)
        list_of_genes.append(gene)
    return list_of_genes
