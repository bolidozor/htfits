import matplotlib
import matplotlib.image

import io
from io import StringIO

from astropy.io import fits
import astropy.io.fits as pyfits
import numpy as np
from urllib.request import urlopen, urlparse
import matplotlib
import matplotlib.image
import io
import urllib.request as urllib2
from urllib.parse import urlparse
from astropy.io import fits
import numpy as np


ALLOWED_SCHEMES = ['http']
ALLOWED_NETLOCS = ['space.astro.cz']

def fits_to_png(environ, start_response):
    url = environ['QUERY_STRING']
    print(url)
    urlp = urlparse(url)
    if not (urlp.netloc in ALLOWED_NETLOCS and urlp.scheme in ALLOWED_SCHEMES):
        start_response('403 Forbidden', [('Content-type', 'text/plain')])
        return "FITS URL is bad"

    try:

        fits_file = fits.open(io.BytesIO(urllib2.urlopen(url).read()))
        sio = io.BytesIO()

        imunit = None

        for unit in fits_file:
            if unit.data is not None:
                imunit = unit

        print("GEN")
        

        matplotlib.image.imsave(sio, imunit.data[::-1,:], format='png', cmap='gnuplot')
        sio.seek(0)

    except Exception:
        start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
        return "Error"

    start_response('200 OK', [('Content-type', 'image/png')])
    return [sio.getvalue()]

def main():
    from wsgiref.util import setup_testing_defaults
    from wsgiref.simple_server import make_server
    import static # https://github.com/lukearno/static

    static = static.Cling('.')

    def app(environ, start_response):
        if environ['PATH_INFO'] == '/f.png':
            return fits_to_png(environ, start_response)

        return static(environ, start_response)
    port = 80
    httpd = make_server('', port, app)
    print("Serving on port {}...".format(port))
    httpd.serve_forever()
    print("End...")

if __name__ == "__main__":
    main()

application = fits_to_png

