# _*_coding : uft-8 _*_
# @Time : 2023/5/23 9:44
# @Author : 
# @File : page
# @Project : meilan
from rest_framework.pagination import PageNumberPagination


class PageNum(PageNumberPagination):
    page_size = 5
    page_size_query_param = 's'
    max_page_size = 50
    page_query_param = 'p'
