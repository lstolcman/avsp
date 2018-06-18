import unittest
from lab2 import DGIM


class TestFromBigFile(unittest.TestCase):
    def setUp(self):
        self.dgim = DGIM(100)

    def test_small_part(self):
        self.dgim.add_stream('01111101101111010101100111111101101010111011011111111100111101111011101111111001')
        self.dgim.add_stream('11110111101101100110111011111110110010111111100011001011100100111101011111110111')
        self.dgim.add_stream('01111110101100110101101101010111011111101001001110111001110101000111111111001101')
        self.dgim.add_stream('10111111011101111100011011011111101101101101111111111110011000011011110111111110')
        self.dgim.add_stream('01111111111111111111101110111111001110110111101110001110111101101101101111110001')
        self.dgim.add_stream('00011111111010111111010111011000111100111111101111110000011011111011101111101010')
        self.dgim.add_stream('11101111100110001010110111101001111101100110011111110101000110111111101101011100')
        self.dgim.add_stream('11111101011110111111111111111111101111101011111011001111010110111111111111110101')
        self.dgim.add_stream('10001111111111010100111111111111111101001101111100111011100111011101111111110110')
        self.dgim.add_stream('11011101110101010111111111111100011011101111010001101011101111111111110111010011')
        self.dgim.add_stream('11100111001110011001100111011011110110111010111011111100111010011110010111111000')
        self.assertEqual(self.dgim.calculate_ones(53), 30)
        self.dgim.add_stream('11110110011010101101111111101111100011101111111110110001011100100111111101011111')
        self.assertEqual(self.dgim.calculate_ones(84), 63)
        self.dgim.add_stream('10111011110101110111110010111101101011010010011001010001101001100111101011110111')
        self.assertEqual(self.dgim.calculate_ones(76), 49)
        self.dgim.add_stream('11010111111111000101110011101011111111111011111011000101111111110010111001100111')
        self.assertEqual(self.dgim.calculate_ones(81), 50)
        self.dgim.add_stream('11011111111101111110111111101001100011101011111011100111101110011000110111111111')
        self.assertEqual(self.dgim.calculate_ones(68), 45)
        self.dgim.add_stream('10111111011100011110111111111111100110011101111101111111111111110111111011100101')
        self.assertEqual(self.dgim.calculate_ones(76), 68)
        self.assertEqual(self.dgim.calculate_ones(75), 68)
        self.dgim.add_stream('11111100111111101010101011011100110010111100010110011101101000100111011111100011')
        self.dgim.add_stream('10101001101111111111100111100001111011010110011101101010100100111111110000110111')
        self.assertEqual(self.dgim.calculate_ones(25), 13)
        self.dgim.add_stream('00110011101101010011100110101011111011110011011111111001111010000111111001101010')
        self.dgim.add_stream('01111011111110101000011001111111010010111010001110110111110101001011001000100111')
        self.dgim.add_stream('11111111011111111001010110111011111111011101111111111110110001011101111011110001')
        self.assertEqual(self.dgim.calculate_ones(94), 72)
        self.dgim.add_stream('01111101011111100111100010110111101110111111010110110110011111011010010111011011')
        self.dgim.add_stream('10111111111100110111011110111111011111101101111111011111110110101101011111110111')
        self.dgim.add_stream('01111110011111111101001011110011011110001110011111111111111011010111011001110111')
        self.dgim.add_stream('10111111111111110101110111011111111011111010110101011110111001110111111111111000')
        self.assertEqual(self.dgim.calculate_ones(94), 87)
        self.assertEqual(self.dgim.calculate_ones(50), 31)
        self.assertEqual(self.dgim.calculate_ones(23), 19)


class TestFromLabPDF(unittest.TestCase):
    def setUp(self):
        self.dgim = DGIM(100)

    def test_1st_pass(self):
        self.dgim.add_stream('1010101101')
        self.dgim.add_stream('1110101011')
        self.assertEqual(self.dgim.calculate_ones(20), 11)

    def test_2nd_pass(self):
        self.dgim.add_stream('1000010010')
        self.assertEqual(self.dgim.calculate_ones(3), 0)


class TestFromMyExamples1(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        window_size = 10
        dgim = DGIM(window_size)
        dgim.add_stream('0110110110')
        self.assertEqual(dgim.calculate_ones(k=10), 5)

    def test_2(self):
        window_size = 10
        dgim = DGIM(window_size)
        dgim.add_stream('01101')
        self.assertEqual(dgim.buckets, {1:[5], 2:[3]})
        dgim.add_stream('1011')
        self.assertEqual(dgim.buckets, {1:[8,9], 2:[3,6]})
        self.assertEqual(dgim.calculate_ones(k=4), 3)

    def test_3(self):
        window_size = 4
        dgim = DGIM(window_size)
        dgim.add_stream('1111')
        self.assertEqual(dgim.buckets, {1:[3,4], 2:[2]})
        dgim.add_stream('1')
        self.assertEqual(dgim.buckets, {1:[5], 2:[2,4]})
        dgim.add_stream('0')
        self.assertEqual(dgim.calculate_ones(k=3), 2)
        self.assertEqual(dgim.buckets, {1:[5], 2:[4]})

    def test_4(self):
        window_size = 4
        dgim = DGIM(window_size)
        dgim.add_stream('111110')
        self.assertEqual(dgim.calculate_ones(k=3), 2)
        self.assertEqual(dgim.buckets, {1:[5], 2:[4]})


if __name__ == '__main__':
    unittest.main()

