from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from gene import Gene
from transcript import Transcript

def draw_coding_sequence(id, x, currentAxis):
    d = 0.075
    for i in range(int(len(x)/2)):
        x1 = x[2*i]
        x2 = x[2*i+1]
        currentAxis.add_patch(Rectangle((x1 - d, id - d), x2-x1, 2*d,alpha=1,facecolor='grey'))
    return currentAxis

def draw_protein_sequence(id, x, color, currentAxis):
    d = 0.2
    for i in range(int(len(x)/2)):
        x1 = x[2*i]
        x2 = x[2*i+1]
        currentAxis.add_patch(Rectangle((x1 - d, id - d), x2-x1, 2*d,alpha=1,facecolor=color))
    return currentAxis

def draw_gene(gene):
    transcripts = gene.transcripts
    n = len(transcripts)
    fig,ax = plt.subplots()
    currentAxis = plt.gca()
    plt.title(' / '.join(gene.gene_name))
    plt.autoscale()
    plt.ylim(0, n + 1)
    plt.figure()
    color_ids = []
    colors = ['slateblue',  'firebrick', 'springgreen', 'goldenrod', 'palevioletred']
    i = 1
    for t in transcripts:
        if t.protein_id not in color_ids:
            color_ids.append(t.protein_id)
    for c_id in color_ids:
        for t in transcripts:
            if t.protein_id == c_id:
                p_id = color_ids.index(t.protein_id) % len(colors)
                currentAxis = draw_coding_sequence(i, t.chrom_loc, currentAxis)
                currentAxis = draw_protein_sequence(i, t.CDS_loc, colors[p_id], currentAxis)
                i += 1
    plt.rcParams['figure.figsize'] = [10, 5]
    plt.show()
