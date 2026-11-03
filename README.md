<br/>
<div align="center">
  <h3 align="center">UnixWrap-Simplify</h3>

  <p align="center">
    A specialized tool that streamlines <a href="https://github.com/acidanthera/OpenCorePkg">OpenCore</a> EFI creation for UnixWrap by automating the essential setup process and providing standardized configurations. Designed to reduce manual effort while ensuring accuracy in your Hackintosh journey.
    <br />
    <br />
    <a href="#-features">Features</a> •
    <a href="#-how-to-use">How To Use</a> •
    <a href="#-contributing">Contributing</a> •
    <a href="#-license">License</a> •
    <a href="#-credits">Credits</a> •
    <a href="#-contact">Contact</a>
  </p>
</div>

> [!NOTE]
> UnixWrap-Simplify is a fork of [OpCore Simplify](https://github.com/lzhoang2801/OpCore-Simplify) by Hoang Hong Quan, adapted for UnixWrap. See [Credits](#-credits).

> [!WARNING]
> While UnixWrap-Simplify significantly reduces setup time, the Hackintosh journey still requires:
> - Understanding basic concepts from the [Dortania Guide](https://dortania.github.io/OpenCore-Install-Guide/)
> - Testing and troubleshooting during the installation process
> - Patience and persistence in resolving any issues that arise
>
> Our tool does not guarantee a successful installation in the first attempt, but it should help you get started.

## ✨ **Features**

1. **Comprehensive Hardware and macOS Support**  
   Fully supports modern hardware. Use `Compatibility Checker` to check supported/unsupported devices and macOS version supported.

   | **Component**  | **Supported**                                                                                       |
   |----------------|-----------------------------------------------------------------------------------------------------|
   | **CPU**        | Intel: Nehalem and Westmere (1st Gen) → Arrow Lake (15th Gen/Core Ultra Series 2) <br> AMD: Ryzen and Threadripper with [AMD Vanilla](https://github.com/AMD-OSX/AMD_Vanilla) |
   | **GPU**        | Intel iGPU: Iron Lake (1st Gen) → Ice Lake (10th Gen) <br> AMD APU: The entire Vega Raven ASIC family (Ryzen 1xxx → 5xxx, 7x30 series) <br> AMD dGPU: Navi 23, Navi 22, Navi 21 generations, and older series <br> NVIDIA: Kepler, Pascal, Maxwell, Fermi, Tesla generations |
   | **macOS**      | macOS High Sierra → macOS Golden Gate 27 |

2. **ACPI Patches and Kexts**  
   Automatically detects and adds ACPI patches and kexts based on hardware configuration.
   
   - Integrated with [SSDTTime](https://github.com/corpnewt/SSDTTime) for common patches (e.g., FakeEC, FixHPET, PLUG, RTCAWAC).
   - Includes custom patches:
      - Prevent kernel panics by directing the first CPU entry to an active CPU, disabling the UNC0 device, and creating a new RTC device for HEDT systems.
      - Disable unsupported or unused PCI devices, such as the GPU (using Optimus and Bumblebee methods or adding the disable-gpu property), Wi-Fi card, and NVMe storage controller.
      - Fix sleep state values in _PRW methods (GPRW, UPRW, HP special) to prevent immediate wake.
      - Add devices including ALS0, BUS0, MCHC, PMCR, PNLF, RMNE, IMEI, USBX, XOSI, along with a Surface Patch.
      - Enable ALSD and GPI0 devices.

3. **Automatic Updates**  
    Downloads the pinned UnixWrap-compatible OpenCorePkg release and checks for kext updates from [Dortania Builds](https://dortania.github.io/builds/) and GitHub releases before each EFI build.
            
4. **EFI Configuration**  
   Apply additional customization based on both widely used sources and personal experience.

   - Spoof GPU IDs for certain AMD GPUs not recognized in macOS.
   - Use CpuTopologyRebuild kext for Intel CPUs with P-cores and E-cores to enhance performance.
   - Disable System Integrity Protection (SIP).
   - Spoof CPU IDs for Intel Pentium, Celeron, Core, and Xeon processors.
   - Add custom CPU names for AMD CPUs, as well as Intel Pentium, Celeron, Xeon, and Core lines from the Rocket Lake (11th) generation and newer.
   - Add a patch to allow booting macOS with unsupported SMBIOS.
   - Add NVRAM entries to bypass checking the internal Bluetooth controller.
   - Properly configure ResizeAppleGpuBars based on specific Resizable BAR information.
   - Allow flexible iGPU configuration between headless and driving a display when a supported discrete GPU is present.
   - Force Intel GPUs into VESA mode with HDMI and DVI connectors to simplify installation process.
   - Provide configuration required for using OpenCore Legacy Patcher.
   - Add built-in device property for network devices (fix 'Could not communicate with the server' when using iServices) and storage controllers (fix internal drives shown as external).
   - Prioritize SMBIOS optimized for both power management and performance.
   - Re-enable CPU power management on legacy Intel CPUs in macOS Ventura 13 and newer.
   - Apply WiFi profiles for itlwm kext to enable auto WiFi connections at boot time.

   and more...

5. **Easy Customization**  
   In addition to the default settings applied, users can easily make further customizations if desired.

   - Custom ACPI patches, kexts, and SMBIOS adjustments (**not recommended**).
   - Force load kexts on unsupported macOS versions.
   - UnixWrap `#UnixWrap -> BootMethod` defaults to `Interpreter only`; change it in the generated `config.plist` to `JIT only` or `JIT + AOT` if desired. AOT is not implemented yet, so the combined mode currently runs JIT only.
   - macOS Golden Gate 27 automatically defaults to an Apple Silicon product profile. The profile is selected coarsely from the hardware report's CPU core count and laptop/desktop form factor; it is not a benchmark-equivalent SoC selection. Apple Silicon serials are not supported by the bundled `macserial`, so generated profiles use placeholder serial/MLB values and are not suitable for Apple online services. The currently verified M6 entry is the base M6 Mac mini; no M6 Pro/Max/Ultra product identifiers are added without a reliable published identifier.

## 🚀 **How To Use**

1. **Download UnixWrap-Simplify**:
   - Click **Code** → **Download ZIP** on the UnixWrap-Simplify repository page, or clone the repository with `git clone <your-UnixWrap-Simplify-repo-url>`.
   - Extract the downloaded ZIP file to your desired location.

   ![Download UnixWrap-Simplify](https://i.imgur.com/mcE7OSX.png)

2. **Running UnixWrap-Simplify**:
   - On **Windows**, run `UnixWrap-Simplify.bat`.
   - On **macOS**, run `UnixWrap-Simplify.command`.
   - On **Linux**, run `UnixWrap-Simplify.py` with existing Python interpreter.

   ![UnixWrap-Simplify Menu](https://i.imgur.com/vTr1V9D.png)

3. **Selecting hardware report**:
   - On Windows, there will be an option for `E. Export hardware report`. It's recommended to use this for the best results with your hardware configuration and BIOS at the time of building.
   - Alternatively, use [**Hardware Sniffer**](https://github.com/lzhoang2801/Hardware-Sniffer) to create a `Report.json` and ACPI dump for configuration manually.

   ![Selecting hardware report](https://i.imgur.com/MbRmIGJ.png)

   ![Loading ACPI Tables](https://i.imgur.com/SbL6N6v.png)

   ![Compatibility Checker](https://i.imgur.com/kuDGMmp.png)

4. **Selecting macOS Version and Customizing OpenCore EFI**:
   - By default, the latest compatible macOS version will be selected for your hardware.
   - UnixWrap-Simplify will automatically apply essential ACPI patches and kexts. 
   - You can manually review and customize these settings as needed.

   ![UnixWrap-Simplify Menu](https://i.imgur.com/TSk9ejy.png)

5. **Building OpenCore EFI**:
   - Once you've customized all options, select **Build OpenCore EFI** to generate your EFI.
   - The tool will automatically download the necessary bootloader and kexts, which may take a few minutes.
   - UnixWrap is staged at `EFI/APPLE/X64/BOOT.EFI`. Simplify downloads the updated UnixWrap v1.0.1 EFI with SHA-256 verification; that version retries its guest RAM allocation down to 2 GiB. Simplify uses the sibling UnixWrap checkout's `run/boot.cfg` and `run/ram.img` when both exist; if either is missing, it downloads both from the v1.0.0 release and verifies their hashes. The guest image is about 503 MiB. The EFI and guest files are staged with OpenCore so the complete `Results` folder can be copied to the USB root.

     The published guest image is a prebuilt macOS 27.0.1 guest for Mac14,3. It boots that prepared image; it does not browse for or extract arbitrary IPSWs from USB at firmware runtime. To use another IPSW, prepare it on the host and catalog it in the sibling UnixWrap checkout before building:

     ```sh
     cd /path/to/UnixWrap
     python3 boot/prepare_ipsw.py /Volumes/YourUSB/macOS.ipsw
     python3 boot/catalog_ipsw.py /Volumes/YourUSB/macOS.ipsw \
       --efi-path 'PciRoot(...)/.../HD(...,GPT,<esp-partition-guid>,...)/\EFI\APPLE\X64\BOOT.EFI'
     ```

     Use the full UEFI device path for the target USB's EFI partition. Simplify carries the catalog entries and extracted icons from `UnixWrap/boot/config.plist` into its generated EFI. Only the IPSW used to prepare the guest image can boot. The build downloads and SHA-256 verifies the precompiled EFI as well as `boot.cfg` and `ram.img` when needed. Set `UNIXWRAP_PACKAGE_URL` and `UNIXWRAP_PACKAGE_SHA256` to use another EFI release, or `UNIXWRAP_DIR` if the checkout is not in the default sibling location. Upload `dist/UnixWrap-X64-RELEASE.zip` as the v1.0.1 GitHub release asset for the default URL to resolve.

   ![WiFi Profile Extractor](https://i.imgur.com/71TkJkD.png)

   ![Choosing Codec Layout ID](https://i.imgur.com/Mcm20EQ.png)

   ![Building OpenCore EFI](https://i.imgur.com/deyj5de.png)

6. **USB Mapping**:
   - After building your EFI, follow the steps for mapping USB ports.

   ![Results](https://i.imgur.com/MIPigPF.png)

7. **Create USB and Install macOS**: 
   - Use [**UnPlugged**](https://github.com/corpnewt/UnPlugged) on Windows to create a USB macOS installer, or follow [this guide](https://dortania.github.io/OpenCore-Install-Guide/installer-guide/mac-install.html) for macOS.
   - For troubleshooting, refer to the [OpenCore Troubleshooting Guide](https://dortania.github.io/OpenCore-Install-Guide/troubleshooting/troubleshooting.html).

> [!NOTE]
> 1. After a successful installation, if OpenCore Legacy Patcher is required, simply apply root patches to activate the missing features (such as modern Broadcom Wi-Fi card and graphics acceleration).
> 
> 2. For AMD GPUs, after applying root patches from OpenCore Legacy Patcher, you need to remove the boot argument `-radvesa`/`-amd_no_dgpu_accel` for graphics acceleration to work.

## 🤝 **Contributing**

Contributions are **highly appreciated**! If you have ideas to improve this project, feel free to fork the repo and create a pull request, or open an issue with the "enhancement" tag.

Don't forget to ⭐ star the project! Thank you for your support! 🌟

## 📜 **License**

Distributed under the BSD 3-Clause License. See `LICENSE` for more information.

## 🙌 **Credits**

- [OpCore Simplify](https://github.com/lzhoang2801/OpCore-Simplify) by Hoang Hong Quan – the original project this fork is based on.
- [OpenCorePkg](https://github.com/acidanthera/OpenCorePkg) and [kexts](https://github.com/lzhoang2801/OpCore-Simplify/blob/main/Scripts/datasets/kext_data.py) – The backbone of this project.
- [SSDTTime](https://github.com/corpnewt/SSDTTime) – SSDT patching utilities.

## 📞 **Contact**

**UnixWrap-Simplify maintainer**
> 

**Original OpCore Simplify author — Hoang Hong Quan**
> Facebook [@macforce2601](https://facebook.com/macforce2601) &nbsp;&middot;&nbsp;
> Telegram [@lzhoang2601](https://t.me/lzhoang2601) &nbsp;&middot;&nbsp;
> Email: lzhoang2601@gmail.com
