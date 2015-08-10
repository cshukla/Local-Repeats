#!/usr/bin/env python

from optparse import OptionParser

#########################################################################################
# contacts_to_links.py
# 
# Input a list of contacts obtained in *C or ChIA-PET experiment. Output a links file 
# suitable to be plotted using Circos.
#########################################################################################
def main():
	usage='usage:%prog [options] <contacts_file>'
	parser = OptionParser(usage)
	(options, args) = parser.parse_args()

	if len(args)!=1:
		parser.error('Must provide contacts file')
		parser.error(usage)
	else:
		contacts_file = args[0]

	contacts_color_mapping = {'1':'color=vvvlgrey,thickness=1', '2':'color=vvlgrey,thickness=1', '3':'color=lred,thickness=2', '4':'color=dred,thickness=4', '5':'color=vdred,thickness=16'}
	for line in open(contacts_file):
		a = line.strip().split('\t')
		chrom1 = 'hs' + a[0][3:]
		chrom2 = 'hs' + a[2][3:]
		start1 = a[1]
		end1 = int(a[1]) + 1
		start2 = a[3]
		end2 = int(a[3]) + 1
		color_thick = contacts_color_mapping[a[4]]
		out_line = ' '.join([chrom1, start1, str(end1), chrom2, start2, str(end2), color_thick])
		print out_line

#########################################################################################
# main()
#########################################################################################
if __name__ == '__main__':
	main()