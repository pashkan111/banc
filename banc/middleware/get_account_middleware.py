# from django.http import HttpResponse

# from rest_framework import status
# from rest_framework.authentication import TokenAuthentication

# class ClientApplicationMiddleware:
#     """Сохранение актуальной информации о клиенте из заголовков запроса."""

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         user = request.user

#         if not isinstance(user, Courier):
#             return response

#             return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

#         return response
