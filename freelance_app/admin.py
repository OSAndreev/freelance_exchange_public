from django.contrib import admin
from .models import UserData, Freelancer, Order, Offers, Category, Customer, DealHistory, BalanceOperations


class UserDataAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'mail',  'bank_account', 'role', 'about']


class FreelancerAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'degree']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'degree']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'explanation', 'cost', 'in_work', 'performer', 'degree_to_company',
                    'degree_to_performer',
                    'category', 'deadline', 'done', 'work_ready']


class OffersAdmin(admin.ModelAdmin):
    list_display = ['details', 'freelance_variety', 'take']


class DealHistoryAdmin(admin.ModelAdmin):
    list_display = ['from_who', 'to_who', 'order']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['description']


class BalanceOperationsAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'type_operation', 'summa']


admin.site.register(UserData, UserDataAdmin)
admin.site.register(Freelancer, FreelancerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Offers, OffersAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(DealHistory, DealHistoryAdmin)
admin.site.register(BalanceOperations)
# Register your models here.
