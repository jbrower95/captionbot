import twitter
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random
import string
import os
import sys
import requests
import textwrap


raise Exception("Please enter your twitter account information.")
# TODO: Fill in twitter account information (removed this for the handin.)
api = twitter.Api(consumer_key=None,
                      consumer_secret=None,
                      access_token_key=None,
                      access_token_secret=None)

raise Exception("Please give your source of captions.")
comments = None
with open("comments-clean.txt", "r") as f:
	comments = f.read().split("\n")
comments = [x.strip() for x in comments]

raise Exception("Please direct the bot to a directory containing .ttf files for fonts.")
fonts = os.listdir("fonts")

def postPhoto(text, photoPath):
	return api.PostMedia(text, photoPath)

def addCaptionToPhoto(filename, caption, font):
	size = random.randint(25, 40)
	font = ImageFont.truetype(font, size)
	img = Image.open(filename)
	draw = ImageDraw.Draw(img)
	
	color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
	margin = offset = 40
	for line in textwrap.wrap(caption, width=30):
	    draw.text((margin, offset), line, color, font=font)
	    offset += font.getsize(line)[1]
	draw = ImageDraw.Draw(img)

	img.save(filename)
	return img

def randomString():
	char_set = string.ascii_uppercase + string.digits
	return ''.join(random.sample(char_set*6, 6))

def getRandomImage():
	raise Exception("If you want to change your image source, modify this function.")
	print "[+] Downloading random image..."
	baseURL = "https://source.unsplash.com/random"
	dimens = "800x600"
	url = baseURL + "/" + dimens
	r = requests.get(url)
	imageName = "image-" + randomString() + ".png"
	with open(imageName, "w+") as image:
		image.write(r.content)
	print "[-] Done."
	return imageName

def movePhotoToQueue(imagePath):
	os.rename(imagePath, "queue/" + imagePath)

def getRandomCaption():
	return random.choice(comments)

def getRandomFont():
	return "fonts/" + random.choice(fonts)

def tweet(preview):
	caption = getRandomCaption()
	imagePath = getRandomImage()
	font = getRandomFont()

	img = addCaptionToPhoto(imagePath, caption, font)
	if preview: img.show()
	print "Caption: " + caption
	confirm = raw_input("Post? (y/q/N/): ")
	if confirm == "y":
		postPhoto("", imagePath)
		if raw_input("Delete file? (y/N): ") == "y": os.remove(imagePath)
	elif confirm == "q":
		movePhotoToQueue(imagePath)
		print "Queued photo."
		print "Number Photos Queued: " + str(len(filter(lambda x: "png" in x, os.listdir("queue"))))
	else:
		print "Aborted."

def pullFromQueue():
	queuedStuff = filter(lambda x: "png" in x, os.listdir("queue"))
	if queuedStuff:
		photo = random.choice(queuedStuff)
		photoPath = "queue/" + photo
		print "Uploading: " + photoPath
		postPhoto("", photoPath)
		print "Removing photo from queue: " + photoPath
		os.rename("queue/" + photo, photo)
	else:
		print "Nothing in queue."

def main():
	suppressImage = "-s" not in sys.argv
	if "-queue" in sys.argv or "-q" in sys.argv:
		pullFromQueue()
	elif "-i" in sys.argv or "-interactive" in sys.argv:
		# interactive mode.
		while True: tweet(suppressImage)
	else:
		print "usage: python main.py [-q | -i]"
		print "-i: Interactive mode. Use to queue or post things now."
		print "-q: Queue mode. Posts a photo from the queue if there is one available."

if __name__ == "__main__":
	main()
