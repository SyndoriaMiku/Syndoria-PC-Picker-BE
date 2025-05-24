#Core URL
from django.urls import path, include
from . import views

urlpatterns = [
    path('cpu/', views.CPUListView.as_view(), name='cpu-list'),
    path('cpu/<int:pk>/', views.CPUDetailView.as_view(), name='cpu-detail'),
    path('cpu-cooler/', views.CPUCoolerListView.as_view(), name='cpu-cooler-list'),
    path('cpu-cooler/<int:pk>/', views.CPUCoolerDetailView.as_view(), name='cpu-cooler-detail'),
    path('motherboard/', views.MotherboardListView.as_view(), name='motherboard-list'),
    path('motherboard/<int:pk>/', views.MotherboardDetailView.as_view(), name='motherboard-detail'),
    path('memory/', views.MemoryListView.as_view(), name='memory-list'),
    path('memory/<int:pk>/', views.MemoryDetailView.as_view(), name='memory-detail'),
    path('gpu/', views.GraphicsListView.as_view(), name='gpu-list'),
    path('gpu/<int:pk>/', views.GraphicsDetailView.as_view(), name='gpu-detail'),
    path('storage/', views.StorageListView.as_view(), name='storage-list'),
    path('storage/<int:pk>/', views.StorageDetailView.as_view(), name='storage-detail'),
    path('power-supply/', views.PowerSupplyListView.as_view(), name='power-supply-list'),
    path('power-supply/<int:pk>/', views.PowerSupplyDetailView.as_view(), name='power-supply-detail'),
]