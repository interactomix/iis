from .base import BaseTestCase
from iis.jobs.forms import CreateForm
from iis.extensions import db
from iis.jobs.models import PipelineDefinition


class TestCreateForm(BaseTestCase):
    def test_empty_form_is_invalid(self):
        self.assertFalse(CreateForm().validate())

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

        form = CreateForm(obj=definition)
        self.assertFalse(form.validate())

    def test_valid_otherwise(self):
        user = self.login()
        form = CreateForm(data=dict(
            user_id=user.get_id(),
            name="TestPDF",
            description="",
            public=False,
            definition='{"key": "value"}'
        ))

        form.validate()
        self.assertTrue(form.validate())
