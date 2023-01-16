import requests

BASE = "http://127.0.0.1:5000/"


# data = [
#      {"name": "Django Unchained", "imdb_rating": 8.4, "genre" : "Drama, Western", "actors" : "Jamie Foxx, Christoph Waltz, Leonardo DiCaprio", "director" : "Quentin Tarantino"},
#      {"name": "The Lord of the Rings: The Return of the King", "imdb_rating": 9, "genre" : "Action, Adventure, Drama", "actors" : "Elijah Wood, Viggo Mortensen, Orlando Bloom", "director" : "Peter Jackson"}, 
#      {"name": "Fight Club", "imdb_rating": 8.8, "genre" : "Drama", "actors" : "Brad Pitt, Edward Norton", "director" : "David Fincher"}
#      ]
#  
# for i in range(len(data)):
#      response = requests.put(BASE +"movie/" + str(i), data[i])
#      print(response.json())
# 
# 
# response = requests.get(BASE +"movie/2")
# print(response.json())
# 
# response = requests.patch(BASE +"movie/1", {"name" : "Django", "genre" : "Action, Drama, Western"})
# print(response.json())

# response = requests.delete(BASE +"movie/0")
