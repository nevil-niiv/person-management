from functools import wraps

from django.db.models import QuerySet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PersonPagination(PageNumberPagination):
    """
    Custom pagination class for the Person entity.

    - Defines how the results for a list of people are paginated.
    - Sets the default page size to 5.
    - Allows clients to customize the page size via
      a query parameter (`page_size`).
    - Limits the maximum page size to 100 to prevent large data fetches.

    Attributes:
        page_size (int): Default number of items per page
            (10 people per page).
        page_size_query_param (str): The query parameter used
            to adjust page size (`page_size`).
        max_page_size (int): The maximum number of items
            allowed per page (100 people).
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


def paginate(exclude_fields=None):
    """
    Decorator to apply pagination to a view method.

    Args:
        exclude_fields (list, optional): Fields we want to exclude
            from response
        for serializing the paginated response.

    Usage:
        @paginate(exclude_fields=[field])
        def some_view(self, request):
            return queryset
    """

    def decorator(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            queryset = func(self, *args, **kwargs)
            assert isinstance(
                queryset, (list, QuerySet)
            ), "apply_pagination expects a List or a QuerySet"

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(
                    page, many=True, exclude_fields=exclude_fields
                )
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(
                queryset, many=True, exclude_fields=exclude_fields
            )
            return Response(serializer.data)

        return inner

    return decorator
