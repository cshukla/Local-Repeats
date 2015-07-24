#!/usr/bin/env python
from optparse import OptionParser
import glob, sys

###########################################################################################
# get_enhancer_local_repeats.py
#
# Input a file with the ratio of H3K4Me1/H3K4Me3 marks and extract the lines where the
# average ratio >=3. Read the BED file made to produce the ratios and output features
# corresponding to the average ratio >= 3.
###########################################################################################
def main():
	usage = 'usage:%prog [options] <bed_file> <enhancer_ratio.tab>'
	parser = OptionParser(usage)
	(options, args) = parser.parse_args()

	if len(args)!=2:
		parser.error('Must provide the BED file and the corresponding enhancer ratios')
	else:
		bed_file = args[0]
		enhancer_ratio = args[1]

	selected_lines = []
	i = 1
	for line in open(enhancer_ratio):
		if line[0]!='#':
			a = line.strip().split()
			for j in range(0,len(a)):
				a[j] = float(a[j])
			average_ratio = sum(a)/len(a)
			if average_ratio >= 3.0:
				selected_lines.append(i)
			i += 1

	i = 1
	for line in open(bed_file):
		if i in selected_lines:
			print line.strip()
		i += 1

###########################################################################################
# main()
###########################################################################################
if __name__ == '__main__':
	main()