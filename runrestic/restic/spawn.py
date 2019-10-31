import logging
import subprocess
from typing import List, Tuple

logger = logging.getLogger(__name__)


def run_multiple_commands(
    commands: List[List], parallel=False
) -> List[Tuple[int, str]]:
    processes = []
    for cmd in commands:
        logger.debug(f"Running {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if not parallel:
            p.wait()
        processes.append(p)

    if parallel:
        [process.wait() for process in processes]

    return [(p.returncode, p.stdout.read().decode("UTF-8")) for p in processes]


# import logging
# import subprocess
# import time
#
# logger = logging.getLogger(__name__)
#
#
# def execute_hook(config: dict, name: str):
#     time_start = time.time()
#
#     commands = config.get("backup").get(name, [])
#
#     rcs = []
#
#     for cmd in commands:
#         logger.info(" - executing hook: {cmd}".format(cmd=cmd))
#
#         try:
#             output = subprocess.check_output(
#                 cmd, stderr=subprocess.STDOUT, universal_newlines=True, shell=True
#             )
#             process_rc = 0
#         except subprocess.CalledProcessError as e:
#             output = e.output
#             process_rc = e.returncode
#
#         logger.debug(output)
#
#         logger.info("   " + ("✓" if process_rc == 0 else "✕"))
#
#         if config["exit_on_error"] and process_rc != 0:
#             return process_rc
#
#         rcs += [process_rc]
#
#     logs = {"duration_seconds": time.time() - time_start, "rc": 1 if any(rcs) else 0}
#     return logs
