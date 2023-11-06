import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_h = logging.FileHandler("/home/farhad/project/tabdeel_drf/log/log.log")
file_f = logging.Formatter(
    "%(asctime)s-%(message)s-%(process)d-%(processName)s-%(thread)d-%(threadName)s"
)
file_h.setFormatter(file_f)
file_h.setLevel(logging.INFO)

stream_view_h = logging.FileHandler("/home/farhad/project/tabdeel_drf/log/view-log.log")
stream_view_f = logging.Formatter("%(asctime)s-%(message)s")
stream_view_h.setFormatter(stream_view_h)
stream_view_h.setLevel(logging.ERROR)

logger.addHandler(file_h)
logger.addHandler(stream_view_h)
