from flask import url_for

from test_utils.base import BaseTestCase
from iis.jobs.models import PipelineDefinition
from iis.extensions import db


class TestJobUploadView(BaseTestCase):
    def test_login_required(self):
        self.assertLoginRequired(url_for("jobs.upload"))

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


class TestJobsSearchView(BaseTestCase):

    def test_empty_search_finds_all(self):
        for i in range(1, 10):
            d = PipelineDefinition()
            d.name = "TestPDF" + str(i)
            d.public = True
            d.definition = '{"test_key": "test content"}'
            d.description = ""
            db.session.add(d)

        db.session.commit()
        r = self.client.get(url_for("jobs.search"))
        self.assertEqual(9, str(r.get_data()).count("TestPDF"))

    def test_search_finds_all_matching(self):
        for i in range(1, 10):
            d = PipelineDefinition()
            d.name = "TestPDF" + str(i)
            d.public = True
            d.definition = '{"test_key": "test content"}'
            d.description = ""
            db.session.add(d)

        for i in range(1, 10):
            d = PipelineDefinition()
            d.name = "TestPDFMatch" + str(i)
            d.public = True
            d.definition = '{"test_key": "test content"}'
            d.description = ""
            db.session.add(d)

        db.session.commit()

        r = self.client.get(url_for("jobs.search"), query_string=dict(
            search_term="TestPDFMatch"
        ))
        self.assertEqual(10, str(r.get_data()).count("TestPDF"))


class TestJobsDetailView(BaseTestCase):
    def test_appears_disabled_for_wrong_user(self):
        user = self.login()

        d = PipelineDefinition()
        d.name = "TestPDF"
        d.public = True
        d.definition = '{"test_key": "test content"}'
        d.description = ""
        d.user = user
        db.session.add(d)
        db.session.commit()

        self.logout()

        r = self.client.get(url_for("jobs.detail", job_id=d.id))
        self.assertEqual(4, str(r.get_data()).count("disabled"))

    def test_rejects_post_for_wrong_user(self):
        user = self.login()

        d = PipelineDefinition()
        d.name = "TestPDF"
        d.public = True
        d.definition = '{"test_key": "test content"}'
        d.description = ""
        d.user = user
        db.session.add(d)
        db.session.commit()

        self.logout()

        self.client.post(url_for("jobs.detail", job_id=d.id), data=dict(
            name="Test",
            public=True,
            definition='{"test_key": "test content"}',
            description=""
        ))
        self.assertEqual("TestPDF", PipelineDefinition.query.get(d.id).name)

    def test_allows_edit_for_correct_user(self):
        user = self.login()

        d = PipelineDefinition()
        d.name = "TestPDF"
        d.public = True
        d.definition = '{"test_key": "test content"}'
        d.description = ""
        d.user = user
        db.session.add(d)
        db.session.commit()

        self.client.post(url_for("jobs.detail", job_id=d.id), data=dict(
            name="Test",
            public=True,
            definition='{"test_key": "test content"}',
            description=""
        ))
        self.assertEqual("Test", PipelineDefinition.query.get(d.id).name)
