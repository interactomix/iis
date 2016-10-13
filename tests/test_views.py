from flask import url_for
from flask_login import current_user

from .base import BaseTestCase
from iis.jobs.models import PipelineDefinition


class TestJobUploadView(BaseTestCase):
    def test_login_required(self):
        self.assertLoginRequired(url_for("jobs.create"))

    def test_created_definition_is_in_db(self):
        self.login()
        # print(current_user.username)
        self.client.post(url_for("jobs.upload"), data=dict(
            name="TestPDF",
            public=False,
            definition='{"test_content": "This is a test pdf"}',
            description=""
        ))
        self.assertTrue(
            PipelineDefinition.query.filter_by(name="TestPDF").one()
        )
