class IntWrapper:
    def __init__(self, bits: int):
        self.bits: int = bits
        self.current: int = None  # used for the iterator

    def set_bits(self, bits: int):
        self.bits = bits

    def __getitem__(self, index: int):
        return int(bin(self.bits)[index + 2])  # +2 for the removal of 0b

    def __iter__(self):
        self.current = -1
        return self

    def __next__(self) -> int:
        try:
            self.current += 1
            return self[self.current]
        except IndexError:
            raise StopIteration

    def __add__(self, val: str):
        self.bits = int(bin(self.bits)[2:] + val)

    def bit_length(self):
        """shorthand for self.bits.bit_length()"""
        return self.bits.bit_length()

    def compressed_gene(self, genes: str) -> None:
        """ 
        compresses the genes into a bit sequence that stores the genes in 2 instead 8 bits
        A = 0b00
        C = 0b01
        G = 0b10
        T = 0b11
        """
        
        self.bits = 1  # add sentinel
        for gene in genes:
            self.bits <<= 2
            # if gene == "A":  # not necessary because it always adds 0s at the front
                # self.bits |= 0b00
            if gene == "C":
                self.bits |= 0b01
            elif gene == "G":
                self.bits |= 0b10
            elif gene == "T":
                self.bits |= 0b11

    
    def decompress_gene(self) -> str:
        """
        decompresses the genes that have been stored in the bits of this object
        returns a string that contains the genes A, C, G and T.
        """

        it = iter(self)
        next(it)  # throw away the sentinel

        gene_string: str = ""

        for _ in range(1, self.bit_length(), 2):
            gene = (next(it) << 1) + next(it)

            if gene == 0b00:
                gene_string += "A"
            elif gene == 0b01:
                gene_string += "C"
            elif gene == 0b10:
                gene_string += "G"
            elif gene == 0b11:
                gene_string += "T"

            else:
                raise ValueError(f"Invalid Bits: {bin(gene)}")
        
        return gene_string
        

