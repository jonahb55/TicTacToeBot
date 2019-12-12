from enum import Enum
import random


class Allele(Enum):
    """Represents a single allele."""
    DOMINANT = "A"
    RECESSIVE = "a"


class Gene(Enum):
    """Represents a single gene (two alleles)."""
    HOMOZYGOUS_RECESSIVE = (Allele.RECESSIVE, Allele.RECESSIVE)
    HETEROZYGOUS = (Allele.DOMINANT, Allele.RECESSIVE)
    HOMOZYGOUS_DOMINANT = (Allele.DOMINANT, Allele.DOMINANT)


class Genome:
    """Represents a series of genes."""
    genes = ()

    def __init__(self, source=None, gametes=None, random_len=None, text=None):
        self.genes = ()
        if source != None:
            self.genes = source
            return
        if gametes != None:
            gene_lookup = {
                (Allele.RECESSIVE, Allele.RECESSIVE): Gene.HOMOZYGOUS_RECESSIVE,
                (Allele.DOMINANT, Allele.RECESSIVE): Gene.HETEROZYGOUS,
                (Allele.RECESSIVE, Allele.DOMINANT): Gene.HETEROZYGOUS,
                (Allele.DOMINANT, Allele.DOMINANT): Gene.HOMOZYGOUS_DOMINANT,
            }
            for i in range(len(gametes[0])):
                self.genes += (gene_lookup[(gametes[0][i], gametes[1][i])],)
            return
        if random_len != None:
            for i in range(random_len):
                self.genes += (random.choice(list(Gene)),)
            return
        if text != None:
            text_lookup = {
                "aa": Gene.HOMOZYGOUS_RECESSIVE,
                "Aa": Gene.HETEROZYGOUS,
                "AA": Gene.HOMOZYGOUS_DOMINANT
            }
            self.genes = ()
            for genetext in text.split("-"):
                self.genes += (text_lookup[genetext],)
            return

    def text(self):
        """Provides a text representation of the genome."""
        genes_text = []
        for gene in self.genes:
            genes_text.append(gene.value[0].value + gene.value[1].value)
        return "-".join(genes_text)

    def gamete(self):
        """Provides a series of alleles from the genome."""
        gamete = ()
        for gene in self.genes:
            gamete += (gene.value[random.getrandbits(1)],)
        return gamete
