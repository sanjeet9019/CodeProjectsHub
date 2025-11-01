#############################################################################
###  Author       : Sanjeet Prasad                                       ###
###  Email        : sanjeet8.23@gmail.com                                ###
###  Description  : Unit tests for 5G NR Throughput Calculator            ###
###                 Validates core methods of NRThroughputCalculator      ###
###                 using Python's unittest framework                     ###
###  Date         : 23-10-2025                                           ###
###  Interpreter  : Python 3.11.0                                        ###
#############################################################################

import unittest
from src.nr_throughput_calculator import NRThroughputCalculator

class TestNRThroughputCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = NRThroughputCalculator()

    def test_01_subcarrier_spacing(self):
        print("Test 01: Subcarrier spacing for numerology 0–3")
        self.assertEqual(self.calc.get_subcarrier_spacing(0), 15)
        self.assertEqual(self.calc.get_subcarrier_spacing(1), 30)
        self.assertEqual(self.calc.get_subcarrier_spacing(2), 60)
        self.assertEqual(self.calc.get_subcarrier_spacing(3), 120)
        print("Test 01 passed\n")

    def test_02_num_prbs(self):
        print("Test 02: PRB calculation for 100 MHz @ 30 kHz")
        prbs = self.calc.get_num_prbs(bandwidth_mhz=100, subcarrier_spacing=30)
        expected = int((100 * 1000) / 30 / 12) - 4
        self.assertEqual(prbs, expected)
        print(f"Test 02 passed: Calculated PRBs = {prbs}\n")

    def test_03_symbol_duration(self):
        print("Test 03: Symbol duration for 30 kHz spacing")
        duration = self.calc.calculate_symbol_duration(30)
        expected = 0.001 / (14 * 30)
        self.assertAlmostEqual(duration, expected, places=8)
        print(f"Test 03 passed: Symbol duration = {duration:.8f} sec\n")

    def test_04_throughput_calculation(self):
        print("Test 04: Throughput calculation with realistic parameters")
        self.calc.num_cc = 1
        self.calc.num_mimo = 4
        self.calc.mod_order = 6
        self.calc.scaling_factor = 1.0
        self.calc.coding_rate = 0.93
        self.calc.num_prbs = 100
        self.calc.symbol_duration = self.calc.calculate_symbol_duration(30)
        self.calc.overhead = 0.14

        throughput = self.calc.calculate_throughput()
        self.assertGreater(throughput, 0)
        self.assertIsInstance(throughput, float)
        print(f"Test 04 passed: Throughput = {throughput:.4f} Mbps\n")

    def test_05_zero_throughput(self):
        print("Test 05: Zero throughput edge case")
        self.calc.num_cc = 0
        self.calc.num_mimo = 0
        self.calc.mod_order = 0
        self.calc.scaling_factor = 0.0
        self.calc.coding_rate = 0.0
        self.calc.num_prbs = 0
        self.calc.symbol_duration = 1
        self.calc.overhead = 0.0

        throughput = self.calc.calculate_throughput()
        self.assertEqual(throughput, 0.0)
        print("Test 05 passed: Throughput = 0.0 Mbps\n")

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(TestNRThroughputCalculator))

    print("\nTest Summary:")
    print(f"Total tests run   : {result.testsRun}")
    print(f"Tests passed      : {len(result.successes) if hasattr(result, 'successes') else result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Tests failed      : {len(result.failures)}")
    print(f"Tests with errors : {len(result.errors)}")
