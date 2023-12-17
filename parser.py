import argparse
import ssd

class Parser:
	def __init__(self):
		self.parser = None
		self.args = None

		self.username = ""
		self.output_dir = "."
		self.timeout = 30

		self.list_all = False
		self.list_user = False
		self.list_stories = False
		self.list_highlights = False
		self.list_spotlights = False
		self.list_lenses = False

		self.stats = False

		self.opt_heatmap = False

		self.download_bool = False

		self.download_all = False
		self.download_stories = False
		self.download_highlights = False
		self.download_spotlights = False
		self.download_lenses = False


	def build_arg_parser(self):	
		epilog = f"EXAMPLES:\nShow stats for a specific user:\n\tpython3 main.py -u <SNAP_USER> -s\n\nList all elements (account, stories, curated highlights, spotlights, lenses) for a specific user:\n\tpython3 main.py -u <SNAP_USER> -l a\n\nList stories, spotlights and generate a heatmap related to this data based on upload date:\n\tpython3 main.py -u <SNAP_USER> -l sp -m\n\nList stories, download everything (stories, curated highlights, spotlights, lenses) and store them to directory 'data':\n\tpython3 main.py -u <SNAP_USER> -l s -d a -o ./data"	
		
		self.parser = argparse.ArgumentParser(description="Snapchat Story Downloader - Made by KrowZ", epilog=epilog, argument_default=argparse.SUPPRESS, formatter_class=argparse.RawTextHelpFormatter)

		self.parser.add_argument("-u", "--username", dest="username", type=str, help="Username of account we want to download stories from")
		self.parser.add_argument("-s", "--stats", dest="stats", action="store_true", help="Only prints summary and statistics about the account")
		self.parser.add_argument("-l", "--list", nargs="?", const="u", metavar='OPTIONS', help="List the desired information. By default, lists only user information. 'a' = all, 's' = stories, 'u' = user, 'c' = curated highlights, 'p' = spotlights, 'l' = lenses. Multiple options can be combined together: E.g: -l 'csl'")
		self.parser.add_argument("-m", "--heatmap", dest="heatmap", action="store_true", help="Generates a heatmap related to upload dates. Must be used with '-l/--list' option")
		self.parser.add_argument("-d", "--download", nargs="?", const="s", metavar='OPTIONS', help="Downloads specific videos posted by a user. By default, only downloads current stories. 'a' = all, 's' = stories, 'c' = curated highlights, 'p' = spotlights, 'l' = lenses. Multiple options can be combined together: E.g: -d 'csl'")
		self.parser.add_argument("-o", "--output", dest="output", type=str, metavar='DIRECTORY', help="Path where stories are stored. Default : current directory")
		self.parser.add_argument("-t", "--timeout", dest="timeout", type=str, help="Requests timeout. Default : 30 seconds")

		self.args = self.parser.parse_args()

		#It means the user specified the -l option but with nothing behind
		if("list" in self.args):
			for letter in self.args.list:
				if(letter not in 'auscpl'):
					self.parser.error("You must specify a valid option for -l/--list")
				if(letter == 'a'):
					self.list_all = True
				else:
					if(letter == 'u'):
						self.list_user = True
					if(letter == 's'):
						self.list_stories = True
					if(letter == 'c'):
						self.list_highlights = True
					if(letter == 'p'):
						self.list_spotlights = True
					if(letter == 'l'):
						self.list_lenses = True

		if("download" in self.args):
			for letter in self.args.download:
				if(letter not in 'ascpl'):
					self.parser.error("You must specify a valid option for -d/--download")
				if(letter == 'a'):
					self.download_all = True
				else:
					if(letter == 's'):
						self.download_stories = True
					if(letter == 'c'):
						self.download_highlights = True
					if(letter == 'p'):
						self.download_spotlights = True
					if(letter == 'l'):
						self.download_lenses = True

			#If any of download is required
			self.download_bool = True

		if(not "username" in self.args):
			self.parser.error("Parameter -u/--username is required")
		else:
			self.username = self.args.username

		if("stats" in self.args):
			self.stats = True

		if("heatmap" in self.args and not "list" in self.args):
			self.parser.error("You cannot generate a heatmap without -l/--list option")

		if("output" in self.args):
			self.output_dir = self.args.output
		if("timeout" in self.args):
			self.timeout = self.args.timeout
		if("heatmap" in self.args):
			self.opt_heatmap = True

		if(not "list" in self.args and not "download" in self.args and not "stats" in self.args):
			self.parser.error("Must must specify at least one of these options: -l/--list, -d/--download, -s/--stats")

		if("stats" in self.args and ("list" in self.args or "download" in self.args)):
			self.parser.error("You can't use option -s/--stats with -l/--list and/or -d/--download")