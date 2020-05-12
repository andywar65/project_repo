from django.test import TestCase

from .models import DownloadableFile

class StreamblocksModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        DownloadableFile.objects.create(id=13,
            fb_file='documents/document.pdf', description='Foo Bar')
        DownloadableFile.objects.create(id=14,
            fb_file='documents/document.pdf')

    def test_download_file_get_description(self):
        download = DownloadableFile.objects.get(id=13)
        self.assertEquals(download.get_description(), 'Foo Bar')

    def test_download_file_get_no_description(self):
        download = DownloadableFile.objects.get(id=14)
        self.assertEquals(download.get_description(), 'document.pdf')
