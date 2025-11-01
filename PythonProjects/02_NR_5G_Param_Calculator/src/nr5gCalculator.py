import sys
import logging
from nr5gmodule import NR5GMenu
import nr5gmodule as nrmod

# ---------------------- Logging Setup ----------------------
logging.basicConfig(filename="nr5gcalc.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_result(label, result):
    logging.info(f"{label}: {result}")

# ---------------------- Input Validation ----------------------
def safe_int_input(prompt, min_val=None, max_val=None):
    try:
        val = int(input(prompt))
        if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
            raise ValueError
        return val
    except ValueError:
        range_msg = ""
        if min_val is not None and max_val is not None:
            range_msg = f" (Expected range: {min_val}–{max_val})"
        elif min_val is not None:
            range_msg = f" (Minimum: {min_val})"
        elif max_val is not None:
            range_msg = f" (Maximum: {max_val})"
        print(f"❌ Invalid input. Please enter a valid integer{range_msg}.\n")
        return None

# ---------------------- Case Functions ----------------------
def case_one():
    arfcn = safe_int_input("Enter NR ARFCN: ", 0, 3279165)
    if arfcn is not None:
        freq = nrmod.get_nr_Freq_from_nr_Arfcn(arfcn)
        print(f"NR ARFCN = {arfcn} ➡ NR Frequency = {freq} MHz\n")
        log_result("ARFCN ➡ Frequency", freq)

def case_two():
    freq = safe_int_input("Enter NR Frequency (MHz): ", 410, 71000)
    if freq is not None:
        arfcn = nrmod.get_nr_Arfcn_from_nr_Freq(freq)
        print(f"NR Frequency = {freq} MHz ➡ NR ARFCN = {arfcn}\n")
        log_result("Frequency ➡ ARFCN", arfcn)

def case_three():
    freq = safe_int_input("Enter NR Frequency (MHz): ", 410, 71000)
    if freq is not None:
        bandlist = nrmod.get_nr_Bands_from_nr_Freq(freq)
        print(f"NR Frequency = {freq} MHz ➡ Band List = {bandlist}\n")
        log_result("Frequency ➡ Band List", bandlist)

def case_four():
    arfcn = safe_int_input("Enter NR ARFCN: ", 0, 3279165)
    if arfcn is not None:
        bandlist = nrmod.get_nr_Bands_from_nr_Arfcn(arfcn)
        print(f"NR ARFCN = {arfcn} ➡ Band List = {bandlist}\n")
        log_result("ARFCN ➡ Band List", bandlist)

def case_five():
    band = input("Enter NR Band (e.g., n78): ")
    duplex = nrmod.get_duplex_mode_from_nr_Band(band)
    print(f"NR Band = {band} ➡ Duplex Type = {duplex}\n")
    log_result("Band ➡ Duplex", duplex)

def case_six():
    band = input("Enter NR Band: ")
    direction = input("Enter Direction (ul/dl): ").lower()
    arfcn_range = nrmod.get_nr_ArfcnRange_from_nr_Band(band, direction)
    print(f"NR Band = {band} ➡ ARFCN Range = {arfcn_range}\n")
    log_result("Band ➡ ARFCN Range", arfcn_range)

def case_seven():
    band = input("Enter NR Band: ")
    direction = input("Enter Direction (ul/dl): ").lower()
    freq_range = nrmod.get_nr_Freqrange_from_nr_Band(band, direction)
    print(f"NR Band = {band} ➡ Frequency Range = {freq_range} MHz\n")
    log_result("Band ➡ Frequency Range", freq_range)

def case_eight():
    gscn = safe_int_input("Enter NR GSCN (0–26639): ", 0, 26639)
    if gscn is not None:
        freq = nrmod.get_nr_Freq_from_nr_GSCN(gscn)
        print(f"GSCN = {gscn} ➡ NR Frequency = {freq} MHz\n")
        log_result("GSCN ➡ Frequency", freq)

def case_nine():
    freq = safe_int_input("Enter NR Frequency (MHz): ", 410, 71000)
    if freq is not None:
        gscn = nrmod.get_nr_GSCN_from_nr_Freq(freq)
        print(f"NR Frequency = {freq} MHz ➡ GSCN = {gscn}\n")
        log_result("Frequency ➡ GSCN", gscn)

def case_ten():
    band = input("Enter NR Band: ")
    gscn_range = nrmod.get_nr_GSCNRange_from_nr_Band(band)
    print(f"NR Band = {band} ➡ GSCN Range = {gscn_range}\n")
    log_result("Band ➡ GSCN Range", gscn_range)

def case_eleven():
    numerology = safe_int_input("Enter Numerology (0–3): ", 0, 3)
    if numerology is not None:
        spacing = nrmod.get_NRsubcarrier_spacing_from_numerology(numerology)
        print(f"Numerology = {numerology} ➡ Subcarrier Spacing = {spacing} KHz\n")
        log_result("Numerology ➡ SCS", spacing)

def case_twelve():
    numerology = safe_int_input("Enter Numerology (0–4): ", 0, 4)
    if numerology is None:
        return
    spacing = nrmod.get_NRsubcarrier_spacing_from_numerology(numerology)
    bandwidth = safe_int_input("Enter Channel Bandwidth (MHz): ", 1)
    if bandwidth is not None:
        prbs = nrmod.get_nr_NumberOfPRBs(bandwidth, spacing)
        print(f"Bandwidth = {bandwidth} MHz ➡ Number of PRBs = {prbs}\n")
        log_result("PRB Calculation", prbs)

def case_default():
    print("❌ Invalid choice. Please enter a number between 1 and 12.\n")

# ---------------------- Menu Dispatcher ----------------------
switcher = {
    NR5GMenu.ARFCN_TO_FREQ: case_one,
    NR5GMenu.FREQ_TO_ARFCN: case_two,
    NR5GMenu.FREQ_TO_BANDLIST: case_three,
    NR5GMenu.ARFCN_TO_BANDLIST: case_four,
    NR5GMenu.BAND_TO_DUPLEX: case_five,
    NR5GMenu.BAND_TO_ARFCN_RANGE: case_six,
    NR5GMenu.BAND_TO_FREQ_RANGE: case_seven,
    NR5GMenu.GSCN_TO_FREQ: case_eight,
    NR5GMenu.FREQ_TO_GSCN: case_nine,
    NR5GMenu.BAND_TO_GSCN_RANGE: case_ten,
    NR5GMenu.NUMEROLOGY_TO_SCS: case_eleven,
    NR5GMenu.PRB_CALCULATION: case_twelve
}

# ---------------------- Main Calculator Loop ----------------------
def nr5GCalculator():
    """
    Displays the 5G NR calculator menu and handles user input.
    Dispatches to the appropriate case function based on selection.
    """
    menu = '''
==============================================================
                  📡 5G NR CALCULATOR MENU
==============================================================
 1. ARFCN ➡ Frequency
 2. Frequency ➡ ARFCN
 3. Frequency ➡ Band List
 4. ARFCN ➡ Band List
 5. Band ➡ Duplex Type
 6. Band ➡ ARFCN Range
 7. Band ➡ Frequency Range
 8. GSCN ➡ Frequency
 9. Frequency ➡ GSCN
10. Band ➡ GSCN Range
11. Numerology ➡ Subcarrier Spacing
12. PRB Calculation (Numerology + Bandwidth)
--------------------------------------------------------------
 h. Help     q. Quit
==============================================================
    '''
    while True:
        print(menu)
        choice_raw = input("Select an option (1–12 or h/q): ").lower()

        if choice_raw == "q":
            print("✅ Exiting 5G NR Calculator. Goodbye!\n")
            break
        elif choice_raw == "h":
            print("📘 Help: Choose a number from 1 to 12 to perform a calculation.\n")
            continue

        try:
            choice = int(choice_raw)
            func = switcher.get(NR5GMenu(choice), case_default)
            func()
        except (ValueError, KeyError):
            case_default()

# ---------------------- Program Entry Point ----------------------
def main():
    """
    Entry point for the 5G NR Calculator.
    Supports optional '--test' mode for quick validation.
    """
    print("\n🧮 Welcome to the 5G NR Calculator\n")
    if "--test" in sys.argv:
        print("🧪 Running test mode...\n")

        # Sample test cases with hardcoded inputs
        print("🔹 ARFCN ➡ Frequency")
        freq = nrmod.get_nr_Freq_from_nr_Arfcn(620000)
        print(f"NR ARFCN = 620000 ➡ NR Frequency = {freq} MHz\n")

        print("🔹 Frequency ➡ ARFCN")
        arfcn = nrmod.get_nr_Arfcn_from_nr_Freq(3500)
        print(f"NR Frequency = 3500 MHz ➡ NR ARFCN = {arfcn}\n")

        print("🔹 PRB Calculation")
        spacing = nrmod.get_NRsubcarrier_spacing_from_numerology(2)
        prbs = nrmod.get_nr_NumberOfPRBs(100, spacing)
        print(f"Bandwidth = 100 MHz ➡ PRBs = {prbs}\n")

        print("✅ Test mode completed.\n")
        return

    nr5GCalculator()

if __name__ == "__main__":
    main()
