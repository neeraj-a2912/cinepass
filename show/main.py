import os
from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from api import User_api, Theatre_api, Show_api, User_Login_api, Booking_api, ShowById, SearchApi, TheatreById, AllShowsApi
from models import db
from flask_jwt_extended import JWTManager, jwt_required
from celery_configuration import create_celery
from cache_configuration import create_cache
import celery_tasks

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["JWT_SECRET_KEY"] = "jwttokenaccesssforticketshow"  
app.config['BROKER_URL'] = 'redis://localhost:6379/0'
app.config['RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['TIME_ZONE'] = 'Asia/Kolkata'
jwt = JWTManager(app)
api = Api(app)
celery = create_celery(app)
cache = create_cache(app)
app.config['SECRET_KEY'] = 'ticketshowapp'
db.init_app(app)
app.app_context().push()


api.add_resource(User_api, '/api/user', '/api/user/<int:id>')
api.add_resource(Theatre_api, '/api/theatre', '/api/theatre/<int:theatre_id>')
api.add_resource(Show_api, '/api/show/<int:theatre_id>',
                 '/api/show/<int:theatre_id>/<int:show_id>')
api.add_resource(ShowById,  '/api/show-details/<int:show_id>')
api.add_resource(User_Login_api, '/api/login')
api.add_resource(Booking_api, '/api/booking/<int:show_id>', '/api/bookings/user/<int:user_id>')
api.add_resource(SearchApi, '/api/search/<string:toBeSearched>')
api.add_resource(TheatreById, '/api/theatre-details/<int:theatre_id>')
api.add_resource(AllShowsApi,'/api/get-all-shows')

class ExportTheatreApi(Resource):

    @jwt_required()
    def post(self, theatre_id):
        task = celery_tasks.exTheatre.delay(theatre_id)
        task_result = task.get()
        print(task_result)
        return {"file_path":task_result, "task_id":task.id}, 200

class ExportShowApi(Resource):

    @jwt_required()
    def get(self, show_id):
        celery_tasks.exShow.delay(show_id)
        return 'success', 200

api.add_resource(ExportTheatreApi, '/api/export/theatre/<int:theatre_id>')
api.add_resource(ExportShowApi, '/api/export/show/<int:show_id>')

if __name__ == "__main__":
    app.run(debug=True, port=5000)