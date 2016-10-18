from test_utils.base import BaseTestCase
from iis.jobs.forms import JobForm
from iis.extensions import db
from iis.jobs.models import PipelineDefinition


class TestJobForm(BaseTestCase):
    def test_empty_form_is_invalid(self):
        self.assertFalse(JobForm().validate())

    def test_using_existing_name_is_not_allowed(self):
        user = self.login()

        definition = PipelineDefinition()
        definition.user_id = user.get_id()
        definition.name = "TestPDF"
        definition.description = ""
        definition.public = False
        definition.definition = '{"key": "value"}'

        db.session.add(definition)
        db.session.commit()

        form = JobForm(obj=definition)
        self.assertFalse(form.validate())

    def test_using_existing_name_with_id_is_ok(self):
        user = self.login()

        definition = PipelineDefinition()
        definition.user_id = user.get_id()
        definition.name = "TestPDF"
        definition.description = ""
        definition.public = False
        definition.definition = '{"key": "value"}'

        db.session.add(definition)
        db.session.commit()

        form = JobForm(obj=definition, id=definition.id)
        self.assertTrue(form.validate())

    def test_valid_otherwise(self):
        user = self.login()
        form = JobForm(data=dict(
            user_id=user.get_id(),
            name="TestPDF",
            description="",
            public=False,
            definition='{"key": "value"}'
        ))

        form.validate()
        self.assertTrue(form.validate())
