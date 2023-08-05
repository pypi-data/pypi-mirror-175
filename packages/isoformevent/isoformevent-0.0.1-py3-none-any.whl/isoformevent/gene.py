class Gene:
    def __init__(self, gene_id, gene_name):
        self.gene_id = gene_id
        self.gene_name = gene_name
        self.transcripts = []
    
    def add_transcript(self, transcript):
        self.transcripts.append(transcript)
