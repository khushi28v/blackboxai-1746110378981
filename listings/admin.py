from django.contrib import admin
from django.urls import path
from django.db.models import Count, Avg
from django.template.response import TemplateResponse
from .models import Property, ChatMessage, Notification

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'bedrooms', 'bathrooms', 'area', 'latitude', 'longitude')
    search_fields = ('title', 'location')
    list_filter = ('location', 'bedrooms')
    ordering = ('-price',)
    fields = ('title', 'description', 'price', 'location', 'bedrooms', 'bathrooms', 'area', 'latitude', 'longitude', 'image')

@admin.register(Property)
class RegisteredPropertyAdmin(PropertyAdmin):
    pass

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')
    search_fields = ('user__username', 'message')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'is_read', 'timestamp')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'content')

class CustomAdminSite(admin.AdminSite):
    site_header = "Real Estate Admin"
    site_title = "Real Estate Admin Portal"
    index_title = "Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.dashboard_view), name='index'),
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        total_properties = Property.objects.count()
        avg_price = Property.objects.aggregate(Avg('price'))['price__avg'] or 0
        top_locations = Property.objects.values('location').annotate(count=Count('id')).order_by('-count')[:5]

        context = dict(
            self.each_context(request),
            total_properties=total_properties,
            avg_price=avg_price,
            top_locations=top_locations,
        )
        return TemplateResponse(request, "admin/dashboard.html", context)

custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.register(Property, RegisteredPropertyAdmin)
custom_admin_site.register(ChatMessage, ChatMessageAdmin)
custom_admin_site.register(Notification, NotificationAdmin)
