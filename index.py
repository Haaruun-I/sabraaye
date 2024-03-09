from pprint import pprint

from yaml import load, Loader
from pathlib import Path
import shutil, os

from feedgen.feed import FeedGenerator
from urllib.parse import urlencode, quote
   
def makeUrl(base_url, *uris, **params):
    url = base_url.rstrip('/')
    for uri in uris:
        _uri = quote(uri).strip('/')
        url = '{}/{}'.format(url, _uri) if _uri else url
    if params:
        url = '{}?{}'.format(url, urlencode(params))
    return url


def makeSeries(seriesDir, globalConfig):
    with open(seriesDir/'index.yaml', 'r') as f:
        config = load(f.read(), Loader)

    config['url'] = makeUrl(globalConfig['deployURL'], 'audio', config['shortName'])
    feed = FeedGenerator()
    feed.load_extension('podcast')
    feed.id(config['url'])
    feed.title(config['title'])
    feed.link(href=config['url'])
    feed.description(config['description'])

    episodePaths = (seriesDir/'audio').iterdir()
    for episodePath in episodePaths:
        episodeURL = makeUrl(config['url'], episodePath.name)
        
        episode = feed.add_entry()
        episode.id(episodeURL)
        episode.title(episodePath.stem)
        episode.link(href=episodeURL)
        episode.enclosure(episodeURL, 0, 'audio/mpeg')

    feed.rss_file(globalConfig['buildFolder']/'feeds'/(config['shortName'] + '.xml'))
    shutil.copytree(seriesDir/'audio', globalConfig['buildFolder']/'audio'/config['shortName'])    
    
    return feed


def main(config):
    shutil.rmtree(config['buildFolder'], ignore_errors=True)
    shutil.copytree(config['publicFolder'], config['buildFolder'])
    os.mkdir(config['buildFolder']/'feeds')

    # Get all subfolders with 'index.yaml' file
    subFolders = [ path for path in config['contentFolder'].iterdir() 
                    if (path/'index.yaml').exists() ] 

    for seriesDir in subFolders:
        feed = makeSeries(seriesDir, config)
    

main({
    'contentFolder': Path('content/'),
    'publicFolder': Path('public/'),
    'buildFolder': Path('build/'),
    'deployURL': 'http://localhost:8004'
})
