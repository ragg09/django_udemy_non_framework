from rest_framework.response import Response
from rest_framework.decorators import api_view
from app_watchlist.models import Movie
from app_watchlist.api.serializers import MovieSerializer

#NOTE: every request requires a request method, 
# the decorato @api_view provides that for us

# @api_view(['GET']) # by defaul, api_view decorator is GET method you can actually leave it blank
# def movie_list(request):
#     movies = Movie.objects.all() # get complex data
#     # when we are getting multiple objects, we need to define the many=true since it needs map every queryset
#     serializer = MovieSerializer(movies, many=True) # serialized, map all data
#     return Response(serializer.data)


@api_view(['GET', 'POST']) # by defaul, api_view decorator is GET method you can actually leave it blank
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all() # get complex data
        # when we are getting multiple objects, we need to define the many=true since it needs map every queryset
        serializer = MovieSerializer(movies, many=True) # serialized, map all data
        return Response(serializer.data)
    
    if request.method == 'POST':
        # get data from clientside
        
        serializer = MovieSerializer(data=request.data)
        
        # validator
        if serializer.is_valid():
            # .save() method is called referenced to the create method in the serializer since the request method is POST
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# since these methods are using ID, to make the code cleaner, we can just merge it all in one function
@api_view(['GET', 'PUT', 'DELETE']) 
def movie_details(request, id):
    movie = Movie.objects.get(id=id)
    
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        # take note that we also pass the selected data in the serializer since our update need that instance of the old data
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            # .save() method is called referenced to the update method in the serializer since the request method is PUT
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
            
    if request.method == 'DELETE': 
        movie = Movie.objects.get(id=id)
        # this delete is a queryset method, it has nothing to do with serializer 
        movie.delete()