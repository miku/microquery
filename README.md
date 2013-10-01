README
======

Copy a live solr first.

    $ cd && mkdir -p tmp & cd tmp
    $ scp -r me@server:/usr/local/vufind/solr .

Start solr (using a [custom solr startup script](https://gist.github.com/miku/6775310) here):

    $ solr `pwd`/solr
    2013-10-01 16:19:13.259:INFO::Logging to STDERR via org.mortbay.log.StdErrLog
    2013-10-01 16:19:13.331:INFO::jetty-6.1-SNAPSHOT
    Oct 01, 2013 4:19:13 PM org.apache.solr.core.SolrResourceLoader locateSolrHome
    ...

----

Get the mini server app:

    $ cd ~/tmp
    $ git clone git@github.com:miku/microquery.git .
    $ cd microquery

Assuming [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) is installed.

    $ mkvirtualenv microquery
    $ pip install -r requirements.txt

Change `BASE_URL = 'http://insert.here'` in `app.py` to some catalog URL first, then
start the server:

    $ python app.py
    * Running on http://0.0.0.0:5000/
    * Restarting with reloader
    ...

Go to http://localhost:5000, this interface goes directly to SOLR and
gets only the availability from vufind, using the AJAX handler.

Append `debug=1` to see a JSON-ish output.

Screenshots
-----------

http://imgur.com/a/FdE3K
