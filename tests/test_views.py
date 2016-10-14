from flask import url_for

from .base import BaseTestCase
from iis.jobs.models import PipelineDefinition


class TestJobUploadView(BaseTestCase):
    def test_login_required(self):
        self.assertLoginRequired(url_for("jobs.create"))

    def test_post_from_valid(self):
        self.login()
        response = self.client.post(url_for("jobs.upload"), data=dict(
            name="TestPDF",
            public=False,
            definition='{"test_content": "This is a test pdf"}',
            description=""
        ))
        self.assertNotIn(b"has-error", response.get_data())

    def test_unique_name_required(self):
        self.login()
        data = dict(
            name="TestPDF",
            public=False,
            definition='{"test_content": "This is a test pdf"}',
            description=""
        )
        self.client.post(url_for("jobs.upload"), data=data)
        response = self.client.post(url_for("jobs.upload"), data=data)
        self.assertIn(b"has-error", response.get_data())
        self.assertEqual(
            1, len(PipelineDefinition.query.filter_by(name="TestPDF").all())
        )

    def test_created_definition_is_in_db(self):
        self.login()
        self.client.post(url_for("jobs.upload"), data=dict(
            name="TestPDF",
            public=False,
            definition='{"test_content": "This is a test pdf"}',
            description=""
        ))
        self.assertTrue(
            PipelineDefinition.query.filter_by(name="TestPDF").one())
