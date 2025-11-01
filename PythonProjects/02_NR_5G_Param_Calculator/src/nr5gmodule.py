"""
#############################################################################
###  Author       : Sanjeet Prasad                                       ###
###  Email        : sanjeet8.23@gmail.com                                ###
###  Description  : NR 5G Parameter Module                               ###
###                 Provides conversion and lookup utilities for         ###
###                 NR ARFCN, Frequency, Band, GSCN, and PRB calculations###
###  Created On   : 03-05-2023                                           ###
###  Interpreter  : Python 3.11.0                                        ###
#############################################################################
"""

import nrarfcn as NR_5G  # External library for NR ARFCN utilities
from enum import IntEnum
# ---------------------- Enum for Menu Choices ----------------------

class NR5GMenu(IntEnum):
    ARFCN_TO_FREQ = 1
    FREQ_TO_ARFCN = 2
    FREQ_TO_BANDLIST = 3
    ARFCN_TO_BANDLIST = 4
    BAND_TO_DUPLEX = 5
    BAND_TO_ARFCN_RANGE = 6
    BAND_TO_FREQ_RANGE = 7
    GSCN_TO_FREQ = 8
    FREQ_TO_GSCN = 9
    BAND_TO_GSCN_RANGE = 10
    NUMEROLOGY_TO_SCS = 11
    PRB_CALCULATION = 12

# ------------------------- 5G Parameter Conversion Functions -------------------------

def get_nr_Freq_from_nr_Arfcn(nrarfcn):
    """Converts NR ARFCN to frequency in MHz"""
    if 0 < nrarfcn < 3279165:
        return NR_5G.get_frequency(nrarfcn)
    print("ENTER VALID NR-ARFCN (0 - 3279165)")
    return -1

def get_nr_Arfcn_from_nr_Freq(nrfreq):
    """Converts NR frequency (MHz) to ARFCN"""
    if 410 < nrfreq < 71000:
        return NR_5G.get_nrarfcn(nrfreq)
    print("ENTER VALID NR-FREQ (410 - 71000 MHz)")
    return -1

def get_nr_Bands_from_nr_Freq(nrfreq):
    """Returns NR band list for given frequency (MHz)"""
    if 410 < nrfreq < 71000:
        return NR_5G.get_bands_by_frequency(nrfreq)
    print("ENTER VALID NR-FREQ (410 - 71000 MHz)")
    return -1

def get_nr_Bands_from_nr_Arfcn(nrarfcn):
    """Returns NR band list for given ARFCN"""
    if 0 < nrarfcn < 3279165:
        return NR_5G.get_bands_by_nrarfcn(nrarfcn)
    print("ENTER VALID NR-ARFCN (0 - 3279165)")
    return -1

def get_duplex_mode_from_nr_Band(nrband):
    """Returns duplex mode (FDD/TDD) for given NR band"""
    temp = nrband
    try:
        nrband_num = int(nrband[1:])
        if (1 <= nrband_num <= 104) or ("n257" <= nrband <= "n263"):
            return NR_5G.get_duplex_mode(temp)
    except:
        pass
    print("ENTER VALID NR BAND Values (n1 - n263)")
    return -1

def get_nr_ArfcnRange_from_nr_Band(nrband, direction):
    """Returns ARFCN range (DL/UL) for a given band"""
    temp = nrband
    try:
        nrband_num = int(nrband[1:])
        if (1 <= nrband_num <= 104) or ("n257" <= nrband <= "n263"):
            return NR_5G.get_nrarfcn_range(temp)
    except:
        pass
    print("ENTER VALID NR BAND Values (n1 - n263)")
    return -1

def get_nr_Freqrange_from_nr_Band(nrband, direction):
    """Returns frequency range (MHz) for a band and direction"""
    temp = nrband
    try:
        nrband_num = int(nrband[1:])
        if (1 <= nrband_num <= 104) or ("n257" <= nrband <= "n263"):
            return NR_5G.get_frequency_range(temp, direction)
    except:
        pass
    print("ENTER VALID NR BAND Values (n1 - n263)")
    return -1

def get_nr_Freq_from_nr_GSCN(nrgscn):
    """Returns frequency for given GSCN"""
    nrgscn = int(nrgscn)
    if 2 <= nrgscn <= 26639:
        return NR_5G.get_frequency_by_gscn(nrgscn)
    print("ENTER VALID GSCN (2 - 26639)")
    return -1

def get_nr_GSCN_from_nr_Freq(nrfreq):
    """Returns GSCN for a given frequency"""
    nrfreq = int(nrfreq)
    if 410 <= nrfreq <= 71000:
        return NR_5G.get_gscn_by_frequency(nrfreq)
    print("ENTER VALID FREQUENCY (410 - 71000 MHz)")
    return -1

def get_nr_GSCNRange_from_nr_Band(nrband):
    """Returns GSCN range for a band"""
    temp = nrband
    try:
        nrband_num = int(nrband[1:])
        if (1 <= nrband_num <= 104) or ("n257" <= nrband <= "n263"):
            return NR_5G.get_gscn_range(temp)
    except:
        pass
    print("ENTER VALID BAND (n1 - n263)")
    return -1

def get_NRsubcarrier_spacing_from_numerology(numerology):
    """Returns subcarrier spacing in kHz for numerology (0–4)"""
    return 15 * (2 ** numerology)

def get_nr_NumberOfPRBs(channelBW, SubcarrierSpacing):
    """Calculates number of physical resource blocks (PRBs)"""
    channelBW_kHz = channelBW * 1000
    totalPRBs = (channelBW_kHz / SubcarrierSpacing) / 12
    return int(totalPRBs) - 4  # Adjusting for guard bands
