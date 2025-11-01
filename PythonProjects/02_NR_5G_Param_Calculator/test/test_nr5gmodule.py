"""
#############################################################################
###  Author       : Sanjeet Prasad                                       ###
###  Email        : sanjeet8.23@gmail.com                                ###
###  Description  : Unit tests for NR 5G Parameter Module                ###
###                 Validates ARFCN, Frequency, Band, GSCN, PRB logic    ###
###  Created On   : 22-10-2025                                           ###
###  Framework    : pytest                                               ###
#############################################################################
"""

import sys
import os

# Add the src/ directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import nr5gmodule as mod


# ---------------------- ARFCN ↔ Frequency ----------------------

def test_arfcn_to_freq_valid():
    assert mod.get_nr_Freq_from_nr_Arfcn(620000) > 0

def test_freq_to_arfcn_valid():
    assert mod.get_nr_Arfcn_from_nr_Freq(3500) > 0

def test_arfcn_to_freq_invalid():
    assert mod.get_nr_Freq_from_nr_Arfcn(-1) == -1

def test_freq_to_arfcn_invalid():
    assert mod.get_nr_Arfcn_from_nr_Freq(100) == -1

# ---------------------- Band ↔ Duplex ----------------------

def test_band_to_duplex_valid():
    assert mod.get_duplex_mode_from_nr_Band("n78") in ["FDD", "TDD"]

def test_band_to_duplex_invalid():
    assert mod.get_duplex_mode_from_nr_Band("x99") == -1

# ---------------------- Band ↔ ARFCN/Frequency/GSCN Range ----------------------

def test_band_to_arfcn_range_valid():
    assert isinstance(mod.get_nr_ArfcnRange_from_nr_Band("n78", "dl"), tuple)

def test_band_to_freq_range_valid():
    assert isinstance(mod.get_nr_Freqrange_from_nr_Band("n78", "ul"), tuple)

def test_band_to_gscn_range_valid():
    assert isinstance(mod.get_nr_GSCNRange_from_nr_Band("n78"), tuple)

# ---------------------- Frequency ↔ Band List ----------------------

def test_freq_to_bandlist_valid():
    assert isinstance(mod.get_nr_Bands_from_nr_Freq(3500), list)

def test_arfcn_to_bandlist_valid():
    assert isinstance(mod.get_nr_Bands_from_nr_Arfcn(620000), list)

# ---------------------- GSCN ↔ Frequency ----------------------

def test_gscn_to_freq_valid():
    assert mod.get_nr_Freq_from_nr_GSCN(3000) > 0

def test_freq_to_gscn_valid():
    assert mod.get_nr_GSCN_from_nr_Freq(3500) > 0

# ---------------------- Numerology ↔ SCS ----------------------

def test_numerology_to_scs_valid():
    assert mod.get_NRsubcarrier_spacing_from_numerology(2) == 60

# ---------------------- PRB Calculation ----------------------

def test_prb_calculation_valid():
    prbs = mod.get_nr_NumberOfPRBs(100, 30)
    assert prbs > 0

