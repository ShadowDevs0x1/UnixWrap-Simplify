import os
import plistlib
import tempfile
import unittest
import zipfile
from unittest import mock

from Scripts.unixwrap_bundle import (
    DEFAULT_BOOT_CFG_SHA256,
    DEFAULT_BOOT_CFG_URL,
    DEFAULT_RAM_IMG_SHA256,
    DEFAULT_RAM_IMG_URL,
    PACKAGE_EFI_PATH,
    UNIXWRAP_BLESS_PATH,
    _read_ipsw_entries,
    stage_unixwrap_bundle,
)


class UnixWrapBundleTests(unittest.TestCase):
    def test_stages_efi_payload_and_bless_override(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            unixwrap_dir = os.path.join(temporary_dir, "UnixWrap")
            result_dir = os.path.join(temporary_dir, "Results")
            os.makedirs(os.path.join(unixwrap_dir, "run"))
            os.makedirs(os.path.join(result_dir, "EFI", "OC"))

            sources = (
                ("BOOTX64.EFI", b"efi"),
                (os.path.join("run", "boot.cfg"), b"boot config"),
                (os.path.join("run", "ram.img"), b"guest image"),
            )
            for relative_path, contents in sources:
                with open(os.path.join(unixwrap_dir, relative_path), "wb") as stream:
                    stream.write(contents)

            config = {"Misc": {"Entries": [{"Name": "Existing", "Path": r"\EFI\Other.efi"}]}}
            stage_unixwrap_bundle(unixwrap_dir, result_dir, config)

            expected_files = (
                (os.path.join("EFI", "APPLE", "X64", "BOOT.EFI"), b"efi"),
                ("boot.cfg", b"boot config"),
                ("ram.img", b"guest image"),
            )
            for relative_path, expected_contents in expected_files:
                with open(os.path.join(result_dir, relative_path), "rb") as stream:
                    self.assertEqual(stream.read(), expected_contents)

            self.assertEqual(
                config["Misc"]["BlessOverride"],
                [r"\EFI\APPLE\X64\BOOT.EFI"],
            )

            stage_unixwrap_bundle(unixwrap_dir, result_dir, config)
            self.assertEqual(
                config["Misc"]["BlessOverride"].count(UNIXWRAP_BLESS_PATH),
                1,
            )
            self.assertEqual(config["Misc"]["Entries"][0]["Path"], r"\EFI\Other.efi")

    def test_missing_payload_fails_clearly(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            with self.assertRaises(FileNotFoundError):
                stage_unixwrap_bundle(temporary_dir, temporary_dir, {})

    def test_downloaded_package_efi_uses_local_guest_payload(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            unixwrap_dir = os.path.join(temporary_dir, "UnixWrap")
            result_dir = os.path.join(temporary_dir, "Results")
            os.makedirs(os.path.join(unixwrap_dir, "run"))
            for name, contents in (
                ("boot.cfg", b"local boot config"),
                ("ram.img", b"local guest image"),
            ):
                with open(os.path.join(unixwrap_dir, "run", name), "wb") as stream:
                    stream.write(contents)

            def download_package(_fetcher, _url, destination, sha256):
                self.assertEqual(sha256, "expected-hash")
                with zipfile.ZipFile(destination, "w") as package:
                    package.writestr(PACKAGE_EFI_PATH, b"downloaded efi")
                return True

            config = {}
            with mock.patch(
                "Scripts.unixwrap_bundle.resource_fetcher.ResourceFetcher.download_and_save_file",
                new=download_package,
            ):
                stage_unixwrap_bundle(
                    unixwrap_dir,
                    result_dir,
                    config,
                    package_url="https://example.invalid/unixwrap.zip",
                    package_sha256="expected-hash",
                )

            for relative_path, expected_contents in (
                (os.path.join("EFI", "APPLE", "X64", "BOOT.EFI"), b"downloaded efi"),
                ("boot.cfg", b"local boot config"),
                ("ram.img", b"local guest image"),
            ):
                with open(os.path.join(result_dir, relative_path), "rb") as stream:
                    self.assertEqual(stream.read(), expected_contents)

    def test_package_download_requires_sha256(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            unixwrap_dir = os.path.join(temporary_dir, "UnixWrap")
            os.makedirs(os.path.join(unixwrap_dir, "run"))
            for name in ("boot.cfg", "ram.img"):
                with open(os.path.join(unixwrap_dir, "run", name), "wb") as stream:
                    stream.write(b"local payload")
            with self.assertRaisesRegex(ValueError, "UNIXWRAP_PACKAGE_SHA256"):
                stage_unixwrap_bundle(
                    unixwrap_dir,
                    temporary_dir,
                    {},
                    package_url="https://example.invalid/unixwrap.zip",
                )

    def test_downloads_and_verifies_guest_payload_when_local_files_are_missing(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            unixwrap_dir = os.path.join(temporary_dir, "UnixWrap")
            result_dir = os.path.join(temporary_dir, "Results")
            os.makedirs(os.path.join(unixwrap_dir, "run"))
            with open(os.path.join(unixwrap_dir, "BOOTX64.EFI"), "wb") as stream:
                stream.write(b"local efi")
            downloads = {
                DEFAULT_BOOT_CFG_URL: (DEFAULT_BOOT_CFG_SHA256, b"downloaded boot config"),
                DEFAULT_RAM_IMG_URL: (DEFAULT_RAM_IMG_SHA256, b"downloaded guest image"),
            }

            def download(_fetcher, url, destination, sha256):
                expected_sha256, contents = downloads[url]
                self.assertEqual(sha256, expected_sha256)
                with open(destination, "wb") as stream:
                    stream.write(contents)
                return True

            with mock.patch(
                "Scripts.unixwrap_bundle.resource_fetcher.ResourceFetcher.download_and_save_file",
                new=download,
            ):
                stage_unixwrap_bundle(unixwrap_dir, result_dir, {})

            for name, expected_contents in (
                ("boot.cfg", b"downloaded boot config"),
                ("ram.img", b"downloaded guest image"),
            ):
                with open(os.path.join(result_dir, name), "rb") as stream:
                    self.assertEqual(stream.read(), expected_contents)

    def test_preserves_catalogued_ipsw_entries_for_staged_efi(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            unixwrap_dir = os.path.join(temporary_dir, "UnixWrap")
            result_dir = os.path.join(temporary_dir, "Results")
            os.makedirs(os.path.join(unixwrap_dir, "run"))
            os.makedirs(os.path.join(unixwrap_dir, "boot"))
            for name in ("boot.cfg", "ram.img"):
                with open(os.path.join(unixwrap_dir, "run", name), "wb") as stream:
                    stream.write(b"prepared guest")
            with open(os.path.join(unixwrap_dir, "BOOTX64.EFI"), "wb") as stream:
                stream.write(b"efi")

            ipsw_entry = {
                "Arguments": '--ipsw "/Volumes/Install/macOS.ipsw"',
                "Enabled": True,
                "Name": "macOS Recovery (ipsw) - 26A428",
                "Path": (
                    "PciRoot(0x0)/Pci(0x14,0x0)/USB(0x1,0x0)/"
                    "HD(1,GPT,01234567-89AB-CDEF-0123-456789ABCDEF,0x800,0x64000)/"
                    r"\EFI\APPLE\X64\BOOT.EFI"
                ),
            }
            with open(os.path.join(unixwrap_dir, "boot", "config.plist"), "wb") as stream:
                plistlib.dump({"Misc": {"Entries": [ipsw_entry]}}, stream)

            config = {"Misc": {"Entries": []}}
            stage_unixwrap_bundle(unixwrap_dir, result_dir, config)

            self.assertEqual(config["Misc"]["Entries"], [ipsw_entry])
            self.assertNotIn("BlessOverride", config["Misc"])

    def test_rejects_ipsw_entry_for_wrong_efi_path(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            unixwrap_dir = os.path.join(temporary_dir, "UnixWrap")
            os.makedirs(os.path.join(unixwrap_dir, "boot"))
            with open(os.path.join(unixwrap_dir, "boot", "config.plist"), "wb") as stream:
                plistlib.dump(
                    {"Misc": {"Entries": [{
                        "Arguments": '--ipsw "/Volumes/Install/macOS.ipsw"',
                        "Path": r"PciRoot(0x0)/HD(1,GPT,UUID)/EFI/BOOT/BOOTX64.EFI",
                    }]}},
                    stream,
                )
            with self.assertRaisesRegex(ValueError, "full HD"):
                _read_ipsw_entries(unixwrap_dir)


if __name__ == "__main__":
    unittest.main()
