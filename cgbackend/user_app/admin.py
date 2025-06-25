from django.contrib import admin
from .models import User


class PremiumFilter(admin.SimpleListFilter):
    title = 'Premium'
    parameter_name = 'premium'
    def lookups(self, request, model_admin):
        return [('True', 'True'),('False', 'False')]
    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(is_premium=True)
        elif self.value() == 'False':
            return queryset.filter(is_premium=False)
        

            

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'last_online', 'token_count', 'premium', 'online']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = [PremiumFilter]
    ordering = ['first_name', 'last_name']
    def full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name
    def premium(self, obj):
        return obj.is_premium
    premium.boolean = premium
