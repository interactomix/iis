import multiprocessing as mp
import typing
import uuid
import base64
import os

import daemonize as d

from iis import app


def daemonize(task: typing.Callable[..., None], pid_base: str) -> str:
    """Fork a new process, daemonize it and return the process uuid.

    Do the double fork magic required to correctly daemonize a
    process.  The daemon runs the task passed to daemonize.

    The process uuid is an internally unique identifier to uniqely identify the
    process/computation.
    """
    process_uuid = base64.b32encode(uuid.uuid4().bytes).decode('ascii')
    pid = os.path.join(pid_base,
                       "flask_iis_worker_process" +
                       process_uuid +
                       ".pid")

    def task_wrapper():
        task(process_uuid)

    def daemon_spawner():
        app.logger.info("Daemonizing worker process with UUID: "
                        + process_uuid)
        daemon = d.Daemonize(
            app="iis_flask_worker-"+process_uuid, pid=pid,
            action=task_wrapper
        )
        daemon.start()

    mp.Process(target=daemon_spawner).start()
    return process_uuid
