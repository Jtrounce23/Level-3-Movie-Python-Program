import os 
import config
import time

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

class API(): 
    def __init__(self):
        self.API_SEARCH_BASE_URL = f"https://api.themoviedb.org/3/search/movie?api_key={config.API_KEY}"
        self.API_SEARCH_TITLE_URL_TAG = f"&query="
        
        self.API_DISCOVER_BASE_URL = f"https://api.themoviedb.org/3/discover/movie?api_key={config.API_KEY}"
        self.API_DISCOVER_YEAR_URL_TAG = f"&primary_release_year="
        
        self.API_TRENDING_URL = f"https://api.themoviedb.org/3/trending/all/day?api_key={config.API_KEY}"
        
        self.API_MOVIE_BASE_URL = f"https://api.themoviedb.org/3/movie/"
        self.API_MOVIE_CREDITS_URL_TAG = f"/credits?api_key={config.API_KEY}"
        
        self.API_KEY_ID_URL_TAG = f"?api_key={config.API_KEY}"
        
    def call_api(self, BASE, TAG, list_name):    
        movie_responce = requests.get(BASE + TAG)
        
        if movie_responce.status_code == 200:
            json_data = movie_responce.json()
            try:
                if len(json_data[f'{list_name}']) == 0:
                    print()
                    return
                else:
                    return(json_data)
            except:
                if len(json_data) == 0:
                    print()
                    return
                else:
                    return(json_data)
            
        else:
            print('failed')       

    def get_cast(self, film_id):
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
        
        return(top_cast)

    def get_movie_data(self, BASE, TAG):
        try:
            json_data = self.call_api(BASE, TAG, 'results')
            
            max_results = 5
            
            print("________________________________")
            print()
            print("Results:".upper())
            
            try:
                raw_data = json_data['results'] 
            except:
                raw_data = json_data
            
            while True:
                
                i = 0
                while i < len(raw_data) and i < max_results:
                    print()
                    print(i+1, raw_data[i]['title'])
                    i += 1
                
                if max_results > len(raw_data):
                    print()
                    print("This is the max number of results")
                    print()
                else:
                    print()     
                    print("showing", max_results, "results")
                    print()
                
                which_movie = input_val("enter the corresponding number to select the film, or enter 0 to show more results: ", int)
                if which_movie == 0:
                    max_results += 5
                    continue
                
                results_movie = raw_data[which_movie - 1]
                film_id = results_movie['id']
                break
        
            top_cast = self.get_cast(film_id)
                
            movie = Movie(results_movie['title'], results_movie['release_date'], top_cast, results_movie['overview'], results_movie['vote_average'])
            movie.display_movie_data()   
            
            print("________________________________")
            print()    
            
            add_to_watchlist(results_movie)
            
        except:
            print("-- NO RESULTS FOUND --")
        
    def search_name(self, movie_name):
        self.get_movie_data(self.API_SEARCH_BASE_URL, self.API_SEARCH_TITLE_URL_TAG + movie_name)
        
    def search_year(self, movie_year):
        self.get_movie_data(self.API_DISCOVER_BASE_URL, self.API_DISCOVER_YEAR_URL_TAG + movie_year)
        
    def search_ID(self, movie_ID, add):
        data = self.call_api(self.API_MOVIE_BASE_URL + f'{movie_ID}', self.API_KEY_ID_URL_TAG, '')
        try:
            top_cast = self.get_cast(movie_ID)
            movie = Movie(data['title'], data['release_date'], top_cast, data['overview'], data['vote_average'])
            movie.display_movie_data()
            
            if add == 'add':
                print()
                add_to_watchlist(data)
        
        except:
            print("-- NO RESULTS FOUND --")
            
    def get_trending(self):
        trending_id = []
        print("________________________________")
        print()
        print("Top trending movies:".upper())
        print()
        json_data = self.call_api(self.API_TRENDING_URL, '', 'results')
        
        i = 0
        a = 0
        while i < len(json_data['results']) and a < 10:
            if json_data['results'][i]['media_type'] == 'movie':
                print(f'{a+1})', json_data['results'][i]['title'])
                trending_id.append(json_data['results'][i]['id'])
                a += 1
            i += 1
            
        print()
        while True:
            trending_menu = input_val("Enter the corresponding number to view the film, or enter 0 to return to menu\n", int)
            if trending_menu != 0:
                try:
                    self.search_ID(trending_id[trending_menu - 1], 'add')
                    break
                except:
                    print()
                    print("-- Please either enter 0, or the number corresponding to the film --")
                    print()   
                
            else:
                break
                
movie_watchlist = []         
        
def input_val(question, inp_type):
    """Have the user enter the input and return it if it's an interger."""
    while True:
        try:
            result = inp_type(input(question))
            return result
        except:
            print()
            print('- invalid input -')
            print('please try again')
            print()
    
def add_to_watchlist(results_movie):
    while True:
        add_watchlist = input_val("Do you want to:\n1) Add this film to watchlist\n2) Return to the menu\n", int)
        if add_watchlist == 1:    
            movie_watchlist.append([results_movie['title'], results_movie['id']])
            print()
            print("--- Movie Added to Watchlist ---")
            time.sleep(1.5)
            break
        elif add_watchlist == 2:
            menu()
            break
        else:
            print()
            print("please enter the number corresponding the the question")
            print()
            
def remove_watchlist():  
    while True:    
        remove_watchlist = input_val("Which film do you want to remove from watchlist? ", int)
        try:
            movie_watchlist.pop(remove_watchlist-1)
            break
        except:
            print()
            print("Please enter the number corresponding to a film")
            print()
    
def print_watchlist():
    print()
    print("Watchlist:")
    print()
    i = 0
    while i < len(movie_watchlist):
        print(f'{i+1})', movie_watchlist[i][0])
        i += 1
    
def menu():
    while True:
        api = API()
        
        print("________________________________")
        print()
        print(f"Would you like to:\n1) Show trending movies?\n2) Search for a film?\n3) view watchlist?\n4) Exit?")
        menu_1 = input_val('', int)
        
        if menu_1 == 1:
            api.get_trending()
        
        elif menu_1 == 2: 
            print("________________________________")
            print()
            while True:
                print(f"Would you like to:\n1) Search by name?\n2) Search by year?\n3) Search by ID")
                menu_2 = input_val('', int)
                
                if menu_2 == 1:
                    print()
                    movie_name = input_val("Movie Name: ", str)
                    api.search_name(movie_name)
                    break
                    
                elif menu_2 == 2:
                    print()
                    movie_year = input_val("Movie Year: ", int)
                    api.search_year(f'{movie_year}')
                    break
                
                elif menu_2 == 3:
                    print()
                    ID = input_val("Film ID: ", int)
                    api.search_ID(ID, 'add')
                    break
                    
                else:
                    print()
                    print("please enter the corresponding number to the question")
                    print()
                
        elif menu_1 == 3:
            while True:
                print("________________________________")
                print_watchlist()
                print()
                if len(movie_watchlist) == 0:
                    print("-- Empty --")
                    time.sleep(1)
                    break
                else:
                    print("________________________________")
                    print()
                    menu_watchlist = input_val("1) View a movie in the watchlist\n2) remove a movie from watchlist\n3) return to menu\n", int)
                    if menu_watchlist == 1:
                        watchlist_view = input_val("enter the nummber corresponding to the film ", int)
                        api.search_ID(movie_watchlist[watchlist_view - 1][1], '')
                    elif menu_watchlist == 2:
                        remove_watchlist()
                    elif menu_watchlist == 3:
                        break
                    else:
                        print("invalid input")
            
        elif menu_1 == 4:
            exit()
            
        else:
            print("please enter the corresponding number to the question")
        
if __name__ == "__main__":
    menu()

        



    
    