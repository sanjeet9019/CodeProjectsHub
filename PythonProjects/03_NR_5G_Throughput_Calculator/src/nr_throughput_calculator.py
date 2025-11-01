#############################################################################
###  Author       : Sanjeet Prasad                                       ###
###  Email        : sanjeet8.23@gmail.com                                ###
###  Description  : 5G NR Data Throughput Calculator (OOP Version)       ###
###                 Interactive CLI using NRThroughputCalculator class   ###
###  Date         : 03-05-2023                                           ###
###  Interpreter  : Python 3.11.0                                        ###
#############################################################################

import os
import threading
import nrarfcn as NR_5G
from PIL import Image

nrthrougput = '''##################### 5G Throughput Calculation Formula ##########################
INPUT PARAMETERS =
J - NUMBER OF CC 
V - MIMO LAYERS
Qm - MODULATION ORDER
f - SCALING FACTOR 
FDD = 1 , TDD = 0.76
Rmax - CODING RATE (0.93) 
Nprb - Number of PRBs 
Ts - OFDM SYMBOL DURATION
Ts = 0.001 / (14 * SubcarrierSpacing)
OH - OVERHEAD
[0.14] FR1 DL, [0.08] FR1 UL, [0.18] FR2 DL, [0.10] FR2 UL

Total PRBs = (BW(MHz) * 1000) / SubcarrierSpacing / 12
ActualNumPRBs = Total PRBs - 4

THROUGHPUT = CCs × [MIMO × Q × f × R × ((N × 12) / Ts) × (1 - OH)] / 1,000,000
##################################################################################'''

class NRThroughputCalculator:
    def __init__(self):
        self.num_cc = 0
        self.num_mimo = 0
        self.mod_order = 0
        self.band_type = ''
        self.scaling_factor = 0.0
        self.coding_rate = 0.93
        self.numerology = 0
        self.channel_bw = 0
        self.subcarrier_spacing = 0
        self.num_prbs = 0
        self.symbol_duration = 0
        self.overhead = 0.14
        self.throughput = 0.0

    def get_subcarrier_spacing(self, numerology):
        return 15 * (2 ** numerology)

    def get_num_prbs(self, bandwidth_mhz, subcarrier_spacing):
        total_prbs = (bandwidth_mhz * 1000) / subcarrier_spacing / 12
        return int(total_prbs) - 4

    def calculate_symbol_duration(self, subcarrier_spacing):
        return 0.001 / (14 * subcarrier_spacing)

    def calculate_throughput(self):
        numerator = self.num_cc * (
            self.num_mimo * self.mod_order * self.scaling_factor * self.coding_rate *
            ((self.num_prbs * 12) / self.symbol_duration) * (1 - self.overhead)
        )
        self.throughput = numerator / 1_000_000
        return self.throughput

    def _show_image(self):
        try:
            image_path = os.path.join(os.path.dirname(__file__), "nr_throughput_formula.jpg")
            image = Image.open(image_path)
            image.show()
        except Exception as e:
            print(f"⚠️ Unable to display image: {e}")

    def display_formula_image(self):
        thread = threading.Thread(target=self._show_image)
        thread.start()

    def display_parameters(self):
        print("\n********** Input Parameters **********\n")
        print(f"{'NUMBER OF CC':<24}: {self.num_cc}")
        print(f"{'MIMO LAYERS':<24}: {self.num_mimo}")
        print(f"{'MODULATION ORDER':<24}: {self.mod_order}")
        print(f"{'SCALING FACTOR':<24}: {self.scaling_factor}")
        print(f"{'CODING RATE':<24}: {self.coding_rate}")
        print(f"{'SUBCARRIER SPACING':<24}: {self.subcarrier_spacing} KHz")
        print(f"{'CHANNEL BANDWIDTH':<24}: {self.channel_bw} MHz")
        print(f"{'NUMBER OF PRBs':<24}: {self.num_prbs}")
        print(f"{'SYMBOL DURATION':<24}: {self.symbol_duration:.8f} sec")
        print(f"{'OVERHEAD':<24}: {self.overhead}")
        print("\n**************************************\n")

# -------------------- Utility Functions --------------------

def get_int(prompt, min_val=0, max_val=1000):
    while True:
        try:
            value = input(prompt).strip()
            if value == "":
                print("⚠️ Input cannot be empty. Please enter a number.")
                continue
            value = int(value)
            if value < min_val or value > max_val:
                print(f"⚠️ Value must be between {min_val} and {max_val}.")
                continue
            return value
        except ValueError:
            print("⚠️ Invalid input. Please enter a valid integer.")

def get_band_type():
    while True:
        value = input("ENTER BAND TYPE (FDD/TDD): ").strip().upper()
        if value in ["FDD", "TDD"]:
            return value
        print("⚠️ Invalid band type. Please enter 'FDD' or 'TDD'.")

# -------------------- Program Entry Point --------------------

def main():
    calc = NRThroughputCalculator()

    print("📡 5G NR Data Throughput Calculation\n")
    calc.display_formula_image()
    print(nrthrougput)

    calc.num_cc = get_int("ENTER NUMBER OF CC: ")
    calc.num_mimo = get_int("ENTER NUMBER OF MIMO LAYERS: ")
    calc.mod_order = get_int("ENTER MODULATION ORDER: ")
    calc.band_type = get_band_type()
    calc.scaling_factor = 1.0 if calc.band_type == "FDD" else 0.76

    print("\n🧮 Calculate Number of PRBs")
    calc.numerology = get_int("ENTER NR NUMEROLOGY (0–4): ", 0, 4)
    calc.subcarrier_spacing = calc.get_subcarrier_spacing(calc.numerology)
    calc.channel_bw = get_int("ENTER CHANNEL BANDWIDTH (MHz): ")
    calc.num_prbs = calc.get_num_prbs(calc.channel_bw, calc.subcarrier_spacing)
    calc.symbol_duration = calc.calculate_symbol_duration(calc.subcarrier_spacing)

    calc.overhead = 0.14  # Default for FR1 DL

    calc.display_parameters()

    result = calc.calculate_throughput()
    print(f"📶 Estimated 5G NR Throughput = {result:.4f} Mbps")

if __name__ == "__main__":
    main()
