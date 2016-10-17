import time

from iis.extensions import db
from .base import BaseTestCase
from iis.util.daemons import daemonize
import iis.models


class TestDaemonize(BaseTestCase):
    DAEMON_PID_PATH = "/tmp"

    def test_no_exception_raised_and_returns_pid(self):
        self.app.logger.debug("Testing daemonize")

        def test_worker(uuid):
            self.app.logger.debug("Executing test process")
            comp = iis.models.Computation(process_uid=uuid, input_data="",
                                          output_data="", status="finished",
                                          progress=100)
            db.session.add(comp)
            db.session.commit()
            self.app.logger.debug("Commited Computation model.")

        uid = daemonize(test_worker,
                        pid_base=TestDaemonize.DAEMON_PID_PATH)  # type: str
        self.assertTrue(isinstance(uid, str))
        time.sleep(5)

        self.app.logger.debug("Accessing Computation model.")
        comp = iis.models.Computation.query.filter_by(process_uid=uid).first()
        self.assertEqual(comp.status, "finished")
        self.app.logger.debug("Testing daemonize successful")
