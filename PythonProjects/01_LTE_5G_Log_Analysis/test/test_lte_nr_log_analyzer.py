#############################################################################
###  Author       : Sanjeet Prasad                                       ###
###  Email        : sanjeet8.23@gmail.com                                ###
###  Description  : Unit tests for LTE & NR Log Analyzer                 ###
###                 - Validates signal extraction and message parsing    ###
###                 - Confirms NR band and combination parsing           ###
###  Date         : 22-10-2025                                           ###
###  Framework    : pytest                                               ###
#############################################################################

# 📦 Ensure the project root is in Python's module search path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.lte_nr_log_analyzer import LTELogAnalyzer, NRLogAnalyzer

# -------------------- LTE Tests --------------------

def test_lte_signal_extraction(tmp_path):
    """
    ✅ Test RSRP and CQI extraction from LTE logs.
    Simulates a log file with two signal entries.
    """
    log = tmp_path / "lte.txt"
    log.write_text("RSRP = -60 ,CQI = 25\nRSRP = -55 ,CQI = 20")
    analyzer = LTELogAnalyzer(str(log))
    analyzer.extract_signal_values()
    assert analyzer.rsrp_values == ["RSRP = -60", "RSRP = -55"]
    assert analyzer.cqi_values == ["CQI = 25", "CQI = 20"]

def test_lte_message_block(tmp_path, capsys):
    """
    ✅ Test LTE message block parsing from MSG2 to MSG3.
    Captures printed output and checks for expected lines.
    """
    log = tmp_path / "lte_msg.txt"
    log.write_text("MSG2\nLine A\nLine B\nMSG3\nLine C")
    analyzer = LTELogAnalyzer(str(log))
    analyzer.search_lte_messages()
    output = capsys.readouterr().out
    assert "MSG2" in output
    assert "Line A" in output
    assert "Line B" in output
    assert "MSG3" not in output  # MSG3 marks the end, not printed

# -------------------- NR Tests --------------------

def test_nr_band_extraction(tmp_path):
    """
    ✅ Test NR band list extraction.
    Simulates a UE capability log with two bandNR entries.
    """
    log = tmp_path / "nr.txt"
    log.write_text("bandNR: 78\nbandNR: 79\nsupportedBandCombinationList")
    analyzer = NRLogAnalyzer(str(log))
    analyzer.extract_supported_bands()
    assert analyzer.supported_band_list == ["bandNR: 78", "bandNR: 79"]

def test_nr_band_combinations(tmp_path):
    """
    ✅ Test NR band combination parsing.
    Simulates a capability block with two bands grouped under one combo.
    """
    log = tmp_path / "nr_combo.txt"
    log.write_text("supportedBandCombinationList\nbandNR: 78\nbandNR: 79\nfeatureSetCombination\nappliedFreqBandListFilter")
    analyzer = NRLogAnalyzer(str(log))
    analyzer.extract_band_combinations()
    assert analyzer.band_combinations == [["bandNR: 78", "bandNR: 79"]]
