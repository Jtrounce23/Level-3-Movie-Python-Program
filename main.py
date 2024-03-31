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
    def __init__(self, title, year, cast, plot, rating):
        self.title = title
        self.year = year
        self.cast = cast
        self.plot = plot
        self.rating = rating
        
    def display_movie_data(self):
        print("________________________________")
        print()
        print(f'''Title: {self.title}\nRelease Date: {self.year}
Vote Average: {self.rating}\n\nPlot: {self.plot}''')
        print()
        
        print("Top Cast:")
        print()
        i = 0
        while i < len(self.cast):
            print(self.cast[i])
            i += 1
        print()

class API(): 
    def __init__(self):
        self.API_SEARCH_BASE_URL = f"https://api.themoviedb.org/3/search/movie?api_key={config.API_KEY}"
        self.API_SEARCH_TITLE_URL_TAG = f"&query="
        
        self.API_DISCOVER_BASE_URL = f"https://api.themoviedb.org/3/discover/movie?api_key={config.API_KEY}"
        self.API_DISCOVER_YEAR_URL_TAG = f"&primary_release_year="
        
        self.API_TRENDING_URL = f"https://api.themoviedb.org/3/trending/all/day?api_key={config.API_KEY}"
        
        self.API_MOVIE_BASE_URL = f"https://api.themoviedb.org/3/movie/"
        self.API_MOVIE_CREDITS_URL_TAG = f"/credits?api_key={config.API_KEY}"
        
        self.watchlist = []
        
    def call_api(self, BASE, TAG, list_name):    
        movie_responce = requests.get(BASE + TAG)
        
        if movie_responce.status_code == 200:
            json_data = movie_responce.json()
            
            if len(json_data[f'{list_name}']) == 0:
                print('no results found')
                print()
                return
            
            else:
                return(json_data)
            
        else:
            print('failed')       

    def get_movie_data(self, BASE, TAG):
        json_data = self.call_api(BASE, TAG, 'results')
        max_results = 5
        
        print("________________________________")
        print()
        print("Results:".upper())
        
        while True:
            
            i = 0
            while i < len(json_data['results']) and i < max_results:
                print()
                print(i+1, json_data['results'][i]['title'])
                i += 1
            
            if max_results > len(json_data['results']):
                print()
                print("This is the max number of results")
                print()
            else:
                print()     
                print("showing", max_results, "results")
                print()
            
            which_movie = int(input("enter the corresponding number to select the film, or enter 0 to show more results: "))
            if which_movie == 0:
                max_results += 5
                continue
            
            results_movie = json_data['results'][which_movie - 1]
            film_id = results_movie['id']
            break
        
        json_data = self.call_api(self.API_MOVIE_BASE_URL + f"{film_id}", self.API_MOVIE_CREDITS_URL_TAG, 'cast')
        
        top_cast = []
        cast = (json_data['cast'])
        
        i = 0
        a = 0
        while i < len(cast) and a < 5:
            if cast[i]['known_for_department'] == 'Acting':
                top_cast.append(cast[i]['name'])
                a += 1
            i += 1
            
        movie = Movie(results_movie['title'], results_movie['release_date'], top_cast, results_movie['overview'], results_movie['vote_average'])
        movie.display_movie_data()      
        
        add_watchlist = int(input("Do you want to:\n1) Add this film to watchlist\n2) Return to the menu\n"))
        if add_watchlist == 1:    
            self.watchlist.append(results_movie['title'])
        elif add_watchlist == 2:
            menu()
        else:
            print("please enter the number corresponding the the question")
        
    def search_name(self):
        movie_name = str(input("Movie Name: "))
        self.get_movie_data(self.API_SEARCH_BASE_URL, self.API_SEARCH_TITLE_URL_TAG + movie_name)
        
    def search_year(self):
        movie_year = str(input("Movie Year: "))
        self.get_movie_data(self.API_DISCOVER_BASE_URL, self.API_DISCOVER_YEAR_URL_TAG + movie_year)
            
    def print_watchlist(self):
        print()
        print("Watchlist:")
        i = 0
        while i < len(self.watchlist):
            print(self.watchlist[i])
            i += 1
            
    def get_trending(self):
        print("________________________________")
        print()
        print("Top trending movies:".upper())
        print()
        json_data = self.call_api(self.API_TRENDING_URL, '', 'results')
        
        i = 0
        a = 0
        while i < len(json_data['results']) and a < 10:
            if json_data['results'][i]['media_type'] == 'movie':
                print(json_data['results'][i]['title'])
                a += 1
            i += 1
        
def get_int():
    ...
    
def menu():
    while True:
        api = API()
        
        api.get_trending()
        
        print("________________________________")
        print()
        print(f"Would you like to:\n1) Search for a film?\n2) view watchlist?\n3) Exit?")
        menu_1 = int(input())
        
        if menu_1 == 1: 
            print("________________________________")
            print()
            print(f"Would you like to:\n1) Search by name?\n2) Search by year?")
            menu_2 = int(input())
            
            if menu_2 == 1:
                print()
                api.search_name()
            elif menu_2 == 2:
                print()
                api.search_year()
            else:
                print()
                print("please enter the corresponding number to the question")
                print()
                
        elif menu_1 == 2:
            api.print_watchlist()
            
        elif menu_1 == 3:
            exit()
            
        else:
            print("please enter the corresponding number to the question")
        
    
if __name__ == "__main__":
    menu()

        



    
    