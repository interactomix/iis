from flask import url_for

from .base import BaseTestCase


class TestJobCreateView(BaseTestCase):
    def test_login_required(self):
        self.assertLoginRequired(url_for('jobs.create'))
