import os
import plistlib
import shutil
import tempfile
import zipfile

from Scripts import resource_fetcher


UNIXWRAP_BLESS_PATH = r"\EFI\APPLE\X64\BOOT.EFI"
PACKAGE_EFI_PATH = "BOOTX64.EFI"
DEFAULT_PACKAGE_URL = (
    "https://github.com/ShadowDevs0x1/UnixWrap/releases/download/"
    "v1.0.0/UnixWrap-X64-RELEASE.zip"
)
DEFAULT_PACKAGE_SHA256 = (
    "fd8875c1a05b1eeccf338b7ea438c6907448d1c80e46b6a2b921249a7b44915a"
)
DEFAULT_BOOT_CFG_URL = (
    "https://github.com/ShadowDevs0x1/UnixWrap/releases/download/"
    "v1.0.0/boot.cfg"
)
DEFAULT_BOOT_CFG_SHA256 = (
    "1e03fac33f69b0a652aa7527899e53cb429d741b4d7da50ddeac93e89b007be5"
)
DEFAULT_RAM_IMG_URL = (
    "https://github.com/ShadowDevs0x1/UnixWrap/releases/download/"
    "v1.0.0/ram.img"
)
DEFAULT_RAM_IMG_SHA256 = (
    "48e488290544ce8e68f6d93a561185bdcb171fa467d33e003cfe77ed135903a0"
)


def _download_package_efi(package_url, package_sha256, temporary_dir):
    if not package_sha256:
        raise ValueError("UNIXWRAP_PACKAGE_SHA256 is required when downloading UnixWrap")

    package_path = os.path.join(temporary_dir, "UnixWrap-X64-RELEASE.zip")
    fetcher = resource_fetcher.ResourceFetcher()
    if not fetcher.download_and_save_file(package_url, package_path, package_sha256):
        raise RuntimeError("Failed to download or verify the UnixWrap EFI package")

    with zipfile.ZipFile(package_path) as package:
        try:
            efi_info = package.getinfo(PACKAGE_EFI_PATH)
        except KeyError:
            raise ValueError(
                "UnixWrap EFI package must contain a root-level {}".format(PACKAGE_EFI_PATH)
            )
        if efi_info.file_size <= 0 or efi_info.file_size > 32 * 1024 * 1024:
            raise ValueError("UnixWrap EFI package contains an invalid EFI size")
        efi_path = os.path.join(temporary_dir, PACKAGE_EFI_PATH)
        with package.open(efi_info) as source, open(efi_path, "wb") as destination:
            shutil.copyfileobj(source, destination)
    return efi_path


def _copy_guest_payload(
    unixwrap_dir,
    result_dir,
    boot_cfg_url,
    boot_cfg_sha256,
    ram_img_url,
    ram_img_sha256,
    temporary_dir,
):
    local_paths = {
        "boot.cfg": os.path.join(unixwrap_dir, "run", "boot.cfg"),
        "ram.img": os.path.join(unixwrap_dir, "run", "ram.img"),
    }
    if all(os.path.isfile(path) for path in local_paths.values()):
        for name, source in local_paths.items():
            shutil.copy2(source, os.path.join(result_dir, name))
        return

    downloads = (
        ("boot.cfg", boot_cfg_url, boot_cfg_sha256),
        ("ram.img", ram_img_url, ram_img_sha256),
    )
    if any(not url or not sha256 for _, url, sha256 in downloads):
        missing = [path for path in local_paths.values() if not os.path.isfile(path)]
        raise FileNotFoundError(
            "UnixWrap guest payload is incomplete and download URLs/checksums are "
            "not configured; missing: {}".format(", ".join(missing))
        )

    fetcher = resource_fetcher.ResourceFetcher()
    for name, url, sha256 in downloads:
        destination = os.path.join(temporary_dir, name)
        if not fetcher.download_and_save_file(url, destination, sha256):
            raise RuntimeError(
                "Failed to download or verify UnixWrap guest payload {}".format(name)
            )
        shutil.copy2(destination, os.path.join(result_dir, name))


def _read_ipsw_entries(unixwrap_dir):
    config_path = os.path.join(unixwrap_dir, "boot", "config.plist")
    if not os.path.isfile(config_path):
        return []

    with open(config_path, "rb") as stream:
        unixwrap_config = plistlib.load(stream)
    if not isinstance(unixwrap_config, dict):
        raise ValueError("UnixWrap boot/config.plist must contain a dictionary")

    misc = unixwrap_config.get("Misc", {})
    if not isinstance(misc, dict):
        raise ValueError("UnixWrap Misc must be a dictionary")
    entries = misc.get("Entries", [])
    if not isinstance(entries, list):
        raise ValueError("UnixWrap Misc -> Entries must be an array")

    ipsw_entries = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        arguments = entry.get("Arguments", "")
        if not isinstance(arguments, str) or "--ipsw" not in arguments:
            continue
        path = entry.get("Path", "")
        if not isinstance(path, str) or not path.upper().endswith(
            UNIXWRAP_BLESS_PATH.upper()
        ) or "HD(" not in path:
            raise ValueError(
                "UnixWrap IPSW picker entries must use a full HD(...) device path "
                "ending in {}".format(UNIXWRAP_BLESS_PATH)
            )
        ipsw_entries.append(entry)
    return ipsw_entries


def stage_unixwrap_bundle(
    unixwrap_dir,
    result_dir,
    config,
    package_url=None,
    package_sha256=None,
    boot_cfg_url=DEFAULT_BOOT_CFG_URL,
    boot_cfg_sha256=DEFAULT_BOOT_CFG_SHA256,
    ram_img_url=DEFAULT_RAM_IMG_URL,
    ram_img_sha256=DEFAULT_RAM_IMG_SHA256,
):
    local_efi_path = os.path.join(unixwrap_dir, "BOOTX64.EFI")
    if not package_url and not os.path.isfile(local_efi_path):
        raise FileNotFoundError(
            "UnixWrap EFI is missing and no package URL was configured: {}".format(
                local_efi_path
            )
        )

    unixwrap_efi_dir = os.path.join(result_dir, "EFI", "APPLE", "X64")
    os.makedirs(unixwrap_efi_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary_dir:
        if package_url:
            efi_path = _download_package_efi(package_url, package_sha256, temporary_dir)
            shutil.copy2(efi_path, os.path.join(unixwrap_efi_dir, "BOOT.EFI"))
        else:
            shutil.copy2(local_efi_path, os.path.join(unixwrap_efi_dir, "BOOT.EFI"))
        _copy_guest_payload(
            unixwrap_dir,
            result_dir,
            boot_cfg_url,
            boot_cfg_sha256,
            ram_img_url,
            ram_img_sha256,
            temporary_dir,
        )

    misc = config.setdefault("Misc", {})
    if not isinstance(misc, dict):
        raise ValueError("OpenCore Misc must be a dictionary")
    ipsw_entries = _read_ipsw_entries(unixwrap_dir)
    entries = misc.setdefault("Entries", [])
    if not isinstance(entries, list):
        raise ValueError("OpenCore Misc -> Entries must be an array")
    for ipsw_entry in ipsw_entries:
        if not any(
            isinstance(existing, dict)
            and existing.get("Path") == ipsw_entry.get("Path")
            and existing.get("Arguments") == ipsw_entry.get("Arguments")
            for existing in entries
        ):
            entries.append(ipsw_entry)

    if ipsw_entries:
        resources_source = os.path.join(
            unixwrap_dir, "boot", "opencore-resources", "Resources", "Image", "UnixWrap"
        )
        if os.path.isdir(resources_source):
            resources_target = os.path.join(
                result_dir, "EFI", "OC", "Resources", "Image", "UnixWrap"
            )
            shutil.copytree(resources_source, resources_target, dirs_exist_ok=True)
    else:
        bless_override = misc.setdefault("BlessOverride", [])
        if not isinstance(bless_override, list):
            raise ValueError("OpenCore Misc -> BlessOverride must be an array")
        if UNIXWRAP_BLESS_PATH not in bless_override:
            bless_override.append(UNIXWRAP_BLESS_PATH)
