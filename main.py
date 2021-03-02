import requests
import re
import optparse

class Snap_Story_Downloader:
	def __init__(self):
		self.parser = None
		self.username = ""
		self.url = "https://story.snapchat.com/s/"
		self.timeout = 30
		self.url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
		self.mp4_files = list()
		self.output_dir = "."

	def build_opt_parser(self):
		self.parser = optparse.OptionParser(usage="Usage: %prog -u USERNAME [-o PATH] [-t TIMEOUT]", version="Snapchat Story Downloader")

		self.parser.add_option("-u", "--username", dest="username", type="string", help="Username of account we want to download stories from")
		self.parser.add_option("-o", "--output", dest="output", type="string", help="Path where stories are stored. Default : current directory")
		self.parser.add_option("-t", "--timeout", dest="timeout", type="string", help="Requests timeout. Default : 30 seconds")

		(options, args) = self.parser.parse_args()

		if(not options.username):
			self.parser.error("Parameter -u/--username is required")
		else:
			self.username = options.username

		if(options.output):
			self.output_dir = options.output
		if(options.timeout):
			self.timeout = options.timeout

	def update_url(self):
		self.url = "https://story.snapchat.com/s/" + self.username

	def make_request(self):
		try:
			response = requests.get(self.url, timeout=self.timeout).text
			self.parse(response)
		except requests.exceptions.Timeout:
			print("Timeout reached")

	def parse(self, response):
		self.mp4_files = re.findall(self.url_regex, response)
		if(self.has_no_mp4()):
			print("User doesn't exist or has no story")
			return
		else:
			self.download_files()

	def has_no_mp4(self):
		count = 0
		for url in self.mp4_files:
			if(".mp4" in url):
				count += 1

		return count == 0

	def download_files(self):
		print("Starting downloading stories ...")
		for url in self.mp4_files:
			if(url.split(".")[-1] == "mp4"):
				try:
					dl_url = requests.get(url, timeout=self.timeout)
					self.save_file(dl_url, url)
				except requests.exceptions.Timeout:
					print("Timeout reached")
		print("Stories saved in " + self.output_dir)

	def save_file(self, data, url):
		filename = "/" + url.split("/")[-3] + ".mp4"
		with open(self.output_dir + filename, 'wb') as file:
 			file.write(data.content)

	def run(self):
		self.build_opt_parser()
		self.update_url()
		self.make_request()



if(__name__ == "__main__"):
	snap_dl = Snap_Story_Downloader() #wowthisistotallyawesomeman
	snap_dl.run()