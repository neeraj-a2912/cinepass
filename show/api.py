import datetime
from flask import request
from flask_restful import Resource, fields, marshal_with
from custom_errors import DataError, LogicError
from models import User, db, Theatre, Show, Booking
from flask_jwt_extended import create_access_token, jwt_required


class User_api(Resource):
    '''Api code for Login_db table'''

    output = {"id": fields.Integer, "email": fields.String,
              "password": fields.String, "name":fields.String, "role":fields.String}

    @jwt_required()
    @marshal_with(output)
    def get(self, id: int):
        '''Returns the User details for the given email'''

        user = User.query.filter_by(id=id).first()

        # Checking whether user record is present
        if user is None:
            return {'message':'User not found'}, 400

        db.session.commit()
        return user, 200

    @jwt_required()
    @marshal_with(output)
    def put(self, name: str):
        '''Modifies the User details for the given name'''

        user = User.query.filter_by(name=name).first()

        # Checking whether user record is present
        if user is None:
            raise DataError(status_code=404)

        data =request.get_json()

        if(data.get("name")):
            user.name = data.get("name")
        
        if(data.get("email")):
            user.email = data.get("email")

        if(data.get("password")):
            user.password = data.get("password")

        db.session.commit()
        return user, 200

    @jwt_required()
    def delete(self, name: str):
        '''Deletes the User details for the given name'''

        user = User.query.filter_by(name=name).first()

        # Checking whether user record is present
        if user is None:
            raise DataError(status_code=404)

        db.session.delete(user)
        db.session.commit()
        return '', 200

    @marshal_with(output)
    def post(self):
        '''Creates a new User'''

        data = request.get_json()
        user = User(email=data.get("email"),
                   password=data.get("password"),
                   name=data.get("name"), role=data.get("role"))

        # Checking whether a user record with same email is present
        if User.query.filter_by(email=user.email).first():
            raise DataError(status_code=409)

        db.session.add(user)
        db.session.commit()
        return user, 201

class User_Login_api(Resource):

    def post(self):
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if user is None:
            return {"message":"User not Found", "user": True, "status":False }, 400
        
        if password!=user.password:
            return {"message":"Password is Incorrect", "password": True, "status":False }, 400
        
        user.last_logged = datetime.datetime.now()
        db.session.commit()
        expires = datetime.timedelta(days=5)

        access_token = create_access_token(identity=user.id, expires_delta=expires)

        return {'access_token': access_token, "user_id": user.id, "role":user.role, "name":user.name, "status":True }, 200

class Theatre_api(Resource):
    '''Api code for Theatre table'''

    output = {"place": fields.String, "id": fields.Integer,
              "name": fields.String, "screens":fields.Integer, 
              "shows": fields.Integer(attribute=lambda theatre:len(theatre.shows))}

    @jwt_required()
    @marshal_with(output)
    def get(self):
        ''' Returns List of all the theatres '''
        
        theatres = Theatre.query.all()

        return theatres, 200

    @jwt_required()
    @marshal_with(output)
    def put(self, theatre_id):
        ''' Modifies the Theatre details for the given theatre_id '''

        theatre = Theatre.query.filter_by(id=theatre_id).first()

        if theatre is None:
            raise DataError(status_code=404)

        data = request.get_json()

        if(data.get('name')):
            theatre.name = data.get('name')

        if(data.get('place')):
            theatre.place = data.get('place')
        
        if(data.get("screens")):
            theatre.screens = data.get('screens')
        

        db.session.commit()
        return theatre, 202

    @jwt_required()
    def delete(self, theatre_id):
        
        '''Deletes the List details for the given list_id'''
        shows = Show.query.filter_by(theatre_id=theatre_id).all()
        
        for show in shows:
            for booking in show.bookings:
                db.session.delete(booking)
            db.session.delete(show)

        theatre = Theatre.query.filter_by(id=theatre_id).first()

        if theatre is  None:
            raise DataError(status_code=404)

        db.session.delete(theatre)
        db.session.commit()
        return '', 200

    @jwt_required()
    @marshal_with(output)
    def post(self):

        ''' Creates a new Theatre '''

        data = request.get_json()
        theatre = Theatre(name=data.get("name"), place=data.get('place'), screens=data.get('screens'))

        db.session.add(theatre)
        db.session.commit()
        return theatre, 201

class Show_api(Resource):
    '''Api code for Show table'''

    output = { "id": fields.Integer, "theatre_id": fields.Integer,
               "name": fields.String, "ratings": fields.Integer,
               "ticket_price": fields.Integer, "tags": fields.String, "capacity": fields.Integer, 
               "screen_number":fields.Integer, "show_timing":fields.String, "show_date":fields.String,
               "theatre": fields.String(attribute=lambda show:show.theatre.name),
               "place": fields.String(attribute=lambda show:show.theatre.place) }

    @jwt_required()
    @marshal_with(output)
    def get(self, theatre_id):

        '''Returns all the show details under the given theatre_id'''

        theatre = Theatre.query.filter_by(id=theatre_id).first()
        # Checking whether theatre record is present
        if theatre is None:
            raise DataError(status_code=404)

        shows = Show.query.filter_by(theatre_id=theatre_id).all()
        shows.reverse()


        db.session.commit()
        return shows, 200


    @jwt_required()
    @marshal_with(output)
    def put(self, show_id, theatre_id):
        '''Modifies the Show details for the given show_id'''

        show = Show.query.filter_by(id=show_id, theatre_id=theatre_id).first()

        # Checking whether show record is present
        if show is None:
            raise DataError(status_code=404)

        data = request.get_json()

        if(data.get('name')):
            show.name = data.get('name')

        if(data.get('tags')):
            show.tags = data.get('tags')

        if(data.get('ratings')):
            show.ratings = data.get('ratings')

        if(data.get('ticket_price')):
            show.ticket_price = data.get('ticket_price')

        if(data.get('capacity')):
            show.capacity = data.get('capacity')

        if(data.get('screen_number')):
            show.screen_number = data.get('screen_number')

        if(data.get('show_timing')):
            show.show_timing = data.get('show_timing')

        if(data.get('show_date')):
            show.show_date = data.get('show_date')


        db.session.commit()
        return show, 202

    @jwt_required()
    def delete(self, show_id, theatre_id):

        '''Deletes the Show details for the given show_id'''
        show = Show.query.filter_by(id=show_id, theatre_id=theatre_id).first()

        for booking in show.bookings:
            print(f"deleted {booking.show.name}")
            db.session.delete(booking)

        theatre = Theatre.query.filter_by(id=theatre_id).first()
        
        # Checking whether show record is present
        if not show:
            raise DataError(status_code=404)
        

        db.session.delete(show)
        theatre.screens += 1
        db.session.commit()
        return '', 200

    @jwt_required()
    @marshal_with(output)
    def post(self, theatre_id):
        '''Creates a new Show'''

        theatre = Theatre.query.filter_by(id=theatre_id).first()
        # Checking whether Theatre record is present
        if theatre is None:
            raise DataError(status_code=404)

        data = request.get_json()
        show = Show(theatre_id=theatre_id, name=data.get('name'), ratings=data.get('ratings'),
                   tags=data.get('tags'), ticket_price=data.get('ticket_price'), capacity = data.get('capacity'),
                   screen_number=data.get('screen_number'), show_timing =  data.get('show_timing'), show_date=data.get('show_date'))

        theatre.screens -= 1

        # Checking whether a Show record with same title and list_id is present
        if Show.query.filter_by(name=show.name, theatre_id=theatre_id).first():
            raise DataError(status_code=409)


        db.session.add(show)
        db.session.commit()
        return show, 201

class ShowById(Resource):

    output = {"id": fields.Integer, "theatre_id": fields.Integer,
                "name": fields.String, "ratings": fields.Integer,
                "ticket_price": fields.Integer, "tags": fields.String, 
                "capacity": fields.Integer, "theatre_name": fields.String(attribute = lambda show : show.theatre.name),
                "screen_number": fields.Integer, "show_timing": fields.String, "show_date":fields.String }

    @jwt_required()
    @marshal_with(output)
    def get(self, show_id):
        ''' Returns Show details given the show id '''

        show = Show.query.get(show_id)
        print(show.bookings)

        if show is None:
            raise DataError(status_code=404)
        
        db.session.commit()
        return show, 200
    
class TheatreById(Resource):

    output = {"place": fields.String, "id": fields.Integer,
              "name": fields.String, "screens":fields.Integer}

    @jwt_required()
    @marshal_with(output)
    def get(self, theatre_id):
        ''' Returns Show details given the show id '''

        theatre = Theatre.query.get(theatre_id)

        if theatre is None:
            raise DataError(status_code=404)
        
        db.session.commit()
        return theatre, 200

class Booking_api(Resource):
    '''Api code for Show table'''

    output = {"id": fields.Integer, "show_id": fields.Integer, "user_id": fields.Integer,
              "number_of_tickets": fields.Integer, "booking_time": fields.DateTime, "total_price": fields.Integer, "current_price":fields.Integer,
              "show_timing" : fields.String(attribute=lambda booking:booking.show.show_timing),
              "show_date" : fields.String(attribute=lambda booking:booking.show.show_date),
              "name": fields.String(attribute=lambda booking:booking.show.name), 
              "screen": fields.String(attribute = lambda booking: booking.show.screen_number),
              "theatre":fields.String(attribute = lambda booking : booking.show.theatre.name),
              "location":fields.String(attribute = lambda booking : booking.show.theatre.place) }

    @jwt_required()
    @marshal_with(output)
    def get(self, user_id):

        '''Returns all the bookings of the given user_id'''
        bookings = Booking.query.filter_by(user_id = user_id).all()
        # Checking whether booking record is present
        if bookings is None:
            raise DataError(status_code=404)
        bookings.reverse()
        db.session.commit()
        return bookings, 200

    @jwt_required()
    @marshal_with(output)
    def put(self, booking_id, user_id):
        '''Modifies the Show details for the given show_id'''

        booking = Booking.query.filter_by(id = booking_id, user_id = user_id).first()

        # Checking whether show record is present
        if booking is None:
            raise DataError(status_code=404)

        data = request.get_json()

        if(data.get('number_of_tickets')):
            booking.number_of_tickets = data.get('number_of_tickets')


        db.session.commit()
        return booking, 202


    @jwt_required()
    @marshal_with(output)
    def post(self, show_id):
        '''Creates a new booking'''

        data = request.get_json()

        show = Show.query.filter_by(id=show_id).first()

        current_price = show.ticket_price
        total_price = data.get("number_of_tickets")*current_price

        booking = Booking(user_id=data.get('user_id'), 
                          show_id=show_id, number_of_tickets = data.get('number_of_tickets'), 
                          total_price = total_price, current_price = current_price)

        show.capacity = show.capacity - data.get('number_of_tickets')

        db.session.add(booking)
        db.session.commit()
        return booking, 201

class SearchApi(Resource):

    @jwt_required()
    def get(self, toBeSearched):
        theatre_results = Theatre.query.filter(Theatre.name.like(f'%{toBeSearched}%') | Theatre.place.like(f'%{toBeSearched}%')).all()
        show_results = Show.query.filter(Show.name.like(f'%{toBeSearched}%') | Show.tags.like(f'%{toBeSearched}%')).all()
        
        theatre_results.reverse()
        show_results.reverse()

        result = {
            'shows' : [ { "id":show.id, "name" : show.name, "theatre" : show.theatre.name, "location": show.theatre.place } for show in show_results],
            'theatres' : [ { "id":theatre.id, "name": theatre.name, "place": theatre.place } for theatre in theatre_results]
        }
        db.session.commit()
        return result, 200

class AllShowsApi(Resource):
    
    output = { "id": fields.Integer, "theatre_id": fields.Integer,
               "name": fields.String, "ratings": fields.Integer,
               "ticket_price": fields.Integer, "tags": fields.String, "capacity": fields.Integer, 
               "screen_number":fields.Integer, "show_timing":fields.String, "show_date":fields.String,
               "theatre": fields.String(attribute=lambda show:show.theatre.name),
               "place": fields.String(attribute=lambda show:show.theatre.place) }
    
    @jwt_required()
    @marshal_with(output)
    def get(self):
        allShows = Show.query.all()
        print(allShows)
        shows = []
        for show in allShows:
            print(datetime.datetime.strptime(show.show_date, '%Y-%m-%d'), datetime.datetime.today())
            if datetime.datetime.strptime(show.show_date, '%Y-%m-%d') >= datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0):
                shows.append(show)
        shows.reverse()
        print(shows)
        return shows, 200