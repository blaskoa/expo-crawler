# About
Web image scraper created using [scrapy](https://scrapy.org/).
Follows all link from homesite (on the same domain), downloads all images from `img` elements and downloads images from available stylesheets recursively.

The scraper only download URLs ending with `.png` `.jpg` `.gif` or `.jpeg`.

Stylesheet recursion also only works when the stylesheet URL ends with `.css` (so if there are URL query params present, the recursion won't work).

# Install and run
The dependencies are handled using [pipenv](https://github.com/pypa/pipenv]).
To run the crawler, do the following:
1. Install [pipenv](https://github.com/pypa/pipenv])
2. Run `pipenv install`
3. Activate pipenv virtual environment using `pipenv shell`
4. Run `scrapy crawl images -o items.json`

Folder `images` will be created, where scrappy will download images from the website.

The `-o items.json` option will serialize all found items into `items.json` file.
