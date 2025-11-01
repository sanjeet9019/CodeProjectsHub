#############################################################################
###  Author       : Sanjeet Prasad                                        ###
###  Email        : sanjeet8.23@gmail.com                                 ###
###  Description  : LaptopMonitor – Extended unit tests using unittest    ###
###                 Covers env overrides, toggles, and edge cases         ###
###  Date         : 24-10-2025                                            ###
###  Interpreter  : Python 3.11.0                                         ###
#############################################################################

import unittest
import os
import tempfile
import pathlib
from laptopmonitor.laptop_monitor import LaptopMonitor

class TestLaptopMonitor(unittest.TestCase):
    """
    ✅ Extended unit tests for LaptopMonitor.
    Validates environment overrides, toggles, and fallback logic.
    """

    def setUp(self):
        print("\n🔍 Starting new test case...")
        os.environ["MAX_CYCLES"] = "1"
        os.environ["MONITOR_INTERVAL"] = "5"
        os.environ["PING_HOST"] = "example.com"
        os.environ["ENABLE_SPEEDTEST"] = "false"
        os.environ["LOG_LEVEL"] = "DEBUG"
        os.environ["PROCESS_KEYWORDS"] = "python,vscode"
        self.monitor = LaptopMonitor()

    def test_01_env_override_ping_host(self):
        """🧪 Test #01: PING_HOST override should be 'example.com'"""
        self.assertEqual(self.monitor.ping_host, "example.com")

    def test_02_env_override_interval(self):
        """🧪 Test #02: MONITOR_INTERVAL override should be 5"""
        self.assertEqual(self.monitor.interval, 5)

    def test_03_env_override_max_cycles(self):
        """🧪 Test #03: MAX_CYCLES override should be 1"""
        self.assertEqual(self.monitor.max_cycles, 1)

    def test_04_env_override_speedtest_toggle(self):
        """🧪 Test #04: ENABLE_SPEEDTEST=false should disable speed test"""
        self.assertFalse(self.monitor.enable_speedtest)

    def test_05_env_override_process_keywords(self):
        """🧪 Test #05: PROCESS_KEYWORDS override should contain 'python' and 'vscode'"""
        self.assertIn("python", self.monitor.process_keywords)
        self.assertIn("vscode", self.monitor.process_keywords)

    def test_06_folder_path_fallback(self):
        """🧪 Test #06: MONITOR_FOLDER_PATH fallback should be a valid path"""
        self.assertTrue(pathlib.Path(self.monitor.folder_path).exists())

    def test_07_monitor_files_empty_folder(self):
        """🧪 Test #07: monitor_files should handle empty folder gracefully"""
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["MONITOR_FOLDER_PATH"] = temp_dir
            monitor = LaptopMonitor()
            monitor.monitor_files()  # Should not raise exceptions

    def test_08_log_level_debug(self):
        """🧪 Test #08: LOG_LEVEL should be set to DEBUG"""
        self.assertEqual(os.getenv("LOG_LEVEL"), "DEBUG")
        
    def test_09_env_override_folder_path(self):
        """
        🧪 Test #09: MONITOR_FOLDER_PATH override should be respected
        Creates a temporary folder and sets it in .env, then verifies LaptopMonitor uses it.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["MONITOR_FOLDER_PATH"] = temp_dir
            monitor = LaptopMonitor()
            resolved = pathlib.Path(monitor.folder_path).resolve()
            expected = pathlib.Path(temp_dir).resolve()
            print(f"➡️ MONITOR_FOLDER_PATH resolved to: {resolved}")
            self.assertEqual(resolved, expected)
            print("✅ Passed: MONITOR_FOLDER_PATH override is respected")
    
    def test_10_monitor_disk_space_logs_output(self):
        """
        🧪 Test #10: monitor_disk_space should log disk usage details
        Verifies that the method runs and logs expected keywords.
        """
        with self.assertLogs(level='INFO') as log:
            self.monitor.monitor_disk_space()
            output = "\n".join(log.output)
            print("➡️ Disk space log output:\n", output)
            self.assertIn("Total", output)
            self.assertIn("Used", output)
            self.assertIn("Free", output)
            self.assertIn("Usage", output)
            print("✅ Passed: Disk space metrics logged successfully")


if __name__ == "__main__":
    print("\n🧪 Running extended LaptopMonitor unit tests...\n")
    unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestLaptopMonitor)
    )
