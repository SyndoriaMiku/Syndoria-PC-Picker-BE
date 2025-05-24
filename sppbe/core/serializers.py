from rest_framework import serializers
from .models import *

class SocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socket
        fields = '__all__'

class FormFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormFactor
        fields = '__all__'
        
class MemoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryType
        fields = '__all__'
        
class CPUSerializer(serializers.ModelSerializer):
    socket = SocketSerializer(read_only=True)
    
    class Meta:
        model = CPU
        fields = '__all__'

class CPUCoolerSerializer(serializers.ModelSerializer):
    socket = SocketSerializer(many=True, read_only=True)
    
    class Meta:
        model = CPUCooler
        fields = '__all__'
        
class MotherboardSerializer(serializers.ModelSerializer):
    socket = SocketSerializer(read_only=True)
    form_factor = FormFactorSerializer(read_only=True)
    memory_type = MemoryTypeSerializer(read_only=True)
    
    class Meta:
        model = Motherboard
        fields = '__all__'
        
class MemorySerializer(serializers.ModelSerializer):
    memory_type = MemoryTypeSerializer(read_only=True)
    
    class Meta:
        model = Memory
        fields = '__all__'
        
class GraphicsCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphicsCard
        fields = '__all__'
        
class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'
        
class PowerSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerSupply
        fields = '__all__'
        
        
        

                
    