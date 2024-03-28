import os 
import config

try:
    import requests
except ImportError:
    print("Please install the requests package by running")
    print("pip install requests")
    print("This program cannot run without the requests package")
    print("Exiting...")
    os._exit(1)

class Movie():
    def __init__(self, title, year, actors, director, plot, rating, runtime):
        self.title = title
        self.year = year
        self.actors = actors
        self.director = director
        self.plot = plot
        self.rating = rating
        self.runtime = runtime
        
    def display_movie_data(self):
        print()
        print(f'''Title: {self.title}\nYear: {self.year}
IMDB Rating: {self.rating}\nRuntime: {self.runtime}\n
Director: {self.director}\nActors: {self.actors}\n
Plot: {self.plot}''')
        print()

class API():
    def __init__(self):
        self.API_BASE_URL = f"http://www.omdbapi.com/?apikey={config.API_KEY}&"
        
movie1 = Movie("banana", "2023", "Ricky Webster", "Jack Trounce", "Edward had a little lamb", "7/10", "75 minutes")

movie1.display_movie_data()



    
    
