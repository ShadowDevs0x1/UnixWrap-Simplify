from Scripts.datasets import os_data

class MacDevice:
    def __init__(self, name, cpu, cpu_generation, discrete_gpu, initial_support, last_supported_version = None,
                 architecture="Intel", product_name=None, form_factor=None, category=None):
        self.name = name
        self.cpu = cpu
        self.cpu_generation = cpu_generation
        self.discrete_gpu = discrete_gpu
        self.initial_support = initial_support
        self.last_supported_version = last_supported_version or os_data.get_latest_darwin_version()
        self.architecture = architecture
        self.product_name = product_name or name
        self.form_factor = form_factor or ("laptop" if name.startswith("MacBook") else "desktop")
        self.category = category


def apple_silicon_mac(name, product_name, chip, initial_support, form_factor, category):
    return MacDevice(
        name, chip, "Apple Silicon", None, initial_support,
        architecture="Apple Silicon", product_name=product_name,
        form_factor=form_factor, category=category
    )

mac_devices = [
    # iMac Models
    MacDevice("iMac11,1", "i7-860", "Lynnfield", "ATI Radeon HD 4850", "10.2.0", "17.99.99"),
    MacDevice("iMac11,2", "i5-680", "Clarkdale", "ATI Radeon HD 4670", "10.3.0", "17.99.99"),
    MacDevice("iMac11,3", "i7-870", "Clarkdale", "ATI Radeon HD 5670", "10.3.0", "17.99.99"),
    MacDevice("iMac12,1", "i5-2400S", "Sandy Bridge", "AMD Radeon HD 6750M", "10.6.0", "17.99.99"),
    MacDevice("iMac12,2", "i7-2600", "Sandy Bridge", "AMD Radeon HD 6770M", "10.6.0", "17.99.99"),
    MacDevice("iMac13,1", "i7-3770S", "Ivy Bridge", "NVIDIA GeForce GT 640M", "12.2.0", "19.99.99"),
    MacDevice("iMac13,2", "i5-3470S", "Ivy Bridge", "NVIDIA GeForce GTX 660M", "12.2.0", "19.99.99"),
    MacDevice("iMac13,3", "i5-3470S", "Ivy Bridge", None, "12.2.0", "19.99.99"),
    MacDevice("iMac14,1", "i5-4570R", "Haswell", None, "12.4.0", "19.99.99"),
    MacDevice("iMac14,2", "i7-4771", "Haswell", "NVIDIA GeForce GT 750M", "12.4.0", "19.99.99"),
    MacDevice("iMac14,3", "i5-4570S", "Haswell", "NVIDIA GeForce GT 755M", "12.4.0", "19.99.99"),
    MacDevice("iMac14,4", "i5-4260U", "Haswell", None, "13.2.0", "20.99.99"),
    MacDevice("iMac15,1", "i7-4790K", "Haswell", "AMD Radeon R9 M290X", "14.0.0", "20.99.99"),
    MacDevice("iMac16,1", "i5-5250U", "Broadwell", None, "15.0.0", "21.99.99"),
    MacDevice("iMac16,2", "i5-5675R", "Broadwell", None, "15.0.0", "21.99.99"),
    MacDevice("iMac17,1", "i5-6500", "Skylake", "AMD Radeon R9 M380", "15.0.0", "21.99.99"),
    MacDevice("iMac18,1", "i5-7360U", "Kaby Lake", None, "16.5.0", "22.99.99"),
    MacDevice("iMac18,2", "i5-7400", "Kaby Lake", "AMD Radeon Pro 555", "16.5.0", "22.99.99"),
    MacDevice("iMac18,3", "i5-7600K", "Kaby Lake", "AMD Radeon Pro 570", "16.5.0", "22.99.99"),
    MacDevice("iMac19,1", "i9-9900K", "Coffee Lake", "AMD Radeon Pro 570X", "18.5.0", "24.99.99"),
    MacDevice("iMac19,2", "i5-8500", "Coffee Lake", "AMD Radeon Pro 555X", "18.5.0", "24.99.99"),
    MacDevice("iMac20,1", "i5-10500", "Comet Lake", "AMD Radeon Pro 5300", "19.6.0"),
    MacDevice("iMac20,2", "i9-10910", "Comet Lake", "AMD Radeon Pro 5300", "19.6.0"),
    # MacBook Models
    MacDevice("MacBook8,1", "M-5Y51", "Broadwell", None, "14.1.0", "20.99.99"),
    MacDevice("MacBook9,1", "m3-6Y30", "Skylake", None, "15.4.0", "21.99.99"),
    MacDevice("MacBook10,1", "m3-7Y32", "Kaby Lake", None, "16.6.0", "22.99.99"),
    # MacBookAir Models
    MacDevice("MacBookAir4,1", "i5-2467M", "Sandy Bridge", None, "11.0.0", "17.99.99"),
    MacDevice("MacBookAir4,2", "i5-2557M", "Sandy Bridge", None, "11.0.0", "17.99.99"),
    MacDevice("MacBookAir5,1", "i5-3317U", "Ivy Bridge", None, "11.4.0", "19.99.99"),
    MacDevice("MacBookAir5,2", "i5-3317U", "Ivy Bridge", None, "12.2.0", "19.99.99"),
    MacDevice("MacBookAir6,1", "i5-4250U", "Haswell", None, "12.4.0", "20.99.99"),
    MacDevice("MacBookAir6,2", "i5-4250U", "Haswell", None, "12.4.0", "20.99.99"),
    MacDevice("MacBookAir7,1", "i5-5250U", "Broadwell", None, "14.1.0", "21.99.99"),
    MacDevice("MacBookAir7,2", "i5-5250U", "Broadwell", None, "14.1.0", "21.99.99"),
    MacDevice("MacBookAir8,1", "i5-8210Y", "Amber Lake", None, "18.2.0", "24.99.99"),
    MacDevice("MacBookAir8,2", "i5-8210Y", "Amber Lake", None, "18.6.0", "24.99.99"),
    MacDevice("MacBookAir9,1", "i3-1000NG4", "Ice Lake", None, "19.4.0", "24.99.99"),
    # MacBookPro Models
    MacDevice("MacBookPro6,1", "i7-640M", "Arrandale", "NVIDIA GeForce GT 330M", "10.3.0", "17.99.99"),
    MacDevice("MacBookPro6,2", "i7-640M", "Arrandale", "NVIDIA GeForce GT 330M", "10.3.0", "17.99.99"),
    MacDevice("MacBookPro8,1", "i5-2415M", "Sandy Bridge", None, "10.6.0", "17.99.99"),
    MacDevice("MacBookPro8,2", "i7-2675QM", "Sandy Bridge", "AMD Radeon HD 6490M", "10.6.0", "17.99.99"),
    MacDevice("MacBookPro8,3", "i7-2820QM", "Sandy Bridge", "AMD Radeon HD 6750M", "10.6.0", "17.99.99"),
    MacDevice("MacBookPro9,1", "i7-3615QM", "Ivy Bridge", "NVIDIA GeForce GT 650M", "11.3.0", "19.99.99"),
    MacDevice("MacBookPro9,2", "i5-3210M", "Ivy Bridge", None, "11.3.0", "19.99.99"),
    MacDevice("MacBookPro10,1", "i7-3615QM", "Ivy Bridge", "NVIDIA GeForce GT 650M", "11.4.0", "19.99.99"),
    MacDevice("MacBookPro10,2", "i5-3210M", "Ivy Bridge", None, "12.2.0", "19.99.99"),
    MacDevice("MacBookPro11,1", "i5-4258U", "Haswell", None, "13.0.0", "20.99.99"),
    MacDevice("MacBookPro11,2", "i7-4770HQ", "Haswell", None, "13.0.0", "20.99.99"),
    MacDevice("MacBookPro11,3", "i7-4850HQ", "Haswell", "NVIDIA GeForce GT 750M", "13.0.0", "20.99.99"),
    MacDevice("MacBookPro11,4", "i7-4770HQ", "Haswell", None, "14.3.0", "21.99.99"),
    MacDevice("MacBookPro11,5", "i7-4870HQ", "Haswell", "AMD Radeon R9 M370X", "14.3.0", "21.99.99"),
    MacDevice("MacBookPro12,1", "i5-5257U", "Broadwell", None, "14.1.0", "21.99.99"),
    MacDevice("MacBookPro13,1", "i5-6360U", "Skylake", None, "16.0.0", "21.99.99"),
    MacDevice("MacBookPro13,2", "i7-6567U", "Skylake", None, "16.1.0", "21.99.99"),
    MacDevice("MacBookPro13,3", "i7-6700HQ", "Skylake", "AMD Radeon Pro 450", "16.1.0", "21.99.99"),
    MacDevice("MacBookPro14,1", "i5-7360U", "Kaby Lake", None, "16.6.0", "22.99.99"),
    MacDevice("MacBookPro14,2", "i5-7267U", "Kaby Lake", None, "16.6.0", "22.99.99"),
    MacDevice("MacBookPro14,3", "i7-7700HQ", "Kaby Lake", "AMD Radeon Pro 555", "16.6.0", "22.99.99"),
    MacDevice("MacBookPro15,1", "i7-8750H", "Coffee Lake", "AMD Radeon Pro 555X", "17.99.99", "24.99.99"),
    MacDevice("MacBookPro15,2", "i7-8559U", "Coffee Lake", None, "17.99.99", "24.99.99"),
    MacDevice("MacBookPro15,3", "i7-8850H", "Coffee Lake", "AMD Radeon Pro Vega 16", "18.2.0", "24.99.99"),
    MacDevice("MacBookPro15,4", "i5-8257U", "Coffee Lake", None, "18.6.0", "24.99.99"),
    MacDevice("MacBookPro16,1", "i7-9750H", "Coffee Lake", "AMD Radeon Pro 5300", "19.0.0"),
    MacDevice("MacBookPro16,2", "i5-1038NG7", "Ice Lake", None, "19.4.0"),
    MacDevice("MacBookPro16,3", "i5-8257U", "Coffee Lake", None, "19.4.0", "24.99.99"),
    MacDevice("MacBookPro16,4", "i7-9750H", "Coffee Lake", "AMD Radeon Pro 5600M", "19.0.0"),
    # Macmini Models
    MacDevice("Macmini5,1", "i5-2415M", "Sandy Bridge", None, "11.0.0", "17.99.99"),
    MacDevice("Macmini5,2", "i5-2520M", "Sandy Bridge", None, "11.0.0", "17.99.99"),
    MacDevice("Macmini5,3", "i7-2635QM", "Sandy Bridge", None, "11.0.0", "17.99.99"),
    MacDevice("Macmini6,1", "i5-3210M", "Ivy Bridge", None, "10.8.1", "19.99.99"),
    MacDevice("Macmini6,2", "i7-3615QM", "Ivy Bridge", None, "10.8.1", "19.99.99"),
    MacDevice("Macmini7,1", "i5-4260U", "Haswell", None, "14.0.0", "21.99.99"),
    MacDevice("Macmini8,1", "i7-8700B", "Coffee Lake", None, "18.0.0", "24.99.99"),
    # iMacPro Models
    MacDevice("iMacPro1,1", "W-2140B", "Skylake-W", "AMD Radeon RX Vega 56", "17.3.0", "24.99.99"),
    # MacPro Models
    MacDevice("MacPro5,1", "X5675 x2", "Nehalem/Westmere", "ATI Radeon HD 5770", "10.4.0", "18.99.99"),
    MacDevice("MacPro6,1", "E5-1620 v2", "Ivy Bridge EP", "AMD FirePro D300", "13.0.0", "21.99.99"),
    MacDevice("MacPro7,1", "W-3245M", "Cascade Lake-W", "AMD Radeon Pro 580X", "19.0.0"),

    # Verified Apple Silicon product identifiers. M3 Ultra is Mac15,14 (not
    # Mac15,4, which is an iMac M3). M6 Pro/Max/Ultra identifiers are not
    # included until they are published by a reliable device database.
    # References: https://github.com/AsahiLinux/docs/blob/main/docs/hw/devices/device-list.md
    # and https://github.com/netdata/netdata/blob/master/src/daemon/status-file-dmi.c
    apple_silicon_mac("MacBookAir10,1", "MacBook Air (M1, 2020)", "M1", "20.1.0", "laptop", "MacBook Air"),
    apple_silicon_mac("MacBookPro17,1", "MacBook Pro 13-inch (M1, 2020)", "M1", "20.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Macmini9,1", "Mac mini (M1, 2020)", "M1", "20.1.0", "desktop", "Mac mini"),
    apple_silicon_mac("iMac21,1", "iMac 24-inch (M1, 4-port, 2021)", "M1", "20.4.0", "desktop", "iMac"),
    apple_silicon_mac("iMac21,2", "iMac 24-inch (M1, 2-port, 2021)", "M1", "20.4.0", "desktop", "iMac"),
    apple_silicon_mac("MacBookPro18,1", "MacBook Pro 16-inch (M1 Pro, 2021)", "M1 Pro", "20.6.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("MacBookPro18,2", "MacBook Pro 16-inch (M1 Max, 2021)", "M1 Max", "20.6.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("MacBookPro18,3", "MacBook Pro 14-inch (M1 Pro, 2021)", "M1 Pro", "20.6.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("MacBookPro18,4", "MacBook Pro 14-inch (M1 Max, 2021)", "M1 Max", "20.6.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac13,1", "Mac Studio (M1 Max, 2022)", "M1 Max", "21.4.0", "desktop", "Mac Studio"),
    apple_silicon_mac("Mac13,2", "Mac Studio (M1 Ultra, 2022)", "M1 Ultra", "21.4.0", "desktop", "Mac Studio"),

    apple_silicon_mac("Mac14,2", "MacBook Air 13-inch (M2, 2022)", "M2", "22.0.0", "laptop", "MacBook Air"),
    apple_silicon_mac("Mac14,15", "MacBook Air 15-inch (M2, 2023)", "M2", "22.4.0", "laptop", "MacBook Air"),
    apple_silicon_mac("Mac14,7", "MacBook Pro 13-inch (M2, 2022)", "M2", "22.0.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac14,3", "Mac mini (M2, 2023)", "M2", "22.3.0", "desktop", "Mac mini"),
    apple_silicon_mac("Mac14,12", "Mac mini (M2 Pro, 2023)", "M2 Pro", "22.3.0", "desktop", "Mac mini"),
    apple_silicon_mac("Mac14,9", "MacBook Pro 14-inch (M2 Pro, 2023)", "M2 Pro", "22.3.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac14,10", "MacBook Pro 16-inch (M2 Pro, 2023)", "M2 Pro", "22.3.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac14,5", "MacBook Pro 14-inch (M2 Max, 2023)", "M2 Max", "22.3.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac14,6", "MacBook Pro 16-inch (M2 Max, 2023)", "M2 Max", "22.3.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac14,13", "Mac Studio (M2 Max, 2023)", "M2 Max", "22.4.0", "desktop", "Mac Studio"),
    apple_silicon_mac("Mac14,14", "Mac Studio (M2 Ultra, 2023)", "M2 Ultra", "22.4.0", "desktop", "Mac Studio"),
    apple_silicon_mac("Mac14,8", "Mac Pro (M2 Ultra, 2023)", "M2 Ultra", "22.5.0", "desktop", "Mac Pro"),

    apple_silicon_mac("Mac15,12", "MacBook Air 13-inch (M3, 2024)", "M3", "23.4.0", "laptop", "MacBook Air"),
    apple_silicon_mac("Mac15,13", "MacBook Air 15-inch (M3, 2024)", "M3", "23.4.0", "laptop", "MacBook Air"),
    apple_silicon_mac("Mac15,3", "MacBook Pro 14-inch (M3, 2023)", "M3", "23.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac15,6", "MacBook Pro 14-inch (M3 Pro, 2023)", "M3 Pro", "23.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac15,7", "MacBook Pro 16-inch (M3 Pro, 2023)", "M3 Pro", "23.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac15,8", "MacBook Pro 14-inch (M3 Max, 2023)", "M3 Max", "23.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac15,9", "MacBook Pro 16-inch (M3 Max, 2023)", "M3 Max", "23.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac15,10", "MacBook Pro 14-inch (M3 Max, 2023)", "M3 Max", "23.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac15,11", "MacBook Pro 16-inch (M3 Max, 2023)", "M3 Max", "23.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac15,4", "iMac 24-inch (M3, 2-port, 2023)", "M3", "23.1.0", "desktop", "iMac"),
    apple_silicon_mac("Mac15,5", "iMac 24-inch (M3, 4-port, 2023)", "M3", "23.1.0", "desktop", "iMac"),
    apple_silicon_mac("Mac15,14", "Mac Studio (M3 Ultra, 2025)", "M3 Ultra", "24.4.0", "desktop", "Mac Studio"),

    apple_silicon_mac("Mac16,12", "MacBook Air 13-inch (M4, 2025)", "M4", "24.3.0", "laptop", "MacBook Air"),
    apple_silicon_mac("Mac16,13", "MacBook Air 15-inch (M4, 2025)", "M4", "24.3.0", "laptop", "MacBook Air"),
    apple_silicon_mac("Mac16,1", "MacBook Pro 14-inch (M4, 2024)", "M4", "24.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac16,8", "MacBook Pro 14-inch (M4 Pro, 2024)", "M4 Pro", "24.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac16,7", "MacBook Pro 16-inch (M4 Pro, 2024)", "M4 Pro", "24.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac16,6", "MacBook Pro 14-inch (M4 Max, 2024)", "M4 Max", "24.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac16,5", "MacBook Pro 16-inch (M4 Max, 2024)", "M4 Max", "24.1.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac16,2", "iMac 24-inch (M4, 2-port, 2024)", "M4", "24.1.0", "desktop", "iMac"),
    apple_silicon_mac("Mac16,3", "iMac 24-inch (M4, 4-port, 2024)", "M4", "24.1.0", "desktop", "iMac"),
    apple_silicon_mac("Mac16,10", "Mac mini (M4, 2024)", "M4", "24.1.0", "desktop", "Mac mini"),
    apple_silicon_mac("Mac16,11", "Mac mini (M4 Pro, 2024)", "M4 Pro", "24.1.0", "desktop", "Mac mini"),
    apple_silicon_mac("Mac16,9", "Mac Studio (M4 Max, 2025)", "M4 Max", "24.4.0", "desktop", "Mac Studio"),

    apple_silicon_mac("Mac17,3", "MacBook Air 13-inch (M5, 2026)", "M5", "25.0.0", "laptop", "MacBook Air"),
    apple_silicon_mac("Mac16,4", "MacBook Air 15-inch (M5, 2026)", "M5", "25.0.0", "laptop", "MacBook Air"),
    apple_silicon_mac("Mac17,2", "MacBook Pro 14-inch (M5, 2025)", "M5", "25.0.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac17,9", "MacBook Pro 14-inch (M5 Pro, 2026)", "M5 Pro", "26.0.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac17,8", "MacBook Pro 16-inch (M5 Pro, 2026)", "M5 Pro", "26.0.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac17,7", "MacBook Pro 14-inch (M5 Max, 2026)", "M5 Max", "26.0.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac17,6", "MacBook Pro 16-inch (M5 Max, 2026)", "M5 Max", "26.0.0", "laptop", "MacBook Pro"),
    apple_silicon_mac("Mac17,16", "Mac mini (M5 Pro, 2026)", "M5 Pro", "26.0.0", "desktop", "Mac mini"),
    apple_silicon_mac("Mac17,14", "Mac Studio (M5 Max, 2026)", "M5 Max", "26.0.0", "desktop", "Mac Studio"),
    apple_silicon_mac("Mac17,15", "Mac Studio (M5 Ultra, 2026)", "M5 Ultra", "26.0.0", "desktop", "Mac Studio"),

    apple_silicon_mac("Mac17,5", "MacBook Neo (A18 Pro, 2026)", "A18 Pro", "26.0.0", "laptop", "MacBook Neo"),
    apple_silicon_mac("Mac18,5", "Mac mini (M6, 2026)", "M6", "26.0.0", "desktop", "Mac mini")
]

def get_mac_device_by_name(name):
    return next((mac_device for mac_device in mac_devices if mac_device.name == name), None)