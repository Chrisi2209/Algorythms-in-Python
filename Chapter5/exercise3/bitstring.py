

Bit = int

class BitString:
    def __init__(self, start_value: int):
        self.bitstring: int = start_value
    
    @property
    def length(self) -> int:
        return len(bin(self.bitstring)) - 2
    
    @property
    def binstring(self) -> str:
        """binstring starts with lsb"""
        a = bin(self.bitstring)
        # ignore negatives
        if a[0] == "-":
            return a[3:][::-1]
        a = a[2:][::-1]
        return a
    
    @property
    def binrep(self) -> str:
        return bin(self.bitstring)[2:]

    
    def append(self, bits: int) -> None:
        self.bitstring <<= len(bin(bits)) - 2
        self.bitstring |= bits
    
    def pop(self, index: int = -1) -> Bit:
        """
        pops with index 0 representing lsb
        """
        if index < 0:
            index = self.length + index
        
        popped: Bit = self[index]
        self.bitstring = int(self.binstring[:index] + self.binstring[index+1:], base=2)
        return popped
    
    def invert(self, index: int) -> None:
        self[index] = 0 if self[index] else 1
    
    def __getitem__(self, index) -> int:
        workstring = self.binstring
        if type(index) == slice:
            workstring = workstring[::-1].zfill(max(index.start, index.stop) + 1)[::-1]
            return int(workstring[index.start:index.stop:index.step][::-1], base=2)

        workstring = workstring[::-1].zfill(index + 1)[::-1]
        return int(workstring[index])
    
    def __setitem__(self, index: int, newvalue: Bit):
        if self[index] != newvalue:
            if self[index] == 1:
                self.bitstring -= 2**index
            else:
                self.bitstring += 2**index
    
    def __iter__(self):
        self.current = -1
        return self

    def __next__(self) -> int:
        try:
            self.current += 1
            return self[self.current]
        except IndexError:
            raise StopIteration

