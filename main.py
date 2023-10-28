import requests
import re
import optparse

class Snap_Story_Downloader:
	def __init__(self):
		self.parser = None
		self.username = ""
		self.url = "https://www.snapchat.com/add/"
		self.timeout = 30
		self.url_regex = r'https://(bolt-gcdn\.sc-cdn\.net|cf-st\.sc-cdn\.net)/[^"]*uc=75'
		self.url_regex2 = r'\.256\.'
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
		self.url = "https://www.snapchat.com/add/" + self.username

	def make_request(self):
		try:
			response = requests.get(self.url, timeout=self.timeout).text
			self.parse(response)
		except requests.exceptions.Timeout:
			print("Timeout reached")

	def parse(self, response):
		self.mp4_files = list()
		self.all_mp4_files = re.finditer(self.url_regex, response)

		for match in self.all_mp4_files:
			if not re.search(self.url_regex2, match.group(0)):
				self.mp4_files.append(match.group(0))

		if(len(self.mp4_files) == 0):
			print("User doesn't exist or has no story")
			return
		else:
			self.download_files()

	def download_files(self):
		print("Starting downloading stories ...")
		count = 0
		for url in self.mp4_files:
			try:
				dl_url = requests.get(url, timeout=self.timeout)
				self.save_file(dl_url, url, count)
			except requests.exceptions.Timeout:
				print("Timeout reached")
			count+=1
		print("Stories saved in " + self.output_dir)

	def save_file(self, data, url, count):
		filename = "/" + str(count) + "_" + url.split("/")[4].split(".")[0] + ".mp4"

		#Add FileNotFoundError exception and PermissionError
		try:
			with open(self.output_dir + filename, 'wb') as file:
				file.write(data.content)
		except FileNotFoundError:
			print("Error can't find the specified folder")
			exit(1)
		except PermissionError:
			print("Error can't access the specified folder. Check permissions or run this program with sudo rights")
			exit(2)

	def run(self):
		self.build_opt_parser()
		self.update_url()
		self.make_request()

if(__name__ == "__main__"):
	snap_dl = Snap_Story_Downloader()
	snap_dl.run()