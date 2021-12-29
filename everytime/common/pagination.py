from rest_framework.pagination import *
from rest_framework.response import Response

# Custom pagination
#  : url 앞에 host 생략하여 response
#
# https://docs.djangoproject.com/en/4.0/ref/request-response/
# https://stackoverflow.com/questions/62421753/how-to-change-the-host-in-next-key-in-a-paginated-url-in-django-rest-framework
# https://www.django-rest-framework.org/api-guide/pagination/
class CustomPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_next_link(self):
        if self.offset + self.limit >= self.count:
            return None

        url = self.request.get_full_path()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = self.offset + self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def get_previous_link(self):
        if self.offset <= 0:
            return None

        url = self.request.get_full_path()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        if self.offset - self.limit <= 0:
            return remove_query_param(url, self.offset_query_param)

        offset = self.offset - self.limit
        return replace_query_param(url, self.offset_query_param, offset)