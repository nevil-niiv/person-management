from django.contrib import admin

from person.models import Person, Role


class RoleAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Role model.

    This class customizes the Django admin panel for managing roles,
    providing features like search, ordering, and read-only fields.

    Attributes:
        list_display (tuple): Specifies the fields to
            display in the admin list view.
        search_fields (tuple): Enables search functionality
            for the specified fields.
        readonly_fields (tuple): Fields that cannot be
            edited directly in the admin panel.
        ordering (tuple): Default ordering for displayed records.
    """

    list_display = ("name", "description")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)


class PersonAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Person model.

    This class customizes the Django admin panel for managing people,
    providing search, filtering, read-only fields, and default ordering.

    Attributes:
        list_display (tuple): Specifies the fields to
            display in the admin list view.
        list_filter (tuple): Enables filtering options in the admin panel.
        search_fields (tuple): Allows searching users by multiple attributes.
        readonly_fields (tuple): Fields that cannot be edited
            directly in the admin panel.
        ordering (tuple): Default ordering for displayed records.
    """

    list_display = ("username", "email", "first_name", "last_name")
    list_filter = ("role", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("id",)


admin.site.register(Role, RoleAdmin)
admin.site.register(Person, PersonAdmin)
