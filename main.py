import webapp2
import jinja2
import os

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

# a list of movies that nobody should be allowed to watch
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Zardoz",
    "Nine Lives"
]

watchlist = [
    "Minions",
    "Freaky Friday",
    "Star Wars",
    "My Favorite Martian"
]

def getCurrentWatchlist():
    """ Returns the user's current watchlist """

    # for now, we are just pretending
    return sorted(watchlist)


class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """

    def get(self):
        t = jinja_env.get_template("edit.html")
        error = self.request.get("error")
        content = t.render(watchlist=getCurrentWatchlist(), error=error)
        self.response.write(content)

class AddMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/add'
        e.g. www.flicklist.com/add
    """

    def post(self):
        new_movie = self.request.get("new-movie")

        # if the user typed nothing at all, redirect and yell at them
        if (not new_movie) or (new_movie.strip() == ""):
            error = "Please specify the movie you want to add."
            self.redirect("/?error=" + error)
        elif new_movie in terrible_movies:
            error = "Trust me, you don't want to add '{0}' to your Watchlist.".format(new_movie)
            self.redirect("/?error=" + error)
        elif new_movie in watchlist:
            error = "'{0}' is already in your Watchlist.".format(new_movie)
            self.redirect("/?error=" + error)
        else:
            watchlist.append(new_movie)

        # render confirmation page
        t = jinja_env.get_template("add.html")
        content = t.render(new_movie=new_movie)
        self.response.write(content)


class CrossOffMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/cross-off'
        e.g. www.flicklist.com/cross-off
    """

    def post(self):
        crossed_off_movie = self.request.get("crossed-off-movie")

        if not crossed_off_movie or crossed_off_movie.strip() == "":
            error = "Please specify a movie to cross off."
            self.redirect("/?error=" + error)

        # if user tried to cross off a movie that is not in their list, reject
        if not (crossed_off_movie in getCurrentWatchlist()):
            # make a helpful error message
            error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(crossed_off_movie)

            # redirect to homepage, and include error as a query parameter in the URL
            self.redirect("/?error=" + error)


        watchlist.remove(crossed_off_movie)

        # render confirmation page
        t = jinja_env.get_template("cross-off.html")
        content = t.render(crossed_off_movie=crossed_off_movie)
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', AddMovie),
    ('/cross-off', CrossOffMovie)
], debug=True)
