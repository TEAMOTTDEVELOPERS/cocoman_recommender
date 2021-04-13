import uvicorn
from fastapi import FastAPI

from cocoman_recommender.containers import Container
from cocoman_recommender.routers import contents_controller


def create_app():
    container = Container()
    app = FastAPI()

    """ Define Container """
    container.wire(modules=[contents_controller])

    app.container = container

    """ Initialize Database """
    container.db().create_database()

    """ Initialize Redis """

    """ Define Middleware """

    """ Define Router """
    app.include_router(contents_controller.router, prefix='/contents')

    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
