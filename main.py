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


class Movie():
    """Attains movie info and uses it to display it"""

    def __init__(self, title, year, cast, plot, rating):
        """
        title: string
        year: string
        cast: string
        plot: string
        rating: float
        """
        self.title = title
        self.year = year
        self.cast = cast
        self.plot = plot
        self.rating = rating

    def display_movie_data(self):
        """Get all the relevent info for the film and format it to be displayed nicely."""
        print("________________________________\n")
        print(f"""Title: {self.title}\nRelease Date: {self.year}
Vote Average: {self.rating}\n\nPlot: {self.plot}""")
        print()

        print("Top Cast:\n")
        i = 0
        while i < len(self.cast):
            print(self.cast[i])
            i += 1


class API():
    """This class involves everything to do with the API"""

    def __init__(self):
        """
        URL's for the TMDB api
        """
        self.API_BASE_URL = "https://api.themoviedb.org/3/"  # Base URL

        self.API_SEARCH_TITLE_URL_TAG = f"search/movie?api_key={api_key}&query="  # URL tag to search by name
        self.API_DISCOVER_YEAR_URL_TAG = f"discover/movie?api_key={api_key}&primary_release_year="  # URL tag to search by year
        self.API_TRENDING_URL_TAG = f"trending/all/day?api_key={api_key}"  # URL tag to get trending movies/tv shows

        self.API_MOVIE_URL_TAG = "movie/"  # URL tag for movie
        self.API_CREDITS_URL_TAG = f"/credits?api_key={api_key}"  # URL to get credits
        self.API_KEY_URL_TAG = f"?api_key={api_key}"  # URL tag for api_key

        self.top_cast = []

    def call_api(self, tag, list_name):
        """call the api by combining a base and tag url.
        It then tests whether its worked & if results have been found or not
        """
        try:
            movie_responce = requests.get(self.API_BASE_URL + tag)

            if movie_responce.status_code == 200:  # This means the movie responce worked fine
                json_data = movie_responce.json()
                try:
                    if len(json_data[f'{list_name}']) != 0:
                        return(json_data)
                except:
                    if len(json_data) != 0:
                        return(json_data)
            else:
                print('-- failed to call API --')  # When movie responce doesn't work
        except:
            print("-- Failed to access API --")
            return("Failed")

    def get_movie_data(self, tag):
        """Get the info for a film using the results of the call API.
        It has to understand what kind of results it has,
        then sends it to the display movie in Movie class 
        """
        try:  # there are results
            
            json_data = self.call_api(tag, 'results')

            if json_data != "Failed":  # checking if json_data didn't work
                max_results = 5

                print("________________________________\n\nRESULTS:")

                try:  # for when there are multiple films
                    raw_data = json_data['results']
                    while True:
                        i = 0
                        while i < len(raw_data) and i < max_results:
                            print()
                            print(i+1, raw_data[i]['title'])
                            i += 1

                        if max_results > len(raw_data):
                            print("\nThis is the max number of results\n")
                        else:
                            print("\nshowing", max_results, "results\n")

                        which_movie = input_val("enter the corresponding number to select the film, or enter 0 to show more results: ", int)
                        if which_movie == 0:
                            max_results += 5
                            continue

                        results_movie = raw_data[which_movie - 1]
                        film_id = results_movie['id']
                        break
                except: # for when there is only one film
                    results_movie = json_data
                    film_id = results_movie['id']

                # This try except works out whether you have come from search ID or not
                # This is important as the data results you get for each are different

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

            # checks if movie is already in watchlist so not to have it in there twice

            if a == 1:
                add_to_watchlist(results_movie)

        except:  # no results
            print("-- NO RESULTS FOUND --")

    def search_name(self, movie_name):
        """use get_movie_data function to search for a film by name"""
        self.get_movie_data(self.API_SEARCH_TITLE_URL_TAG + movie_name)

    def search_year(self, movie_year):
        """use the get_movie_data function to search for top movies by year released"""
        self.get_movie_data(self.API_DISCOVER_YEAR_URL_TAG + movie_year)
        
    def search_ID(self, movie_ID):
        """use the get_movie_data function to get movie by ID"""
        self.get_movie_data(self.API_MOVIE_URL_TAG + f'{movie_ID}' + self.API_KEY_URL_TAG)

    def get_trending(self):
        """use the call_api function to get trending. 
        It then sorts the movies from tv series to give the 10 trending movies
        """
        trending_id = []
        print("________________________________\n\nTOP TRENDING MOVIES:\n")
        
        json_data = self.call_api(self.API_TRENDING_URL_TAG, 'results')
        
        if json_data != "Failed":
            i = 0
            a = 0
            while i < len(json_data['results']) and a < 10:
                if json_data['results'][i]['media_type'] == 'movie':
                    print(f'{a+1})', json_data['results'][i]['title'])
                    trending_id.append(json_data['results'][i]['id'])
                    a += 1
                i += 1

        # This uses call_api to get all the trending movies, however this gets a combination of movies & tv series,
        # so the function has to sort the movies from the tv series then stores the id in a list.

        print()
        while True:
            trending_menu = input_val("Enter the corresponding number to view the film, or enter 0 to return to menu\n", int)
            if trending_menu != 0:
                try:
                    self.search_ID(trending_id[trending_menu - 1])
                    break
                except:
                    print("\n-- Please enter the number corresponding to the question --\n")
            else:
                break

        # The reason it stores the id is so that if the user wants to see the movie info for a trending film,
        # it doesnt give multiple results by that name, and can instead search by ID


while True:
    api_key = str(input("Please enter your TMDB API key here: "))
    try:
        test_data = requests.get(f"https://api.themoviedb.org/3/trending/all/day?api_key={api_key}")
        if test_data.status_code == 200:
            break
        else:
            print("\n-- ERROR --\nlease check your API key is correct\n\n________________________________\n")
            continue
    except:
        print("\n-- ERROR --\nplease check your connection is working\n\n________________________________\n")
        continue

# gets the API key & checks if its valid, along with the connection

api = API()
movie_watchlist = []


def input_val(question, inp_type):
    """Have the user enter the input and return it dependant on the input type"""
    while True:
        try:
            result = inp_type(input(question))
            if inp_type == int:
                if result > -1:
                    return result
                else:
                    print('\nPlease enter the number corresponding to the question\n')
            else:
                return result
        except:
            print('\n- invalid input -')
            print('please try again\n')


def add_to_watchlist(results_movie):
    """allow the user to append a movie the the watchlist or return to the menu if they dont"""
    while True:
        print("________________________________\n")
        add_watchlist = input_val("Do you want to:\n1) Add this film to watchlist\n2) Return to the menu\n", int)
        if add_watchlist == 1:
            movie_watchlist.append([results_movie['title'], results_movie['id']])  # Adds both the title and id of each film into the watchlist
            print("\n--- Movie Added to Watchlist ---")
            time.sleep(1.5)
            break
        elif add_watchlist == 2:  # Returns to menu
            menu()
            break
        else:
            print("\nplease enter the number corresponding the the question\n")


def remove_watchlist():
    """Allow the user to remove a movie from the watchlist"""
    while True:
        remove_watchlist = input_val("Which film do you want to remove from watchlist? ", int)
        try:
            movie_watchlist.pop(remove_watchlist-1)  # Removes both the name and id of a movie from the watchlist
            break
        except:
            print("\nPlease enter the number corresponding to a film\n")


def print_watchlist():
    """print each movie name in the watchlist.
    Then it asks the user whether they would like to view a movie, remove a movie, or return back to the menu
    """
    while True:
        print("________________________________")
        print("\nWatchlist:\n")
        i = 0
        while i < len(movie_watchlist):
            print(f'{i+1})', movie_watchlist[i][0])
            i += 1

        # prints each movie in the watchlist

        print()
        if len(movie_watchlist) == 0:
            print("-- Empty --")
            time.sleep(1)
            break
            # checks to see if watchlist is empty
        else:
            print("________________________________\n")
            menu_watchlist = input_val("1) View a movie in the watchlist\n2) remove a movie from watchlist\n3) return to menu\n", int)
            if menu_watchlist == 1:
                watchlist_view = input_val("enter the nummber corresponding to the film ", int)
                api.search_ID(movie_watchlist[watchlist_view - 1][1])
            elif menu_watchlist == 2:
                remove_watchlist()
            elif menu_watchlist == 3:
                break
            else:
                print("Please enter the number corresponding to the question")

            # uses search_ID to get movie data as similar to the trending function the ID is stored in the watchlist for convenience
            # uses remove_watchlist function to remove a movie


def menu():
    """menu function.
    Asks the user what they would like to do, and they respond by entering the corresponding number
    """
    while True:
        print("________________________________\n")
        print(f"Would you like to:\n1) Show trending movies?\n2) Search for a film?\n3) view watchlist?\n4) Exit?")
        # main menu
        main_menu = input_val('', int)

        if main_menu == 1: # gets top 10 trending movies
            api.get_trending()

        elif main_menu == 2: # search menu
            print("________________________________\n")
            while True:
                print(f"Would you like to:\n1) Search by name?\n2) Search by year?\n3) Search by ID")
                menu_search = input_val('', int)

                if menu_search == 1: # search by name
                    print()
                    movie_name = input_val("Movie Name: ", str)
                    api.search_name(movie_name)
                    break

                elif menu_search == 2: # search by year of release
                    print()
                    movie_year = input_val("Movie Year: ", int)
                    if movie_year > 1850 and movie_year < 2030:
                        api.search_year(f'{movie_year}')
                    else:
                        print("\n-- NO RESULTS FOUND --\n")
                    break

                elif menu_search == 3: # search by movie ID
                    print()
                    ID = input_val("Film ID: ", int)
                    api.search_ID(ID)
                    break

                else:
                    print("\nplease enter the corresponding number to the question\n")

        elif main_menu == 3: # prints watchlist
            print_watchlist()

        elif main_menu == 4: # exits
            exit()

        else:
            print("please enter the corresponding number to the question")


if __name__ == "__main__":
    menu()