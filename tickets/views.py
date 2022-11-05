from django.shortcuts import render
from django.http.response import JsonResponse
from .models import *
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

# Create your views here.

#first without REST and no model query   FBV

def no_rest_no_model(request):
    guests = [
        {
            'id' : 1,
            'name' : 'Hazem',
            'phone_number' : '01852763518'
        },
        {
            'id' : 2,
            'name' : 'khaled',
            'phone_number' : '0259863128'
        }
    ]

    return JsonResponse(guests, safe=False)

#with model query without REST

def from_model(request):
    data = Guest.objects.all()
    response = {
        'guests' : list(data.values('name', 'phone_number'))
    }
    return JsonResponse(response)

# List = GET
# Create = POST
# pk query = GET
# Update = PUT
# Delete detroy = DELETE


#function based views
#GET POST
@api_view(['GET', 'POST'])
def FBV_List(request):
    #GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    #POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)


#GET PUT DELETE

@api_view(['GET', 'PUT', 'DELETE'])

def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist():
        return Response(status= status.HTTP_404_NOT_FOUND)
    #GET
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    #PUT
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    #DELETE
    if request.method == 'DELETE':
        guest.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)



#class based views CBV

#GET POST

class CBV_list(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)



# GET PUT DELETE
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#5 mixins list

class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

# mixins get put delete
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request)
    def put(self, requset, pk):
        return self.update(requset)
    def delete(self, request, pk):
        return self.destroy(request)



#Generics
# get post
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

# get put delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

#viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ['movie_name']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


#find movie in function based view
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        movie_name = request.data['movie_name'],
        hall_number = request.data['hall_number'] 
    )
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)




#create nwe reservation

@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        movie_name = request.data['movie_name'],
        hall_number = request.data['hall_number'] 
    )

    guest = Guest()
    guest.name = request.data['name']
    guest.phone_number = request.data['phone_number']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)



#post author editor

class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer