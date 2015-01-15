
from fiole import get, run_fiole, default_app


@get('/')
def index(request):
	return 'Hello World!'

def run_bjoern(host, port, handler, workers=2):
	NUM_WORKERS = workers
	worker_pids = []

	# Bind to TCP host/port pair:
	import os
	import bjoern
	bjoern.listen(handler, host, port)
	# bjoern.run()

	for _ in xrange(NUM_WORKERS):
		pid = os.fork()
		if pid > 0:
			worker_pids.append(pid)
		elif pid == 0:
			try:
				bjoern.run()
			except KeyboardInterrupt:
				pass
			exit()
	try:
		for _ in xrange(NUM_WORKERS):
			os.wait()
	except KeyboardInterrupt:
		for pid in worker_pids:
			os.kill(pid, signal.SIGINT)

def run_gevent(host, port, handler):
	from gevent import monkey; monkey.patch_all()
	from gevent import pywsgi
	server = pywsgi.WSGIServer((host, port), handler, backlog=128000)
	server.serve_forever()

# run_fiole(port=8080, server=run_gevent)

# run_fiole(port=8080, server=run_bjoern)


from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

print dir(default_app)
app = SessionMiddleware(default_app, session_opts)
app.routes = default_app.routes

run_fiole(app=default_app,port=8080, server=run_bjoern)
