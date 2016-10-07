import flask_testing
import time

from iis import create_app, db
from iis.util.daemons import daemonize
import iis.models


class TestDaemonize(flask_testing.TestCase):
    DAEMON_PID_PATH = "/tmp"

    def create_app(self):
        return create_app(self)

    def test_no_exception_raised_and_returns_pid(self):
        self.app.logger.debug("Testing daemonize")

        def test_worker(uuid):
            self.app.logger.debug("Executing test process")
            comp = iis.models.Computation(process_uid=uuid, input_data="",
                                          output_data="", status="finished",
                                          progress=100)
            db.session.add(comp)
            db.session.commit()

        uid = daemonize(test_worker,
                        pid_base=TestDaemonize.DAEMON_PID_PATH)  # type: str
        self.assertTrue(isinstance(uid, str))
        time.sleep(5)

        comp = iis.models.Computation.query.filter_by(process_uid=uid).first()
        self.assertEqual(comp.status, "finished")
        self.app.logger.debug("Testing daemonize successful")
