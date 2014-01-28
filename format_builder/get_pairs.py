import re
import sys

ARTIST_PATTERN = 'Ar:(\S+)'
TAGS_URL_PATTERN = 'http://www.last.fm/music/%s/+tags'

def get_artist_list(filename):
	artist_list = []
	with open(filename, 'r') as file:
		for line in file:
			artist_list.append(re.findall(ARTIST_PATTERN, line.strip())[0])
	return artist_list

def get_pairs(artist_list):
	pair_list = []
	for artist in artist_list:
		pair_list.append((' '.join(map(lambda x: x.capitalize(), artist.split('+'))), TAGS_URL_PATTERN % artist))
	return pair_list

def write_file(outfile, pairs):
	with open(outfile, 'w') as file:
		for pair in pairs:
			file.write(pair[0] + ',' + pair[1] + '\n')

def main():
	filename = sys.argv[1]
	outfile = sys.argv[2]
	artist_list = get_artist_list(filename)
	pairs = get_pairs(artist_list)
	write_file(outfile, pairs)

if __name__ == '__main__':
	main()
