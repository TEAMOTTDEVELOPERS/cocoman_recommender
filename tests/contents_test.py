import unittest
from unittest import TestCase

from sqlalchemy.exc import NoResultFound

from cocoman_recommender.containers import Container
from cocoman_recommender.schemas.contents import Contents


class ContentsTest(TestCase):
    container = Container()

    def setUp(self) -> None:
        self.container.db().create_database()

    def tearDown(self) -> None:
        with self.container.db().session() as session:
            session.query(Contents).delete()
            session.commit()

    def test_read_contents(self):
        contents = Contents(
            title='example',
            year='2021',
            country='example',
            running_time='100',
            grade_rate='all',
            broadcaster='example',
            open_date='20210101',
            broadcast_date='20210101',
            story='example',
            ott_id=[],
            actors_id=[],
            directors_id=[],
            genres_id=[],
            keywords_id=[]
        )
        content = self.container.contents_repository().create(contents)
        result = self.container.contents_repository().get_by_id(content.id)
        self.assertEqual(result.title, 'example')

    def test_update_contents(self):
        contents = Contents(
            title='example',
            year='2021',
            country='example',
            running_time='100',
            grade_rate='all',
            broadcaster='example',
            open_date='20210101',
            broadcast_date='20210101',
            story='example',
            ott_id=[],
            actors_id=[],
            directors_id=[],
            genres_id=[],
            keywords_id=[]
        )
        content = self.container.contents_repository().create(contents)
        contents.title = 'example1'

        content = self.container.contents_repository().update(content.id, contents)
        self.assertEqual(content.title, 'example1')

    def test_delete_contents(self):
        contents = Contents(
            title='example',
            year='2021',
            country='example',
            running_time='100',
            grade_rate='all',
            broadcaster='example',
            open_date='20210101',
            broadcast_date='20210101',
            story='example',
            ott_id=[],
            actors_id=[],
            directors_id=[],
            genres_id=[],
            keywords_id=[]
        )
        content = self.container.contents_repository().create(contents)

        self.container.contents_repository().delete_by_id(content.id)
        self.assertRaises(NoResultFound, lambda: self.container.contents_repository().get_by_id(content.id))


if __name__ == "__main__":
    unittest.main()
