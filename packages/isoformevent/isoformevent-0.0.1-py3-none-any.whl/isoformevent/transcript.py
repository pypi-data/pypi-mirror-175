class Transcript:
    def __init__(self, trancript_id, chrom_loc, protein_id, CDS):
        self.trancript_id = trancript_id
        self.chrom_loc = chrom_loc
        self.protein_id = protein_id
        self.relative_loc = []
        self.CDS = CDS
        self.CDS_loc = []
    
    def calculate_relative_loc(self):
        x = self.chrom_loc
        y = []
        delta = x[1] - x[0]
        y = [1, 1 + delta]
        for i in range(1,int(len(x)/2)):
            delta = x[2*i+1] - x[2*i] 
            y.append(y[2*i-1]+1)
            y.append(y[2*i] + delta)
        self.relative_loc = y

    def calculate_CDS_loc(self):
        x = copy.deepcopy(self.chrom_loc)
        y = self.relative_loc
        cds = self.CDS
        i_a = 1
        i_b = len(y) - 2
        delta_a = 0
        delta_b = 0
        for k in range(len(y)):
            if (cds[0] <= y[i_a]):
                i_a -= 1
                delta_a = cds[0] - y[i_a]
                break
            i_a += 1
        for k in range(len(y)):
            if (cds[1] >= y[i_b]):
                i_b += 1
                delta_b = cds[1] - y[i_b]
                break
            i_b -= 1
        z = x[i_a:i_b+1]
        z[0] = z[0] + delta_a
        z[-1] = z[-1] + delta_b
        self.CDS_loc = z
