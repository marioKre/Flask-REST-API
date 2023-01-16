from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from os import path

# Create a new flask application
app = Flask(__name__)
# Initialize an api object for the application
api = Api(app)

# Configuring database URI and disabling modification tracking
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Defining Movie database model with its fields and primary key
class MovieModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    imdb_rating = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(30), nullable=False)
    actors = db.Column(db.String(150), nullable=False)
    director = db.Column(db.String(100), nullable=False)

    # Return a string representation of an instance of the class.
    # Contains values of 'name', imdb_raint'...attributes of the movie object
    def __repr__(self):
        return f"Movie(name = {self.name}, imdb_rating = {self.imdb_rating}, genre = {self.genre}, actors = {self.actors}, director = {self.director})"

# Checks if database already exists and creates it if it doesn't exist
if not path.exists('database.db'):
        with app.app_context():
            db.create_all()

# Create a parser that will be used to parse the JSON data sent in the request body for the PUT request
movie_put_args = reqparse.RequestParser()
movie_put_args.add_argument("name", type=str, help="Name of the movie is required", required=True)
movie_put_args.add_argument("imdb_rating", type=str, help="IMDB rating of the movie is required", required=True)
movie_put_args.add_argument("genre", type=str, help="Genre of the movie is required", required=True)
movie_put_args.add_argument("actors", type=str, help="Actors of the movie are required", required=True)
movie_put_args.add_argument("director", type=str, help="Director of the movie is required", required=True)

# Create a parser that will be used to parse the JSON data sent in the request body for the PATCH request
movie_update_args = reqparse.RequestParser()
movie_update_args.add_argument("name", type=str)
movie_update_args.add_argument("imdb_rating", type=str)
movie_update_args.add_argument("genre", type=str)
movie_update_args.add_argument("actors", type=str)
movie_update_args.add_argument("director", type=str)

# Setting fields that will be returned in the response
# Used to specify the fields that should be included in the JSON representation of a movie resource
resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'imdb_rating' : fields.Integer,
    'genre' : fields.String,
    'actors' : fields.String,
    'director' : fields.String,
}


# The movie class, inherits from the Flask-RESTful Resource
class Movie(Resource):

    # Decorator is used to specify that this representation should be used 
    # when converting movie resources to JSON when handling HTTP requests and responses.
    @marshal_with(resource_fields)
    def get(self, movie_id):
        # Get method to retrieve a movie by id
        result = MovieModel.query.filter_by(id=movie_id).first()
        if not result:
            # Returning error if movie is not found
            abort(404, message="Couldn't find movie with given ID")
        return result

    @marshal_with(resource_fields)
    def put(self, movie_id):
        # Parsing and validating request data
        args = movie_put_args.parse_args()
        # Checking if movie id and name already exist
        id_result = MovieModel.query.filter_by(id=movie_id).first()
        name_result =  MovieModel.query.filter_by(name=args['name']).all()   
        if id_result:
            # Returning error if movie id is already taken
            abort(409, message="Movie id already taken")
        elif name_result:
            # Returning error if movie name is already taken
            abort(409, message="Movie name already taken")
        movie  =  MovieModel(
            id=movie_id, 
            name=args['name'], 
            imdb_rating=args['imdb_rating'], 
            genre=args['genre'], 
            actors=args['actors'], 
            director=args['director']
            )
        # Adding movie to the database
        db.session.add(movie)
        db.session.commit()
        return movie, 201

    @marshal_with(resource_fields)
    def patch(self, movie_id):
        # Parsing and validating request data
        args = movie_update_args.parse_args()
        # Querying movie by id and name
        result = MovieModel.query.filter_by(id=movie_id).first()
        name_result =  MovieModel.query.filter_by(name=args['name']).all()   
        if not result:
            abort(404, message="Couldn't find movie with given ID")
        elif name_result:
            abort(409, message= "Name of the movie already used")
        #  Updating movie fields with request data
        if args['name']:
            result.name = args['name']
        if args['imdb_rating']:
            result.imdb_rating = args['imdb_rating']
        if args['genre']:
            result.genre = args['genre']
        if args['actors']:
            result.actors = args['actors']
        if args['director']:
            result.director = args['director']
        db.session.add(result)
        db.session.commit()
        return result

    @marshal_with(resource_fields)
    def delete(self, movie_id):
        movie = MovieModel.query.filter_by(id=movie_id).first()
        if not movie:
            abort(404, message="Couldn't find movie with given ID")
        db.session.delete(movie)
        db.session.commit()
        return 200


# Map the movie resource to the '/movie/<int:movie>' endpoint
api.add_resource(Movie, "/movie/<int:movie_id>")

# Run the application in debug mode
if __name__ == "__main__":
    app.run(debug=True)
