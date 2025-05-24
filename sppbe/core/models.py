from django.db import models

CPU_Brand_CHOICES = [
    ('Intel', 'Intel'),
    ('AMD', 'AMD'),
]
GPU_Brand_CHOICES = [
    ('Nvidia', 'Nvidia'),
    ('AMD', 'AMD'),
]

# Create your models here.

class Socket(models.Model):
    """Socket on CPU and Mobo"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Socket"
        verbose_name_plural = "Socket"
        ordering = ['name']

class MemoryType(models.Model):
    """Memory Type"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Memory Type"
        verbose_name_plural = "Memory Type"
        ordering = ['name']

class FormFactor(models.Model):
    """Form Factor"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Form Factor"
        verbose_name_plural = "Form Factor"
        ordering = ['name']

class CPU (models.Model):
    """CPU Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50, choices=CPU_Brand_CHOICES)  # e.g., Intel, AMD
    microarchitecture = models.CharField(max_length=50, blank=True, null=True)
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE, related_name='cpu')
    cores = models.IntegerField()
    threads = models.IntegerField()
    base_clock = models.DecimalField(max_digits=10, decimal_places=2)
    boost_clock = models.DecimalField(max_digits=10, decimal_places=2)
    integrated_graphics = models.CharField(max_length=50, blank=True, null=True)  # e.g., Intel UHD Graphics
    cache_l2 = models.CharField(max_length=20, blank=True, null=True, verbose_name="Cache L2 (per core)")  # e.g., 256KB
    cache_l3 = models.CharField(max_length=20, blank=True, null=True, verbose_name="Cache L3")  # e.g., 8MB
    tdp = models.IntegerField(verbose_name="TDP")
    description = models.TextField(blank=True, null=True)
    estimated_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    def format_clock(self, field):
        value = getattr(self, field)
        return f"{value} GHz" if value else "N/A"
    
    class Meta:
        verbose_name = "CPU"
        verbose_name_plural = "CPU"
        ordering = ['-brand', '-estimated_price', 'name']
        
    def __str__(self):
        return f"{self.name}"

class CPUCooler(models.Model):
    """CPU Cooler Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    socket = models.ManyToManyField(Socket, related_name='cpu_cooler')
    cooler_type = models.CharField(max_length=50)  
    color = models.CharField(max_length=50, blank=True, null=True)  # e.g., Black, White
    fan_size = models.IntegerField()  # in mm
    radiator_size = models.CharField(max_length=50, blank=True, null=True)  # e.g., 120mm, 240mm
    estimated_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    
    description = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = "CPU Cooler"
        verbose_name_plural = "CPU Cooler"
        ordering = ['brand', 'name', '-estimated_price']
    
class Motherboard(models.Model):
    """Motherboard Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    chipset_brand = models.CharField(max_length=50)  # e.g., Intel, AMD
    chipset = models.CharField(max_length=50) # e.g., Z590, B550
    socket = models.ForeignKey(Socket, on_delete=models.CASCADE, related_name='motherboard')
    form_factor = models.ForeignKey(FormFactor, on_delete=models.CASCADE, related_name='motherboard')
    back_connector = models.BooleanField(default=False)  # True if it is back connector mainboard
    color = models.CharField(max_length=50, blank=True, null=True)  # e.g., Black, White
    memory_type = models.ForeignKey(MemoryType, on_delete=models.CASCADE, related_name='motherboard')
    memory_slots = models.IntegerField()
    memory_max = models.IntegerField()
    ethernet = models.CharField(max_length=50, blank=True, null=True)
    wifi = models.CharField(max_length=50, blank=True, null=True)
    bluetooth = models.CharField(max_length=50, blank=True, null=True)
    total_usb_a = models.IntegerField()
    total_usb_c = models.IntegerField()
    total_sata = models.IntegerField()
    total_m2 = models.IntegerField()
    estimated_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Motherboard"
        verbose_name_plural = "Motherboard"
        ordering = ['brand', 'chipset', '-estimated_price']

class Memory(models.Model):
    """Memory Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    memory_type = models.ForeignKey(MemoryType, on_delete=models.CASCADE, related_name='memory')
    total_capacity = models.IntegerField()  # in GB
    single_capacity = models.IntegerField()  # in GB
    bus = models.IntegerField()  # in MHz
    cas = models.CharField(max_length=20)  # CAS latency
    estimated_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Memory"
        verbose_name_plural = "RAM"
        ordering = ['brand', '-estimated_price']

class GraphicsCard(models.Model):
    """Graphics Card Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gpu_brand = models.CharField(max_length=50, choices=GPU_Brand_CHOICES)  # e.g., Nvidia, AMD
    gpu_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    core = models.IntegerField()  # number of cores
    core_clock = models.DecimalField(max_digits=10, decimal_places=2)  # in MHz
    vram = models.IntegerField()  # in GB
    vram_type = models.CharField(max_length=50)  # e.g., GDDR6
    vram_bus = models.IntegerField()  # in bits
    bandwidth = models.CharField(max_length=50)  # e.g., PCIe 4.0 x16
    port = models.TextField()
    length = models.IntegerField()  # in mm
    tdp = models.IntegerField()  # Thermal Design Power
    psu_recommended = models.IntegerField()  # Recommended PSU in watts
    power_connector = models.CharField(max_length=50)  # e.g., 8-pin, 6-pin

    description = models.TextField(blank=True, null=True)
    estimated_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    
    class Meta:
        verbose_name = "Graphics Card"
        verbose_name_plural = "Graphics Card"
        ordering = ['-gpu_brand', 'gpu_name', '-estimated_price']

class Storage(models.Model):
    """Storage Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    storage_type = models.CharField(max_length=50)  # e.g., SSD, HDD
    capacity = models.CharField(max_length=50)  # e.g., 1TB, 500GB
    interface = models.CharField(max_length=50)  # e.g., SATA, NVMe
    form_factor = models.CharField(max_length=50, blank=True, null=True)  # e.g., 2.5", M.2
    description = models.TextField(blank=True, null=True)
    estimated_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    
    class Meta:
        verbose_name = "Storage"
        verbose_name_plural = "Storage"
        ordering = ['-estimated_price', 'capacity', 'brand']

class PowerSupply(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    form_factor = models.CharField(max_length=50)  # e.g., ATX, SFX
    rating = models.CharField(max_length=50)  # e.g., 80 Plus Bronze, Gold
    wattage = models.IntegerField()  # in watts
    length = models.IntegerField()  # in mm
    modular = models.CharField(max_length=50)  # e.g., Fully Modular, Semi Modular, Non-Modular
    color = models.CharField(max_length=50, blank=True, null=True)  # e.g., Black, White
    pcie16 = models.IntegerField(default=0)  # Number of PCIe 16-pin connectors
    pcie12 = models.IntegerField(default=0)  # Number of PCIe 12-pin connectors
    pcie8 = models.IntegerField(default=0)  # Number of PCIe 8-pin connectors
    pcie6 = models.IntegerField(default=0)  # Number of PCIe 6-pin connectors
    pcie62 = models.IntegerField(default=0)  # Number of PCIe 6+2 pin connectors
    sata = models.IntegerField(default=0)  # Number of SATA connectors
    molex = models.IntegerField(default=0)  # Number of Molex connectors
    description = models.TextField(blank=True, null=True)
    estimated_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    
    class Meta:
        verbose_name = "PSU"
        verbose_name_plural = "PSU"
        ordering = ['-estimated_price', 'wattage', 'rating', 'brand']
        


    