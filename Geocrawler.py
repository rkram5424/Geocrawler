# Author: Ryan Kramlich

import urllib, urllib2, cookielib, sys, getpass
from pygeocoder import Geocoder

def main():	
	# Ryan's Seafruit Supreme (patent pending)
	# Toppings: Pineapple, Black Olives, Anchovies, Green Peppers, Mushrooms	

	log_in()

def log_in():
	print('Welcome to GeoCrawler.\nGeoCrawler is an easy way to collect Geocache information in batches.')
	# login = raw_input('Geocaching.com login: ')
	login = 'drsafetymd'
	# password = getpass.getpass('Geocaching.com password: ')
	password = 'melonballs'

	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	login_data = urllib.urlencode({'username' : login, 'j_password' : password})
	page = opener.open('http://www.geocaching.com/login/default.aspx', login_data)
	print page.read()
	# search = raw_input('Location: ')
	# search_num = raw_input('Number of Caches to collect: ')
	search = '36830'
	search_num = 20
	results = Geocoder.geocode(search)
	search_url = 'http://www.geocaching.com/seek/nearest.aspx?lat=' + str((results[0].coordinates)[0]) + '&lng=' + str((results[0].coordinates)[1]) + '&dist=100'
	page = opener.open(search_url)
	data = page.read()
	start_bracket = 'http://www.geocaching.com/geocache/GC'
	end_bracket = '"'
	addr_array = []
	data = clear_before(data, 'class="favorite-rank"')
	for i in range(search_num):
		addr_array.append('http://www.geocaching.com/geocache/GC' + find_between(data, start_bracket, end_bracket))
		data = data.replace(addr_array[i], '')
		data = clear_before(data, addr_array[i])

	f = open('details.txt', 'w')
	for i in range(len(addr_array)):
		detail = collect_cache(addr_array[i], opener)
		for j in range(8):
			f.write(detail[j] + ' ')
		f.write('\n')

def collect_cache(url, opener):
	page = opener.open(url)
	data = page.read()
	detail_array = []

	name = find_between(data, 'CacheName">', '</span>')
	coords = find_between(data, '"uxLatLon">', '</span>')
	difficulty = find_between(data, 'with difficulty of ', ',')
	terrain = find_between(data, ', terrain of ', '. ')
	size = find_between(data, 'alt="Size: ', '"')
	info = find_between(data, 'ShortDescription">', '</span>')
	info = info + find_between(data, 'LongDescription">', '</span>')
	info = info.replace('<br />', '\n')
	key = '''
A|B|C|D|E|F|G|H|I|J|K|L|M
-------------------------
N|O|P|Q|R|S|T|U|V|W|X|Y|Z
	'''
	hint = find_between(data, '<div id="div_hint" class="span-8 WrapFix">', '</div>')

	detail_array.append(name)
	detail_array.append(coords)
	detail_array.append(difficulty)
	detail_array.append(terrain)
	detail_array.append(size)
	detail_array.append(info)
	detail_array.append(key)
	detail_array.append(hint)

	return detail_array

def clear_before(s, sample):
	try:
		start = s.index(sample) + len(sample)
		end = len(s) - 1
		return s[start:end]
	except ValueError:
		return s

def find_between(s, first, last ):
    try:
        start = s.index(first) + len(first)
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

if __name__ == '__main__':
	main()