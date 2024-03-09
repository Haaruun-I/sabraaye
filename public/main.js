console.log('test')
const player = new Shikwasa.Player({
    container: document.querySelector('footer'),
    download: true,
    autoplay: true,
    theme: "sepia",
    themeColor: "#6F8F66",
    fixed: {type:'fixed', position:'bottom'},
    audio: {src:'/audio/tafsiir-cusub/4aad | Buruuj - Takwiir.mp3'}
})
console.log('test2')

document.addEventListener('alpine:init', () => Alpine.data('model', () => ({
    test: "test",
    showList: [],
    changePlaying(episode) {
        console.table(episode)
        player.update(episode)   
    },
    init() {
        getPodcastFromURL("/feeds/tafsiir-cusub.xml", feed => {
            this.showList = [feed]
        })
        console.log('teest3')
    }
})))

Alpine.start()