import os
import shutil
try:
	import toml
except:
	os.system('pip3 install toml')
	import toml

# redirects = {
# 	[[redirects]]
#   from = "/old-path"
#   to = "/new-path"
#   status = 301
#   force = false
#   query = {path = ":path"}
#   conditions = {Language = ["en"], Country = ["US"], Role = ["admin"]}


# }

netlify = {'redirects':[]}
urls = toml.load('urls.toml')

class Redirect:
	src = ""
	dest = ""
	status = 302
	force = True
	languages = []
	countries = []
	roles = []

	def __init__(self, url):
		self.src = '/'+url.replace('/','')

	def todict(self):
		d =  {
			"from": self.src,
			"to": self.dest,
			"status": self.status,
			"force": self.force,
			"conditions": {}
		}
		if self.languages != []:
			d["conditions"]["Language"] = self.languages
		if self.countries != []:
			d["conditions"]["Country"] = self.countries
		if self.roles != []:
			d["conditions"]["Role"] = self.roles
		return d

for link in urls['link']:
	key = link['key']
	for rule in link['rule']:
		re = Redirect(key)
		re.dest = rule['url'] if rule['url'].startswith('https://') else "https://"+rule['url']
		re.countries = rule['country'] if 'country' in rule else []
		re.languages = rule['language'] if 'language' in rule else []
		re.headers = rule['headers'] if 'headers' in rule else {}
		
		if rule['password'] != False:
			re.src = re.src + "/" + rule['password']

		netlify['redirects'].append(re.todict())

		if rule['password'] != False:
			rp = re
			rp.__init__(key)
			rp.status = 200
			rp.dest = "/password.html"
			netlify['redirects'].append(rp.todict())			

if os.path.isdir('build'):
	shutil.rmtree('build')
os.mkdir('build')
shutil.copy('index.html','build/index.html')
shutil.copy('password.html','build/password.html')
shutil.copy('netlify.toml','build/netlify.toml')

with open('netlify.toml', 'a') as file:
	file.write(toml.dumps(netlify))

with open('build/netlify.toml', 'a') as file:
	file.write(toml.dumps(netlify))