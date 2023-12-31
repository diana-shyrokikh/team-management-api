from rest_framework.pagination import PageNumberPagination


class TenSizePagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page_size"
    max_page_size = 100000


class TwentySizePagination(PageNumberPagination):
    page_size = 20
    page_query_param = "page_size"
    max_page_size = 100000
