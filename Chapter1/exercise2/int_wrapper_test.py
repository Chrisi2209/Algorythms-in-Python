import unittest
import int_wrapper
import random

class IntWrapperTest(unittest.TestCase):

    def test_iterator(self):
        # test1
        num = int_wrapper.IntWrapper(12)

        bits_of_num = (1, 1, 0, 0)
        for i, bit in enumerate(num):
            # print(i, ":",  bit, "=", bits_of_num[i])
            self.assertEqual(bit, bits_of_num[i])

        # test2
        num = int_wrapper.IntWrapper(1043082)

        bits_of_num = [int(digit) for digit in "11111110101010001010"]  # bits from website converter
        for i, bit in enumerate(num):
            # print(i, ":",  bit, "=", bits_of_num[i])
            self.assertEqual(bit, bits_of_num[i])


    def test_compress(self):
        wrapper = int_wrapper.IntWrapper(None)
        
        possible_genes = ["A", "C", "G", "T"]
        genes = "".join([i for i in random.choices(possible_genes, k=40)])


        wrapper.compressed_gene(genes)
        self.assertEqual(wrapper.decompress_gene(), genes)


if __name__ == '__main__':
    unittest.main()
