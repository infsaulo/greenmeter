import commands
import sys

def get_names(out_filename):
	artist_names = map(lambda x: 'Ar:' + x, commands.getoutput('ls outputs').split('\n'))
	with open(out_filename, 'w') as file:
		for artist_name in artist_names:
			file.write(artist_name + '\n')

def main():
	filename = sys.argv[1]
	get_names(filename)

if __name__ == '__main__':
	main()
