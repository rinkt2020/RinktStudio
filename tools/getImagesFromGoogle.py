from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
from urllib.request import *
import sys
import time
import io
from PIL import Image
from mimetypes import guess_extension
from urllib.request import urlretrieve
import ntpath

# adding path to geckodriver to the OS environment variable
os.environ["PATH"] += os.pathsep + os.getcwd()
download_path = "dataset/"

def main():
	searchtext = sys.argv[1]
	num_requested = int(sys.argv[2])
	number_of_scrolls = 20000 / 400 + 1 
	# number_of_scrolls * 400 images will be opened in the browser

	if not os.path.exists(download_path + searchtext.replace(" ", "_")):
		os.makedirs(download_path + searchtext.replace(" ", "_"))

	url = "https://www.google.co.in/search?q="+searchtext+"&source=lnms&tbm=isch"
	driver = webdriver.Firefox()
	driver.get(url)

	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
	extensions = {"jpg", "jpeg", "png", "gif"}
	img_count = 0
	downloaded_img_count = 0
	
	for _ in range(int(number_of_scrolls)):
		for __ in range(10):
			# multiple scrolls needed to show all 400 images
			driver.execute_script("window.scrollBy(0, 1000000)")
			time.sleep(0.2)
		# to load next 400 images
		time.sleep(0.5)
		try:
			driver.find_element_by_xpath("//input[@value='Show more results']").click()
		except Exception as e:
			print ("Less images found: {}".format(e))
			break

	# imges = driver.find_elements_by_xpath('//div[@class="rg_meta"]') # not working anymore
	imges = driver.find_elements_by_xpath('//img[contains(@class,"rg_i Q4LuWd")]')
	print ("Total images: {}\n".format(len(imges)))
	for img in imges:
		img_count += 1
		#print ("Downloading image {}:{}".format(img_count,img_url))
		try:
			image_src = img.get_attribute('src')
			filename, m = urlretrieve(image_src)
			#print ("file name: {}\n".format(filename))
			#
			img_type = guess_extension(m.get_content_type())
			head, tail = ntpath.split(filename)
			newname = tail or ntpath.basename(head)
			newname = newname + "." + img_type
			newPath = os.path.join("C:\\testImgs\\invoices", newname)
			os.rename(filename, newPath)
			print(newPath)
			# req = Request(image_src, headers=headers)
			# raw_img = urlopen(req).read()
			# f = open(download_path+searchtext.replace(" ", "_")+"/"+str(downloaded_img_count)+"."+img_type, "wb")
			# f.write(raw_img)
			# f.close
			
			# print ("Downloading image " + image_src)
			# image_src = image_src[image_src.find('/9'):]
			# print ("Downloading image " + image_src)
			# Image.open(io.BytesIO(base64.b64decode(image_src))).save(str(downloaded_img_count)+'.jpg')
			# downloaded_img_count += 1
		except Exception as e:
			print ("Download failed: {}".format(e))
		finally:
			print
		if downloaded_img_count >= num_requested:
			break

	print ("Total downloaded: {}/{}".format(downloaded_img_count,img_count))
	driver.quit()

if __name__ == "__main__":
	main()