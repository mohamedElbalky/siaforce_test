from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from pymongo import MongoClient

from .serializers import UserCreateSerializer, UserSerializerWithToken


# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["credentials_db"]
collection = db["credentials"]



@api_view(["POST"])
def register_user_view(request):
    """
    Create a new user.
    """
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.save()
        res_serializer = UserSerializerWithToken(data, many=False)
        return Response(res_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------

class CustomPagination(PageNumberPagination):
    page_size = 50  # Default page size
    page_size_query_param = 'page_size'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_credentials(request):
    paginator = CustomPagination()
    query = request.GET.get('q', '')  # Change to `q`

    if query:
        # Fetch credentials matching the search query
        credentials = list(collection.find(
            {"$or": [
                {"application": {"$regex": query, "$options": "i"}},
                {"soft": {"$regex": query, "$options": "i"}},
                {"host": {"$regex": query, "$options": "i"}},
                {"username": {"$regex": query, "$options": "i"}},
                {"url": {"$regex": query, "$options": "i"}},
            ]}
        ))
    else:
        credentials = list(collection.find({}))

    # Convert ObjectId to string
    for cred in credentials:
        cred['_id'] = str(cred['_id'])

    # Paginate the credentials
    page = paginator.paginate_queryset(credentials, request)
    if page is not None:
        return paginator.get_paginated_response(page)

    return Response(credentials)

