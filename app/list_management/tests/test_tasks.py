from unittest.mock import patch
from django.test import TestCase
from list_management.tasks import (
    scrape_imdb_top_250,
    scrape_filmweb_top_250,
    scrape_oscar_best_picture,
)


class CeleryTaskTest(TestCase):
    @patch("list_management.tasks.IMDBTop250Scraper.scrape")
    def test_scrape_imdb_top_250(self, mock_scrape):
        # Invoke the task
        scrape_imdb_top_250()
        # Make sure the scrape method has been called
        self.assertTrue(mock_scrape.called)

    @patch("list_management.tasks.FilmwebTop250Scraper.scrape")
    def test_scrape_filmweb_top_250(self, mock_scrape):
        scrape_filmweb_top_250()
        self.assertTrue(mock_scrape.called)

    @patch("list_management.tasks.OscarBestPictureScraper.scrape")
    def test_scrape_oscar_best_picture(self, mock_scrape):
        scrape_oscar_best_picture()
        self.assertTrue(mock_scrape.called)
