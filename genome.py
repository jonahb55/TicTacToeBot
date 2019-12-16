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
    genes = []

    def __init__(self, text=None, gametes=None, random_len=None):
        self.genes = []
        if text != None:
            text_lookup = {
                "aa": Gene.HOMOZYGOUS_RECESSIVE,
                "Aa": Gene.HETEROZYGOUS,
                "AA": Gene.HOMOZYGOUS_DOMINANT
            }
            for genetext in text.split("-"):
                self.genes.append(text_lookup[genetext])
            return
        if gametes != None:
            gene_lookup = {
                (Allele.RECESSIVE, Allele.RECESSIVE): Gene.HOMOZYGOUS_RECESSIVE,
                (Allele.DOMINANT, Allele.RECESSIVE): Gene.HETEROZYGOUS,
                (Allele.RECESSIVE, Allele.DOMINANT): Gene.HETEROZYGOUS,
                (Allele.DOMINANT, Allele.DOMINANT): Gene.HOMOZYGOUS_DOMINANT,
            }
            for i in range(len(gametes[0])):
                self.genes.append(gene_lookup[(gametes[0][i], gametes[1][i])])
            return
        if random_len != None:
            for i in range(random_len):
                self.genes.append(self.__random_gene())
            return

    def __random_gene(self):
        """Selects a random gene based on accurate weights."""
        return random.choices(population=list(Gene), weights=[0.25, 0.5, 0.25])[0]

    def mutate(self, rate):
        """Randomly replaces genes based on mutation rate."""
        for i in range(len(self.genes)):
            if random.random() < rate:
                choice = self.__random_gene()
                while choice == self.genes[i]:
                    choice = self.__random_gene()
                self.genes[i] = choice

    def text(self):
        """Provides a text representation of the genome."""
        genes_text = []
        for gene in self.genes:
            genes_text.append(gene.value[0].value + gene.value[1].value)
        return "-".join(genes_text)

    def gamete(self):
        """Provides a series of alleles from the genome."""
        gamete = []
        for gene in self.genes:
            gamete.append(gene.value[random.getrandbits(1)])
        return gamete
