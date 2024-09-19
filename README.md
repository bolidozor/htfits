# htfits - http FITS file viewer

## Installation 

### Apache

### gunicorn
    gunicorn -w 3 htfits:application --bind 127.0.0.1:7100

### Stand-alone Python server 

    git clone git@github.com:bolidozor/htfits.git
    sudo pip install static
    cd htfits
    python htfits.py

Now we should point a web browser on address
http://localhost:8000/#http://space.astro.cz/bolidozor/OBSUPICE/OBSUPICE-R3/snapshots/2015/01/04/04/20150104041403368_OBSUPICE-R3_snap.fits

The generated image contains one Bolidozor detected meteor from Czech Astronomical Society data center at: http://space.astro.cz/bolidozor/
