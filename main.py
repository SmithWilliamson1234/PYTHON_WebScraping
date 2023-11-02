from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin

app = Flask(__name__)

app.config['STATIC_FOLDER'] = 'static'
def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            link_data = []
            base_url = urlparse(url).scheme + '://' + urlparse(url).netloc

            for link in links:
                href = link.get('href')
                absolute_url = urljoin(base_url, href)
                link_data.append({'text': link.get_text(), 'href': absolute_url})

            return link_data
        else:
            return None
    except Exception as e:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    link_data = []
    if request.method == 'POST':
        url = request.form['url']
        result = scrape_website(url)
        if result:
            link_data = result

    return render_template('index.html', link_data=link_data)

if __name__ == '__main__':
    app.run(debug=True)
