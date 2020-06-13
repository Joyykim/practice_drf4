from django.contrib import admin

# Register your models here.
from cards.models import Card


def report(request, queryset):
    ids = [x for x in queryset.all()]
    count = queryset.update(is_reported=True)
    print('here:', ids, 'Count', count)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    search_fields = ('title', 'owner__username')
    date_hierarchy = 'created_at'
    list_display = ('id', 'content', '_owner', 'created_at', 'is_reported')
    list_filter = ('is_reported',)
    actions = (report,)

    def _owner(self, obj):
        return f'{obj.owner.username}'
