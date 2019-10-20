#Rini94
#Download images from Pinterest boards - Give the image limit as argument or else it downloads the entire board

import urllib.request
import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

pages = 1
max_pages = 1000 #max number of scrolls allowed in lazy loading
max_images = 10000 #max images limit - default
count = 0


def get_url ():
	board_url = input ("Enter the url of the board: \n")
	#board_url = "https://www.pinterest.com/flickr/straight-from-flickr/"
	if len(board_url) <= 1:
		print ("\nNo board url entered...\nExiting...\n")
		sys.exit()
	if not board_url.startswith ("http"):
		board_url = "https://" + board_url
	return board_url


def create_and_change_dir (dir_name):
	file_path = os.path.dirname(os.path.realpath(__file__))+ "/"+dir_name+"/"
	directory = os.path.dirname(file_path)
	if not os.path.exists(directory):
		os.makedirs(directory)
	os.chdir(file_path)


def download_image(image):
	try:
		srcset = image.get_attribute('srcset')
		image_url = srcset.split(', ')[1].split(' 2x')[0]
		name = image_url.split('/')
		image_name = name[len(name) - 1]

		print("Downloading image: ", image_name)
		if ".jpg" in image_url:
			urllib.request.urlretrieve(image_url, image_name)
			print("Downloaded image: ", image_name)
			return "success"

	except Exception as e:
		print("Exception", e)
		driver.implicitly_wait(1)


def end_loading (images_count):
	global max_images
	try:
		if images_count >= max_images:
			return True
		more_ideas_div = driver.find_element(By.CSS_SELECTOR, "[data-test-id='secondaryBoardGrid']");
		return True
	except NoSuchElementException:
		return False

#start

print ("--- Pinterest Board Downloader ---")
board_url = get_url ()

print ("\nLoading...\n")

if len(sys.argv) > 1:
	try:
		max_images = int(sys.argv[1])
	except:
		print ("Non number given... No image download limit set...")

print ("\nBoard URL: ", board_url)

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

chrome_options = Options()
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get(board_url)
wait = WebDriverWait(driver, 30)
board_header_ele = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-id='boardHeader'] h1")))
board_name = board_header_ele.text

print("Downloading images from the board: ", board_name)
create_and_change_dir(board_name)

container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-id='pinGrid']")))
items = container.find_elements_by_class_name("GrowthUnauthPinImage img")
images_count = len(items)

while pages < max_pages and not end_loading(images_count): #Scroll for lazy loading
	doc_height = driver.execute_script("return document.body.scrollHeight;")
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(3)
	scrolled_height = driver.execute_script("return document.body.scrollHeight")
	pages += 1
	items = container.find_elements_by_class_name("GrowthUnauthPinImage img")
	images_count = len(items)
	if doc_height == scrolled_height or end_loading(images_count):
		break
print ("Board ended. Total pages: ", pages)
print ("Starting download...")

items = container.find_elements_by_class_name("GrowthUnauthPinImage img")

for item in items:
	download = download_image(item)
	if download == "success":
		count = count + 1
		if count >= max_images:
			break

print ("Total images downloaded: ", count)
print ("Completed.")

sys.exit()
