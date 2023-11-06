import multiprocessing
from tabdeel_drf.settings import SECRET_KEY

bind = "127.0.0.1:8000"
backlog = 2048
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 5


spew = False


daemon = False
raw_env = ["DJANGO_SECRET_KEY=SECRET_KEY"]
pidfile = "/home/farhad/project/tabdeel_drf/log/pid-log.log"
umask = 0
user = None
group = None
tmp_upload_dir = "/home/farhad/project/tabdeel_drf/log/tmp-log.log"


errorlog = "/home/farhad/project/tabdeel_drf/log/error-log.log"
loglevel = "info"
accesslog = "/home/farhad/project/tabdeel_drf/log/access-log.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

proc_name = None


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):
    pass


def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spawning workers")


def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")
    import threading, sys, traceback

    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId, ""), threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")


def ssl_context(conf, default_ssl_context_factory):
    import ssl

    context = default_ssl_context_factory()

    context.minimum_version = ssl.TLSVersion.TLSv1_3

    def sni_callback(socket, server_hostname, context):
        if server_hostname == "foo.127.0.0.1.nip.io":
            new_context = default_ssl_context_factory()
            new_context.load_cert_chain(certfile="foo.pem", keyfile="foo-key.pem")
            socket.context = new_context

    context.sni_callback = sni_callback

    return context
