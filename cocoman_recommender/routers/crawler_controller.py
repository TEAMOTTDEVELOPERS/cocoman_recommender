from fastapi import Depends, APIRouter
from fastapi_utils.cbv import cbv
from dependency_injector.wiring import inject, Provide

from cocoman_recommender.containers import Container
from cocoman_recommender.services.crawler.justwatch import JustWatchCrawler

router = APIRouter()


@cbv(router)
class CrawlerController:
    @inject
    def __init__(self, crawler_service: JustWatchCrawler = Depends(Provide[Container.justwatcher_crawler])):
        self.crawler_service = crawler_service

    @router.post('/{target}/{lang}')
    async def crawling(self, target: str, lang: str):
        return self.crawler_service.crawling_justwatch(target, lang)
