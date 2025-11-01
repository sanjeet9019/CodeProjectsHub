#############################################################################
###  Author       : Sanjeet Prasad                                       ###
###  Email        : sanjeet8.23@gmail.com                                ###
###  Description  : LTE & NR Log Analyzer                                ###
###                 - LTE: Extracts RSRP/CQI and message flow            ###
###                 - NR: Parses UE Capability for supported bands       ###
###  Date         : 22-10-2025                                           ###
###  Interpreter  : Python 3.11.0                                        ###
#############################################################################

import re
import os
import argparse
import logging
from tabulate import tabulate

# -------------------- Logging Setup --------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# -------------------- LTE Analyzer --------------------

class LTELogAnalyzer:
    """
    Analyzes LTE network logs to extract signal metrics and decode message flow.
    """

    def __init__(self, logfile_path):
        self.logfile_path = logfile_path
        self.rsrp_values = []
        self.cqi_values = []
        self.msg_start = "MSG2"
        self.msg_stop = "MSG3"

    def extract_signal_values(self):
        """
        Extracts RSRP and CQI values using regular expressions.
        """
        if not os.path.exists(self.logfile_path):
            logging.error(f"LTE log file not found: {self.logfile_path}")
            return

        rsrp_pattern = r"RSRP = -?\d+"
        cqi_pattern = r"CQI = -?\d+"
        logging.info(f"Reading LTE log file: {self.logfile_path}")

        with open(self.logfile_path, "r") as logfile:
            for line in logfile:
                rsrp_match = re.findall(rsrp_pattern, line)
                cqi_match = re.findall(cqi_pattern, line)
                if rsrp_match and cqi_match:
                    self.rsrp_values.append(rsrp_match[0])
                    self.cqi_values.append(cqi_match[0])

        if self.rsrp_values:
            print("\n📶 RSRP & CQI Values:")
            print(tabulate(zip(self.rsrp_values, self.cqi_values), headers=["RSRP", "CQI"]))
        else:
            logging.warning("No RSRP/CQI values found.")

    def search_lte_messages(self):
        """
        Searches for LTE message block from MSG2 to MSG3 and prints it.
        """
        if not os.path.exists(self.logfile_path):
            logging.error(f"LTE log file not found: {self.logfile_path}")
            return

        found = False
        logging.info(f"Searching for LTE message block: {self.msg_start} → {self.msg_stop}")

        with open(self.logfile_path, "r") as logfile:
            for line in logfile:
                if re.search(rf"\b{self.msg_start}\b", line):
                    found = True
                    print(f"\n📨 Found '{self.msg_start}' message:")
                    print(line.strip())

                    for next_line in logfile:
                        if self.msg_stop in next_line:
                            print("\n🛑 End of message block.\n")
                            break
                        print(next_line.strip())
                    break

        if not found:
            logging.warning(f"Message '{self.msg_start}' not found.")

    def run_analysis(self):
        """
        Executes the full LTE analysis pipeline.
        """
        logging.info("Starting LTE Log Analysis...")
        self.extract_signal_values()
        self.search_lte_messages()
        logging.info("LTE Log Analysis Completed.")

# -------------------- NR Analyzer --------------------

class NRLogAnalyzer:
    """
    Analyzes UE Capability logs to extract supported NR bands and combinations.
    """

    def __init__(self, logfile_path):
        self.logfile_path = logfile_path
        self.supported_band_list = []
        self.band_combinations = []

    def extract_supported_bands(self):
        """
        Extracts NR band identifiers from UE Capability logs.
        """
        if not os.path.exists(self.logfile_path):
            logging.error(f"NR capability file not found: {self.logfile_path}")
            return

        band_pattern = r"bandNR: \d+"
        logging.info(f"Reading NR capability file: {self.logfile_path}")

        with open(self.logfile_path, "r") as file:
            for line in file:
                bands = re.findall(band_pattern, line)
                if bands:
                    self.supported_band_list.append(bands[0])
                if "supportedBandCombinationList" in line:
                    break

        if self.supported_band_list:
            print("\n📶 Supported NR Bands:")
            print(tabulate([[b] for b in self.supported_band_list], headers=["BandNR"]))
        else:
            logging.warning("No NR bands found.")

    def extract_band_combinations(self):
        """
        Extracts NR band combinations from UE Capability logs.
        """
        if not os.path.exists(self.logfile_path):
            logging.error(f"NR capability file not found: {self.logfile_path}")
            return

        band_pattern = r"bandNR: \d+"
        current_combo = []
        logging.info("Parsing NR band combinations...")

        with open(self.logfile_path, "r") as file:
            for line in file:
                if "supportedBandCombinationList" in line:
                    for line in file:
                        bands = re.findall(band_pattern, line)
                        if bands:
                            current_combo.append(bands[0])
                        if "featureSetCombination" in line:
                            if current_combo:
                                self.band_combinations.append(current_combo)
                                current_combo = []
                        if "appliedFreqBandListFilter" in line:
                            break
                    break

        if self.band_combinations:
            print("\n🔗 Band Combinations:")
            for i, combo in enumerate(self.band_combinations, 1):
                print(f"Combo {i}: {', '.join(combo)}")
        else:
            logging.warning("No band combinations found.")

    def run_analysis(self):
        """
        Executes the full NR capability analysis pipeline.
        """
        logging.info("Starting 5G NR Capability Analysis...")
        self.extract_supported_bands()
        self.extract_band_combinations()
        logging.info("NR Log Analysis Completed.")

# -------------------- Program Entry Point --------------------

# This block ensures that the script runs only when executed directly,
# not when imported as a module. It's the standard Python convention
# for defining the "main" starting point of execution.
# When run, it triggers both LTE and NR log analysis pipelines.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LTE & NR Log Analyzer")
    parser.add_argument("--lte", type=str, help="Path to LTE log file")
    parser.add_argument("--nr", type=str, help="Path to NR capability file")
    args = parser.parse_args()

    logging.info("📊 Running Combined LTE + NR Log Analyzer")

    # Default paths if no arguments are provided
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DEFAULT_LTE = os.path.join(PROJECT_ROOT, "..", "data", "LTENetworkLogs.txt")
    DEFAULT_NR = os.path.join(PROJECT_ROOT, "..", "data", "UECapabilityInfo.txt")

    if not args.lte and not args.nr:
        args.lte = DEFAULT_LTE
        args.nr = DEFAULT_NR

    if args.lte:
        lte = LTELogAnalyzer(args.lte)
        lte.run_analysis()

    if args.nr:
        nr = NRLogAnalyzer(args.nr)
        nr.run_analysis()
