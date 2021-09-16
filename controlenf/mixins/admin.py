from django.contrib import admin


@admin.action(description="Restaurar modelos deletados")
def restore_model_action(self, request, queryset):
    for obj in queryset:
        obj.restore()


@admin.action(description="Deletar modelos logicamente")
def soft_model_delete_action(self, request, queryset):
    for obj in queryset:
        obj.delete(soft_delete=True)


class ControlModelAdmin(admin.ModelAdmin):
    actions = [
        restore_model_action,
        soft_model_delete_action,
    ]

