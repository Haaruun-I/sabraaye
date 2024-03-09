const xmlParse = new DOMParser().parseFromString.bind(new DOMParser());

const getPodcastFromURL = (feedURL, callback) => {
  fetch(feedURL)
  .then(res => {res.text().then(res => {
        let parsedFeed = {}
        feed = xmlParse(res, 'text/xml')

        parsedFeed.title = feed.querySelector('title').textContent
        parsedFeed.episodeList = []
        feed.querySelectorAll('item').forEach(episode => {
          parsedFeed.episodeList.push({
            title: episode.querySelector('title').textContent,
            src: episode.querySelector('link').textContent,
            artist: parsedFeed.title
          })
        
        })
        parsedFeed.episodeList = parsedFeed.episodeList.sort((a,b) => a.title.localeCompare(b.title))
        
        callback(parsedFeed)    
    })
  })
}