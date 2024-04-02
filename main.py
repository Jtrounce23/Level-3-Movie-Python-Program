import os 
import time

try:
    import requests
except ImportError:
    print("Please install the requests package by running")
    print("pip install requests")
    print("This program cannot run without the requests package")
    print("Exiting...")
    os._exit(1)

print("________________________________")
print()
print("Welcome to the Movie App")
print()
api_key = str(input("Please enter your TMDB API key here: "))

class Movie():
    def __init__(self, title, year, cast, plot, rating):
        '''
        title: string
        year: string
        cast: string
        plot: string
        rating: float
        '''
        self.title = title
        self.year = year
        self.cast = cast
        self.plot = plot
        self.rating = rating
        
    def display_movie_data(self):
        '''
        Gets all the relevent info for the film and formats it to be displayed nicely
        '''
        
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
        '''
        
        '''
        self.API_BASE_URL = f"https://api.themoviedb.org/3/" #Base URL

        self.API_SEARCH_TITLE_URL_TAG = f"search/movie?api_key={api_key}&query=" #URL tag to search by name
        self.API_DISCOVER_YEAR_URL_TAG = f"discover/movie?api_key={api_key}&primary_release_year=" #URL tag to search by year
        self.API_TRENDING_URL_TAG = f"trending/all/day?api_key={api_key}" #URL tag to get trending movies/tv shows
        
        self.API_MOVIE_URL_TAG = f"movie/" #URL tag for movie
        self.API_CREDITS_URL_TAG = f"/credits?api_key={api_key}" #URL to get credits
        self.API_KEY_URL_TAG = f"?api_key={api_key}" #URL tag for api_key
        
        self.top_cast = []
        
    def call_api(self, TAG, list_name):  
        '''
        calls the api by combining a base and tag url, 
        then it tests whether its worked & if results have been found or not
        '''  
        movie_responce = requests.get(self.API_BASE_URL + TAG)
        
        if movie_responce.status_code == 200:
            json_data = movie_responce.json()
            try:
                if len(json_data[f'{list_name}']) != 0:
                    return(json_data)
            except:
                if len(json_data) != 0:
                    return(json_data)
            
        else:
            print('failed')       

    def get_movie_data(self, TAG):
        '''
        This function is used for searches where there will be multiple results, 
        i.e. when searching for oppenheimer there will be many results with oppenheimer.
        after you enter the film you want it gets the data and gives that to the display_movie_data
        function from the Movie class, to display the info to the user.
        '''
        try: #there are results
            json_data = self.call_api(TAG, 'results')
            
            max_results = 5
            
            print("________________________________")
            print()
            print("Results:".upper())
            
            try: #coming from either search name or year
                raw_data = json_data['results'] 
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
            except: #coming from search ID
                results_movie = json_data
                film_id = results_movie['id']
                
            #This try except works out whether you have come from search ID or not
            #This is important as the data results you get for each are different
            
            cast_data = self.call_api(self.API_MOVIE_URL_TAG + f"{film_id}" + self.API_CREDITS_URL_TAG, 'cast')
            
            cast = (cast_data['cast'])
            self.top_cast = []
            
            i = 0
            a = 0
            while i < len(cast) and a < 5:
                if cast[i]['known_for_department'] == 'Acting':
                    self.top_cast.append(cast[i]['name'])
                    a += 1
                i += 1
                
            movie = Movie(results_movie['title'], results_movie['release_date'], self.top_cast, results_movie['overview'], results_movie['vote_average'])
            movie.display_movie_data()      
           
            i = 0
            a = 1
            while i < len(movie_watchlist):
                if movie_watchlist[i][0] == results_movie['title']:
                    a = 2
                i += 1
            
            #checks if movie is already in watchlist so not to have it in there twice
            
            if a == 1:     
                add_to_watchlist(results_movie)

        except: #no results
            print("-- NO RESULTS FOUND --")
        
    def search_name(self, movie_name):
        '''
        uses get_movie_data function to search for a film by name
        '''
        self.get_movie_data(self.API_SEARCH_TITLE_URL_TAG + movie_name)
        
    def search_year(self, movie_year):
        '''
        uses the get_movie_data function to search for top movies by year released
        '''
        self.get_movie_data(self.API_DISCOVER_YEAR_URL_TAG + movie_year)
        
    def search_ID(self, movie_ID):
        '''
        when searching for ID there should only be one result, hence why it doesnt use get_movie_data,
        instead it simply uses the call_api function to acquire the data, as well as the get cast, and then
        gives it to the display_movie_data function from the Movie class to present it.
        '''
        self.get_movie_data(self.API_MOVIE_URL_TAG + f'{movie_ID}' + self.API_KEY_URL_TAG)
            
    def get_trending(self):
        '''
        uses the call_api function to get trending, and then sorts the movies from tv series to give the 10 trending movies 
        '''
        trending_id = []
        print("________________________________")
        print()
        print("Top trending movies:".upper())
        print()
        json_data = self.call_api(self.API_TRENDING_URL_TAG, 'results')
        
        i = 0
        a = 0
        while i < len(json_data['results']) and a < 10:
            if json_data['results'][i]['media_type'] == 'movie':
                print(f'{a+1})', json_data['results'][i]['title'])
                trending_id.append(json_data['results'][i]['id'])
                a += 1
            i += 1
            
        #This uses call_api to get all the trending movies, however this gets a combination of movies & tv series,
        #so the function has to sort the movies from the tv series then stores the id in a list.
            
        print()
        while True:
            trending_menu = input_val("Enter the corresponding number to view the film, or enter 0 to return to menu\n", int)
            if trending_menu != 0:
                try:
                    self.search_ID(trending_id[trending_menu - 1])
                    break
                except:
                    print()
                    print("-- Please either enter 0, or the number corresponding to the film --")
                    print()   
                
            else:
                break
            
        #The reason it stores the id is so that if the user wants to see the movie info for a trending film, 
        #it doesnt give multiple results by that name, and can instead search by ID
                
api = API()                           
movie_watchlist = []        
        
def input_val(question, inp_type):
    """Have the user enter the input and return it dependant on the input type"""
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
    '''
    allows the user to append a movie the the watchlist, or return to the menu if they dont
    '''
    while True:
        print("________________________________")
        print()
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
    '''
    This allows the user to remove a movie from the watchlist
    '''
    while True:    
        remove_watchlist = input_val("Which film do you want to remove from watchlist? ", int)
        try:
            movie_watchlist.pop(remove_watchlist-1)
            break
        except:
            print()
            print("Please enter the number corresponding to a film")
            print()
        #
    
def print_watchlist():
    '''
    prints each movie name in the watchlist, then asks the user whether they would like to 
    view a movie, remove a movie, or return back to the menu 
    '''
    while True:
        print("________________________________")
        print()
        print("Watchlist:")
        print()
        i = 0
        while i < len(movie_watchlist):
            print(f'{i+1})', movie_watchlist[i][0])
            i += 1
            
        #prints each movie in the watchlist
            
        print()
        if len(movie_watchlist) == 0:
            print("-- Empty --")
            time.sleep(1)
            break
            #checks to see if watchlist is empty
        else:
            print("________________________________")
            print()
            menu_watchlist = input_val("1) View a movie in the watchlist\n2) remove a movie from watchlist\n3) return to menu\n", int)
            if menu_watchlist == 1:
                watchlist_view = input_val("enter the nummber corresponding to the film ", int)
                api.search_ID(movie_watchlist[watchlist_view - 1][1])
            elif menu_watchlist == 2:
                remove_watchlist()
            elif menu_watchlist == 3:
                break
            else:
                print("invalid input")
                
            #uses search_ID to get movie data as similar to the trending function the ID is stored in the watchlist for convenience
            #uses remove_watchlist function to remove a movie 
    
def menu():
    '''
    menu function, asks the user what they would like to do, and they respond by entering the corresponding number
    '''
    while True:
        
        print("________________________________")
        print()
        print(f"Would you like to:\n1) Show trending movies?\n2) Search for a film?\n3) view watchlist?\n4) Exit?")
        #main menu
        main_menu = input_val('', int)
        
        if main_menu == 1: #gets top 10 trending movies
            api.get_trending()
        
        elif main_menu == 2: #search menu
            print("________________________________")
            print()
            while True:
                print(f"Would you like to:\n1) Search by name?\n2) Search by year?\n3) Search by ID")
                menu_search = input_val('', int)
                
                if menu_search == 1: #search by name
                    print()
                    movie_name = input_val("Movie Name: ", str)
                    api.search_name(movie_name)
                    break
                    
                elif menu_search == 2: #search by year of release
                    print()
                    movie_year = input_val("Movie Year: ", int)
                    api.search_year(f'{movie_year}')
                    break
                
                elif menu_search == 3: #search by movie ID
                    print()
                    ID = input_val("Film ID: ", int)
                    api.search_ID(ID)
                    break
                    
                else: 
                    print()
                    print("please enter the corresponding number to the question")
                    print()
                
        elif main_menu == 3: #prints watchlist
            print_watchlist()
            
        elif main_menu == 4: #exits
            exit()
            
        else:
            print("please enter the corresponding number to the question")
        
if __name__ == "__main__":
    menu()