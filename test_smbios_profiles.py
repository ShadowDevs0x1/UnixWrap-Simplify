import contextlib
import io
import unittest

from Scripts.datasets.mac_model_data import mac_devices, get_mac_device_by_name
from Scripts.smbios import SMBIOS
from Scripts.utils import Utils


class AppleSiliconProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.smbios = SMBIOS.__new__(SMBIOS)
        cls.smbios.utils = Utils()

    @staticmethod
    def hardware_report(platform, cores):
        return {
            "Motherboard": {"Name": "Test system", "Platform": platform},
            "CPU": {"Core Count": str(cores), "Codename": "Test"},
            "GPU": {"Test GPU": {"Device Type": "Integrated GPU"}},
        }

    def test_apple_silicon_product_ids_are_unique_and_covered(self):
        profiles = [device for device in mac_devices if device.architecture == "Apple Silicon"]
        identifiers = [device.name for device in profiles]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(get_mac_device_by_name("Mac17,5").cpu, "A18 Pro")
        self.assertEqual(get_mac_device_by_name("Mac18,5").cpu, "M6")
        self.assertEqual(get_mac_device_by_name("MacBookPro18,3").cpu, "M1 Pro")
        self.assertIn("Mac17,15", identifiers)

    def test_golden_gate_defaults_to_hardware_tiered_apple_profiles(self):
        cases = (
            ("Laptop", 2, "Mac17,5"),
            ("Laptop", 4, "MacBookAir10,1"),
            ("Laptop", 6, "Mac14,2"),
            ("Laptop", 12, "Mac17,3"),
            ("Laptop", 16, "Mac17,7"),
            ("Desktop", 4, "Macmini9,1"),
            ("Desktop", 8, "Mac15,4"),
            ("Desktop", 12, "Mac18,5"),
            ("Desktop", 20, "Mac17,15"),
        )
        for platform, cores, expected in cases:
            with self.subTest(platform=platform, cores=cores):
                result = self.smbios.select_smbios_model(self.hardware_report(platform, cores), "26.0.0")
                self.assertEqual(result, expected)

    def test_pre_golden_gate_selection_remains_intel_based(self):
        report = self.hardware_report("Desktop", 12)
        self.assertEqual(self.smbios.select_smbios_model(report, "25.0.0"), "MacPro7,1")

    def test_apple_silicon_serial_generation_does_not_call_macserial(self):
        self.smbios.check_macserial = lambda: self.fail("Apple Silicon profiles must skip macserial")
        self.smbios.run = lambda *_: self.fail("Apple Silicon profiles must skip macserial")
        with contextlib.redirect_stdout(io.StringIO()):
            generated = self.smbios.generate_smbios("Mac17,5")
        self.assertEqual(generated["SystemProductName"], "Mac17,5")
        self.assertEqual(generated["SystemSerialNumber"], "A00000000009")


if __name__ == "__main__":
    unittest.main()
