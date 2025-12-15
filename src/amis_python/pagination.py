from rest_framework.pagination import PageNumberPagination


class AmisPagination(PageNumberPagination):
    page_size_query_param = "perPage"