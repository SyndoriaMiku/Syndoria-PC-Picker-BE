from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class StandardResultsPagination(PageNumberPagination):
    page_size = 10 # Số lượng item trên mỗi trang
    page_size_query_param = 'page_size' # Cho phép client thay đổi số lượng item
    max_page_size = 100 # Giới hạn tối đa

class CPUListView(APIView):
    """
    View to list all CPUs.
    Can be filtered by brand, name, socket, microarchitecture, integrated_graphics.
    Can create a new CPU.
    Implements GET and POST methods, GET got pagination.
    """
    pagination_class = StandardResultsPagination
    
    def get(self, request, format=None):
        queryset = CPU.objects.all() #Get all CPUs
        
        # Filter by brand
        brand = request.query_params.get('brand', None)
        if brand is not None:
            queryset = queryset.filter(brand__icontains=brand)
        # Filter by name
        name = request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        # Filter by socket
        socket_name = request.query_params.get('socket', None)
        if socket_name is not None:
            queryset = queryset.filter(socket__name__icontains=socket_name)
        # Filter by microarchitecture
        microarchitecture = request.query_params.get('microarchitecture', None)
        if microarchitecture is not None:
            queryset = queryset.filter(microarchitecture__icontains=microarchitecture)
        # Filter by integrated graphics
        integrated_graphics = request.query_params.get('integrated_graphics', None)
        if integrated_graphics is not None:
            queryset = queryset.filter(integrated_graphics__icontains=integrated_graphics)
        
        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = CPUSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = CPUSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        """
        Create a new CPU.
        """
        serializer = CPUSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CPUDetailView(APIView):    
    def get_object(self, pk):
        """
        Helper method to get the CPU object by primary key.
        """
        try:
            return CPU.objects.get(pk=pk)
        except CPU.DoesNotExist:
            return None
        
    def get(self, request, pk, format=None):
        """
        Retrieve a CPU by its primary key.
        """
        cpu = self.get_object(pk)
        if cpu is None:
            return Response({"error": "CPU not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CPUSerializer(cpu)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        """
        Update a CPU by its primary key.
        """
        cpu = self.get_object(pk)
        if cpu is None:
            return Response({"error": "CPU not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CPUSerializer(cpu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """
        Delete a CPU by its primary key.
        """
        cpu = self.get_object(pk)
        if cpu is None:
            return Response({"error": "CPU not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cpu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CPUCoolerListView(APIView):
    """
    View to list all CPU coolers.
    Can be filtered by brand, name, and socket.
    Can create a new CPU cooler.
    Implements GET and POST methods, GET got pagination.
    """
    pagination_class = StandardResultsPagination

    def get(self, request, format=None):
        queryset = CPUCooler.objects.all()  # Get all CPU coolers

        # Filter by brand
        brand = request.query_params.get('brand', None)
        if brand is not None:
            queryset = queryset.filter(brand__icontains=brand)
        # Filter by name
        name = request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        # Filter by socket
        socket_name = request.query_params.get('socket', None)
        if socket_name is not None:
            queryset = queryset.filter(socket__name__icontains=socket_name)

        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = CPUCoolerSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CPUCoolerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new CPU cooler.
        """
        serializer = CPUCoolerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CPUCoolerDetailView(APIView):
    def get_object(self, pk):
        """
        Helper method to get the CPU cooler object by primary key.
        """
        try:
            return CPUCooler.objects.get(pk=pk)
        except CPUCooler.DoesNotExist:
            return None
        
    def get(self, request, pk, format=None):
        """
        Retrieve a CPU cooler by its primary key.
        """
        cpu_cooler = self.get_object(pk)
        if cpu_cooler is None:
            return Response({"error": "CPU Cooler not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CPUCoolerSerializer(cpu_cooler)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        """
        Update a CPU cooler by its primary key.
        """
        cpu_cooler = self.get_object(pk)
        if cpu_cooler is None:
            return Response({"error": "CPU Cooler not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CPUCoolerSerializer(cpu_cooler, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """
        Delete a CPU cooler by its primary key.
        """
        cpu_cooler = self.get_object(pk)
        if cpu_cooler is None:
            return Response({"error": "CPU Cooler not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cpu_cooler.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MotherboardListView(APIView):
    """
    View to list all motherboards.
    Can be filtered by brand, name, socket, form factor, memory type, memory slot and wifi/bluetooth available.
    Can create a new motherboard.
    Implements GET and POST methods, GET got pagination.
    """
    pagination_class = StandardResultsPagination

    def get(self, request, format=None):
        queryset = Motherboard.objects.all()  # Get all motherboards


        # Filter by chipset
        chipset_name = request.query_params.get('chipset', None)
        if chipset_name is not None:
            queryset = queryset.filter(chipset__name__icontains=chipset_name)
        # Filter by chipset brand
        chipset_brand = request.query_params.get('chipset_brand', None)
        if chipset_brand is not None:
            queryset = queryset.filter(chipset_brand__icontains=chipset_brand)
        # Filter by brand
        brand = request.query_params.get('brand', None)
        if brand is not None:
            queryset = queryset.filter(brand__icontains=brand)
        # Filter by name
        name = request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        # Filter by socket
        socket_name = request.query_params.get('socket', None)
        if socket_name is not None:
            queryset = queryset.filter(socket__name__icontains=socket_name)
        # Filter by form factor
        form_factor_name = request.query_params.get('form_factor', None)
        if form_factor_name is not None:
            queryset = queryset.filter(form_factor__name__icontains=form_factor_name)
        # Filter by memory type
        memory_type_name = request.query_params.get('memory_type', None)
        if memory_type_name is not None:
            queryset = queryset.filter(memory_type__name__icontains=memory_type_name)
        # Filter by memory slots
        memory_slots = request.query_params.get('memory_slots', None)
        if memory_slots is not None:
            queryset = queryset.filter(memory_slots__gte=memory_slots)
        # Filter by wifi availability
        wifi = request.query_params.get('wifi', None)
        if wifi is not None:
            if wifi.lower() == 'yes':
                queryset = queryset.filter(wifi__isnull=False)
            elif wifi.lower() == 'no':
                queryset = queryset.filter(wifi__isnull=True)

        # Filter by bluetooth availability
        bluetooth = request.query_params.get('bluetooth', None)
        if bluetooth is not None:
            if bluetooth.lower() == 'yes':
                queryset = queryset.filter(bluetooth__isnull=False)
            elif bluetooth.lower() == 'no':
                queryset = queryset.filter(bluetooth__isnull=True)
        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = MotherboardSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = MotherboardSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new motherboard.
        """
        serializer = MotherboardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
class MotherboardDetailView(APIView):
    def get_object(self, pk):
        """
        Helper method to get the motherboard object by primary key.
        """
        try:
            return Motherboard.objects.get(pk=pk)
        except Motherboard.DoesNotExist:
            return None
        
    def get(self, request, pk, format=None):
        """
        Retrieve a motherboard by its primary key.
        """
        motherboard = self.get_object(pk)
        if motherboard is None:
            return Response({"error": "Motherboard not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MotherboardSerializer(motherboard)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        """
        Update a motherboard by its primary key.
        """
        motherboard = self.get_object(pk)
        if motherboard is None:
            return Response({"error": "Motherboard not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MotherboardSerializer(motherboard, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """
        Delete a motherboard by its primary key.
        """
        motherboard = self.get_object(pk)
        if motherboard is None:
            return Response({"error": "Motherboard not found"}, status=status.HTTP_404_NOT_FOUND)
        
        motherboard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MemoryListView(APIView):
    """
    View to list all memory modules.
    Can be filtered by brand, name, and memory type.
    Can be filtered by minimum capacity.
    Implements GET and POST methods, GET got pagination.
    """
    pagination_class = StandardResultsPagination

    def get(self, request, format=None):
        queryset = Memory.objects.all()  # Get all memory modules

        # Filter by brand
        brand = request.query_params.get('brand', None)
        if brand is not None:
            queryset = queryset.filter(brand__icontains=brand)
        # Filter by name
        name = request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        # Filter by memory type
        memory_type_name = request.query_params.get('memory_type', None)
        if memory_type_name is not None:
            queryset = queryset.filter(memory_type__name__icontains=memory_type_name)
        # Filter by minimum capacity
        min_capacity = request.query_params.get('min_capacity', None)
        if min_capacity is not None:
            queryset = queryset.filter(total_capacity__gte=min_capacity)

        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = MemorySerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = MemorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new memory module.
        """
        serializer = MemorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class MemoryDetailView(APIView):
    def get_object(self, pk):
        """
        Helper method to get the memory object by primary key.
        """
        try:
            return Memory.objects.get(pk=pk)
        except Memory.DoesNotExist:
            return None
        
    def get(self, request, pk, format=None):
        """
        Retrieve a memory module by its primary key.
        """
        memory = self.get_object(pk)
        if memory is None:
            return Response({"error": "Memory module not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MemorySerializer(memory)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        """
        Update a memory module by its primary key.
        """
        memory = self.get_object(pk)
        if memory is None:
            return Response({"error": "Memory module not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MemorySerializer(memory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """
        Delete a memory module by its primary key.
        """
        memory = self.get_object(pk)
        if memory is None:
            return Response({"error": "Memory module not found"}, status=status.HTTP_404_NOT_FOUND)
        
        memory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GraphicsListView(APIView):
    """
    View to list all graphics cards.
    Can be filtered by GPU Brand, GPU, Graphics Card Brand, Color.
    Can be filtered by minimum VRAM.
    Can create a new graphics card.
    Implements GET and POST methods, GET got pagination.
    """
    pagination_class = StandardResultsPagination

    def get(self, request, format=None):
        queryset = GraphicsCard.objects.all()  # Get all graphics cards

        # Filter by GPU Brand
        gpu_brand = request.query_params.get('gpu_brand', None)
        if gpu_brand is not None:
            queryset = queryset.filter(gpu_brand__icontains=gpu_brand)
        # Filter by GPU
        gpu = request.query_params.get('gpu', None)
        if gpu is not None:
            queryset = queryset.filter(gpu_name__icontains=gpu)
        # Filter by Graphics Card Brand
        brand = request.query_params.get('brand', None)
        if brand is not None:
            queryset = queryset.filter(brand__icontains=brand)
        # Filter by Color
        color = request.query_params.get('color', None)
        if color is not None:
            queryset = queryset.filter(color__icontains=color)
        # Filter by minimum VRAM
        min_vram = request.query_params.get('min_vram', None)
        if min_vram is not None:
            queryset = queryset.filter(vram__gte=min_vram)

        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = GraphicsCardSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = GraphicsCardSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new graphics card.
        """
        serializer = GraphicsCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class GraphicsDetailView(APIView):
    def get_object(self, pk):
        """
        Helper method to get the graphics card object by primary key.
        """
        try:
            return GraphicsCard.objects.get(pk=pk)
        except GraphicsCard.DoesNotExist:
            return None
        
    def get(self, request, pk, format=None):
        """
        Retrieve a graphics card by its primary key.
        """
        graphics_card = self.get_object(pk)
        if graphics_card is None:
            return Response({"error": "Graphics card not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GraphicsCardSerializer(graphics_card)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        """
        Update a graphics card by its primary key.
        """
        graphics_card = self.get_object(pk)
        if graphics_card is None:
            return Response({"error": "Graphics card not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GraphicsCardSerializer(graphics_card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """
        Delete a graphics card by its primary key.
        """
        graphics_card = self.get_object(pk)
        if graphics_card is None:
            return Response({"error": "Graphics card not found"}, status=status.HTTP_404_NOT_FOUND)
        
        graphics_card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StorageListView(APIView):
    """
    View to list all storage devices.
    Can be filtered by brand, name, and storage type.
    Can create a new storage device.
    Implements GET and POST methods, GET got pagination.
    """
    pagination_class = StandardResultsPagination

    def get(self, request, format=None):
        queryset = Storage.objects.all()  # Get all storage devices

        # Filter by brand
        brand = request.query_params.get('brand', None)
        if brand is not None:
            queryset = queryset.filter(brand__icontains=brand)
        # Filter by name
        name = request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        # Filter by storage type
        storage_type_name = request.query_params.get('storage_type', None)
        if storage_type_name is not None:
            queryset = queryset.filter(storage_type__name__icontains=storage_type_name)
        # Filter by minimum capacity
        min_capacity = request.query_params.get('min_capacity', None)
    
        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = StorageSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = StorageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new storage device.
        """
        serializer = StorageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class StorageDetailView(APIView):
    def get_object(self, pk):
        """
        Helper method to get the storage object by primary key.
        """
        try:
            return Storage.objects.get(pk=pk)
        except Storage.DoesNotExist:
            return None
        
    def get(self, request, pk, format=None):
        """
        Retrieve a storage device by its primary key.
        """
        storage = self.get_object(pk)
        if storage is None:
            return Response({"error": "Storage device not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StorageSerializer(storage)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        """
        Update a storage device by its primary key.
        """
        storage = self.get_object(pk)
        if storage is None:
            return Response({"error": "Storage device not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StorageSerializer(storage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """
        Delete a storage device by its primary key.
        """
        storage = self.get_object(pk)
        if storage is None:
            return Response({"error": "Storage device not found"}, status=status.HTTP_404_NOT_FOUND)
        
        storage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PowerSupplyListView(APIView):
    """
    View to list all power supplies.
    Can be filtered by brand, name and rating.
    Can be filtered by minimum wattage.
    Can create a new power supply.
    Implements GET and POST methods, GET got pagination.
    """
    pagination_class = StandardResultsPagination

    def get(self, request, format=None):
        queryset = PowerSupply.objects.all()  # Get all power supplies

        # Filter by brand
        brand = request.query_params.get('brand', None)
        if brand is not None:
            queryset = queryset.filter(brand__icontains=brand)
        # Filter by name
        name = request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        # Filter by rating
        rating = request.query_params.get('rating', None)
        if rating is not None:
            queryset = queryset.filter(rating__icontains=rating)
        # Filter by minimum wattage
        min_wattage = request.query_params.get('min_wattage', None)
        if min_wattage is not None:
            queryset = queryset.filter(wattage__gte=min_wattage)

        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = PowerSupplySerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = PowerSupplySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new power supply.
        """
        serializer = PowerSupplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PowerSupplyDetailView(APIView):
    def get_object(self, pk):
        """
        Helper method to get the power supply object by primary key.
        """
        try:
            return PowerSupply.objects.get(pk=pk)
        except PowerSupply.DoesNotExist:
            return None
        
    def get(self, request, pk, format=None):
        """
        Retrieve a power supply by its primary key.
        """
        power_supply = self.get_object(pk)
        if power_supply is None:
            return Response({"error": "Power supply not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PowerSupplySerializer(power_supply)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        """
        Update a power supply by its primary key.
        """
        power_supply = self.get_object(pk)
        if power_supply is None:
            return Response({"error": "Power supply not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PowerSupplySerializer(power_supply, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """
        Delete a power supply by its primary key.
        """
        power_supply = self.get_object(pk)
        if power_supply is None:
            return Response({"error": "Power supply not found"}, status=status.HTTP_404_NOT_FOUND)
        
        power_supply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    