from beaker.middleware import SessionMiddleware


def simple_app(environ, start_response):
    # Get the session object from the environ
    session = environ['beaker.session']

    # Check to see if a value is in the session
    user = 'logged_in' in session

    # Set some other session variable
    session['user_id'] = 10

    start_response('200 OK', [('Content-type', 'text/plain')])
    return ['User is logged in: %s' % user]



# Configure the SessionMiddleware
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,
}

import falcon



class Resource(object):

    def on_get(self, req, resp):
        # resp.body = '{"message": "Hello world!"}'
        session = req.env['beaker.session']
        print session
        resp.content_type = 'text/plain'
        resp.body = 'Hello world!'
        resp.status = falcon.HTTP_200


api = application = falcon.API()

api.add_route('/',Resource())


wsgi_app = SessionMiddleware(api, session_opts)

import bjoern
bjoern.listen(wsgi_app, host="127.0.0.1", port=8080)
bjoern.run()