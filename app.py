#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, render_template, redirect
import json
import pprint
import pysolr
import requests

BASE_URL = 'http://insert.here'

app = Flask(__name__)

def check_availability(finc_id):
    """
    In the frontend, this is done asynchronously.
    """
    template = "{base}/AJAX/JSON?method={method}&id%5B%5D={finc_id}"
    url = template.format(base=BASE_URL, method='getItemStatuses', 
                          finc_id=finc_id)
    response = json.loads(requests.get(url).text)
    return {
        'location': response.get('data')[0].get('location'),
        'callnumber': response.get('data')[0].get('callnumber'),
        'availability': response.get('data')[0].get('availability'),
    }

@app.route("/")
def hello():
    """ bye """
    return redirect('/query')

@app.route("/query")
def query():
    """
    Query a local solr (a copy of a live instance).
    Solr start helper script: https://gist.github.com/miku/6775310
    """
    s = pysolr.Solr('http://localhost:8983/solr/biblio')

    query = request.args.get('q', None)
    query = query or '*:*'
    sigel = request.args.get('sigel', 'DE-*')

    solrquery = '%s AND institution:%s' % (query, sigel)
    results = s.search(q=solrquery)

    items = []
    for result in results:
        finc_id = result.get('id')
        title = result.get('title_full')
        authors = [ar for ar in [result.get('author'), 
                                 result.get('author2')] if ar]
        year = result.get('publishDate')
        availability = check_availability(finc_id)

        items.append(dict(id=id, title=title, authors=authors, year=year, 
                          availability=availability))
    
    if request.args.get('debug', False):
        return """
            <input style='font-size: 20px' autofocus='autofocus' 
                   size=100 value='%s'></input>
            <pre>%s</pre>
            """ % (solrquery, pprint.pformat(items))
    else:
        return render_template('index.html', items=items, query=query)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
