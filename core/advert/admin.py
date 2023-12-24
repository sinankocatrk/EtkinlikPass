from django.contrib import admin
from .models import Advert , DeleteReason, ComplaintReason

admin.site.register(Advert)


@admin.register(DeleteReason)
class DeleteReasonAdmin(admin.ModelAdmin):
    list_display = ['advert', 'reason', 'user']


@admin.register(ComplaintReason)
class ComplaintReasonAdmin(admin.ModelAdmin):
    list_display = ['advert', 'reason', 'user']
