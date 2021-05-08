from dependency_injector import containers, providers

from dataclasses import asdict
from cocoman_recommender.config.config import conf
from cocoman_recommender.schemas.conn import Database
from cocoman_recommender.schemas.ott import OttRepository
from cocoman_recommender.schemas.contents import ContentsRepository
from cocoman_recommender.schemas.actor import ActorRepository
from cocoman_recommender.schemas.director import DirectorRepository
from cocoman_recommender.schemas.genre import GenreRepository
from cocoman_recommender.schemas.keyword import KeywordRepository
from cocoman_recommender.services.contents_service import ContentsService
from cocoman_recommender.services.crawler.justwatch import JustWatchCrawler
from cocoman_recommender.services.recommender_service import GenreRecommenderService


class Container(containers.DeclarativeContainer):
    c = conf()
    conf_dict = asdict(c)

    db = providers.Singleton(Database, db_url=conf_dict['DB_URL'])

    """ Repository """
    ott_repository = providers.Factory(OttRepository, session_factory=db.provided.session)
    contents_repository = providers.Factory(ContentsRepository, session_factory=db.provided.session)
    actor_repository = providers.Factory(ActorRepository, session_factory=db.provided.session)
    director_repository = providers.Factory(DirectorRepository, session_factory=db.provided.session)
    genre_repository = providers.Factory(GenreRepository, session_factory=db.provided.session)
    keyword_repository = providers.Factory(KeywordRepository, session_factory=db.provided.session)

    """ Service """
    contents_service = providers.Factory(ContentsService, contents_repository=contents_repository,
                                         ott_repository=ott_repository,
                                         actor_repository=actor_repository,
                                         director_repository=director_repository,
                                         genre_repository=genre_repository,
                                         keyword_repository=keyword_repository)
    justwatcher_crawler = providers.Factory(JustWatchCrawler, ott_repository=ott_repository,
                                            contents_repository=contents_repository, actor_repository=actor_repository,
                                            director_repository=director_repository, genre_repository=genre_repository)
    genre_recommender = providers.Factory(GenreRecommenderService, contents_repository=contents_repository)
