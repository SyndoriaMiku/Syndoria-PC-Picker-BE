from django.contrib import admin
from django import forms
from .models import *

class GraphicsCardForm(forms.ModelForm):
    class Meta:
        model = GraphicsCard
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data.get('gpu_brand') == 'Nvidia' or (self.instance and self.instance.gpu_brand == 'Nvidia'):
            self.fields['core'].label = "CUDA Core"
        elif self.data.get('gpu_brand') == 'AMD' or (self.instance and self.instance.gpu_brand == 'AMD'):
            self.fields['core'].label = "Stream Processors"
        else:
            self.fields['core'].label = "Số nhân" # Default label

        # Nếu có instance (đang chỉnh sửa), cập nhật label dựa trên gpu_brand
        if self.instance:
            if self.instance.gpu_brand == 'Nvidia':
                self.fields['core'].label = "CUDA Core"
            elif self.instance.gpu_brand == 'AMD':
                self.fields['core'].label = "Stream Processors"
                
# Register your models here.


admin.site.register(Socket)
admin.site.register(FormFactor)
admin.site.register(MemoryType)
admin.site.register(CPU)
admin.site.register(CPUCooler)
admin.site.register(Motherboard)
admin.site.register(Memory)
admin.site.register(GraphicsCard, form=GraphicsCardForm)
admin.site.register(Storage)
admin.site.register(PowerSupply)

