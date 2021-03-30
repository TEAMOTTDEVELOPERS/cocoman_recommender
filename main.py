import uvicorn
from fastapi import FastAPI

from cocoman_recommender.config.config import conf
from cocoman_recommender.schemas.contents import Contents
from cocoman_recommender.schemas.ott import Ott
from cocoman_recommender.schemas.actor import Actor
from cocoman_recommender.schemas.director import Director
from cocoman_recommender.schemas.genre import Genre
from cocoman_recommender.schemas.keyword import Keyword
from cocoman_recommender.schemas.review import Review
from cocoman_recommender.schemas.user import User
from cocoman_recommender.schemas.star_rating import StarRating
from cocoman_recommender.schemas.search_history import SearchHistory

from cocoman_recommender.containers import Container
from cocoman_recommender.routers import ott_controller


def create_app():
    container = Container()
    app = FastAPI()

    """ Define Container """
    container.wire(modules=[ott_controller])

    app.container = container

    """ Initialize Database """
    container.db().create_database()

    """ Initialize Redis """

    """ Define Middleware """

    """ Define Router """
    app.include_router(ott_controller.router)

    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
