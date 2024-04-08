from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId, json_util
from myproject.settings import mongo
import traceback
from django.conf import settings
from rest_framework import generics
from myapp.models import Student
from myapp.serializers import StudentSerializer


class StudentGeneric(generics.ListAPIView, generics.CreateAPIView):  # Changed from ListAPIView to ListCreateAPIView
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentGeneric1(generics.UpdateAPIView, generics.DestroyAPIView):  # Changed from ListAPIView to ListCreateAPIView
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'





class BookList(APIView):
    def get(self, request):
        try:
            collection = mongo.get_collection('crud_django')
            books = list(collection.find({}))
            # Serialize the MongoDB document to JSON, and convert ObjectId to string
            for book in books:
                book['_id'] = str(book['_id'])
            return Response({"data": books}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Expection")
            return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            collection = mongo.get_collection('crud_django')
            result = collection.insert_one(request.data).inserted_id
            # Convert ObjectId to string before sending it in the response
            return Response({"_id": str(result)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            traceback.print_exc()
            return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookDetail(APIView):
    def get(self, request, pk):
        try:
            collection = mongo.get_collection('crud_django')
            book = collection.find_one({'_id': ObjectId(pk)})
            if book:
                # Convert ObjectId to string
                book['_id'] = str(book['_id'])
                return Response(book, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, pk):
        try:
            collection = mongo.get_collection('crud_django')
            update_result = collection.update_one({'_id': ObjectId(pk)}, {'$set': request.data})
            if update_result.matched_count == 0:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            # Convert ObjectId to string before sending it in the response
            return Response({"_id": str(pk), "updated": True}, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            collection = mongo.get_collection('crud_django')
            delete_result = collection.delete_one({'_id': ObjectId(pk)})
            if delete_result.deleted_count == 0:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            traceback.print_exc()
            return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def patch(self, request, pk):
        try:
            # Convert the string 'pk' to a MongoDB ObjectId
            object_id = ObjectId(pk)
            # Get the collection
            collection = mongo.get_collection('crud_django')
            # Perform the partial update using the '$set' operator with the data provided in the request body
            update_result = collection.update_one({'_id': object_id}, {'$set': request.data})
            
            # Check if the document to update was found and updated
            if update_result.matched_count == 0:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"_id": str(object_id), "updated": True}, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 