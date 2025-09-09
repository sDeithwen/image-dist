from flask import Flask, Response, request
import requests
import hashlib
import redis
import html
import unittest

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)
salt = "UNIQUE_SALT"
default_name = 'Joe Bloggs'

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    name = default_name
    if request.method == 'POST':
        name = html.escape(request.form['name'], quote=True)
    salted_name = salt + name
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()
    header = '<html><head><title>Identidock</title></head><body>'
    body = '''<form method="POST">
    Hello <input type="text" name="name" value="{0}">
    <input type="submit" value="submit"> </form>
    <p>You look like a:
    <img src="/monster/{1}"/> '''.format(name, name_hash)
    footer = '</body></html>'
    return header + body + footer

@app.route('/monster/<name>')
def get_identicon(name):
    name = html.escape(name, quote=True)
    image = cache.get(name)
    if image is None:
        print("Cache miss (Промах кэша)", flush=True)
        r = requests.get('http://dnmonster:8000/monster/' + name + '?size=80')
        image = r.content
        cache.set(name, image)
    return Response(image, mimetype='image/png')

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_get_mainpage(self):
        page = self.app.post("/", data=dict(name="Moby Dick"))
        assert page.status_code == 200
        assert 'Hello' in str(page.data)
        assert 'Moby Dick' in str(page.data)

    def test_html_escaping(self):
        page = self.app.post("/", data=dict(name='"><b>TEST</b><!--'))
        assert '<b>' not in str(page.data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    unittest.main()