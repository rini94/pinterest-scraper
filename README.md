# Pinterest-Scraper

Scrape images from a board and save it to a folder.

- Run the script. Images limit can be given as argument (optional).
- Enter the board url.
- The images are downloaded and saved to a folder with the name of the board (A max images limit of 10000 given as default).
- Uses Selenium and chrome driver.
- Uses Python3.

## Examples:
#### 1.
````
 python pinterest-scraper.py
 ````
Output:

````
Enter the url of the chapter or the page:
https://www.pinterest.com/flickr/straight-from-flickr/
````
This will download all the images from the board.

#### 2.
````
 python pinterest-scraper.py 4
 ````
Output:

````
Enter the url of the chapter or the page:
https://www.pinterest.com/flickr/straight-from-flickr/
````
This will download 4 images from the board.

*Board url used here is just for example.
