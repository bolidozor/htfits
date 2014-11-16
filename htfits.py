import matplotlib
import matplotlib.image
import StringIO
import pyfits
import numpy as np
import urllib2
import static # https://github.com/lukearno/static

try:
    import urllib2.parse as urlparse
except ImportError:
    import urlparse

ALLOWED_SCHEMES = ['http']
ALLOWED_NETLOCS = ['space.astro.cz']

def fits_to_png(environ, start_response):
    url = environ['QUERY_STRING']

    urlp = urlparse.urlparse(url)
    if not (urlp.netloc in ALLOWED_NETLOCS and urlp.scheme in ALLOWED_SCHEMES):
        start_response('403 Forbidden', [('Content-type', 'text/plain')])
        return "FITS URL is bad"

    try:
        fits = pyfits.open(StringIO.StringIO(urllib2.urlopen(url).read()))
        sio = StringIO.StringIO()

        imunit = None

        for unit in fits:
            if unit.data is not None:
                imunit = unit

        matplotlib.image.imsave(sio, imunit.data[::-1,:], format='png')
    except Exception:
        start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
        return "Error"

    start_response('200 OK', [('Content-type', 'image/png')])
    return sio.getvalue()

static = static.Cling('.')

def app(environ, start_response):
    if environ['PATH_INFO'] == '/fits.png':
        return fits_to_png(environ, start_response)

    return static(environ, start_response)

def main():
    from wsgiref.util import setup_testing_defaults
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8000, app)
    print "Serving on port 8000..."
    httpd.serve_forever()

if __name__ == "__main__":
    main()
