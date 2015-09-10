#!/usr/bin/env python
from optparse import OptionParser
from collections import defaultdict
import sys, tempfile, subprocess, os, ggplot

################################################################################
# transmap_bed.py
#
# Extract Transmapped features for all features in a BED file
#
# Input a transmap BED file, transmap info file and feature BED file. For each
# feature in the input BED file, find overlaps with different organisms using 
# transmap BED and info files.
################################################################################

################################################################################
# main
################################################################################
def main():
	usage='usage:%prog [options] <input_bed> <transmap_bed> <transmap_info>'
	parser = OptionParser(usage)
	parser.add_option('-o', dest='organisms', default='self', help='Comma seperated list of organisms for which you want to map input features to TransMap')
	parser.add_option('-p', dest='out_pdf', default='transmap_bed_heat.pdf', help='Output PDF [Default: %default]')
	(options, args) = parser.parse_args()

	if len(args)!=3:
		parser.error('Must provide all the 3 files \n%s' %(usage))
	else:
		input_bed = args[0]
		transmap_bed = args[1]
		transmap_info = args[2]

	print >> sys.stderr, 'Intersecting the input BED file with TransMap BED file...'
	input_transmap_intersect_fd, input_transmap_intersect_file = tempfile.mkstemp()
	subprocess.call('intersectBed -wa -wb -a %s -b %s > %s' %(input_bed, transmap_bed, input_transmap_intersect_file), shell=True)
	print >> sys.stderr, 'intersectBed has finished running'

	print >> sys.stderr, 'Hashing the mapped IDs and source database using TransMap info file...'
	mapped_ids_src_db = {}
	for line in open(transmap_info):
		a = line.strip().split()
		mapped_id, src_db = a[0], a[1]
		mapped_ids_src_db[mapped_id] = src_db
	print >> sys.stderr, 'Finished hashing'

	print >> sys.stderr, 'Mapping input features to TransMap features...'
	input_feature_transmap = defaultdict(list)
	for line in open(input_transmap_intersect_file):
		a = line.strip().split()
		input_feature = a[3]
		transmap_feature = a[7]
		transmap_org = mapped_ids_src_db[transmap_feature]
		input_feature_transmap[input_feature].append(transmap_org)
	print >> sys.stderr, 'Finished mapping'
	input_transmap_count = len(input_feature_transmap.keys())
	print >> sys.stderr, 'Successful TransMap hit found for %d features' %input_transmap_count

	print >> sys.stderr, 'Preparing dataframe based on Input feature -- TransMap organism hash...'
	if options.organisms == 'self':
		all_organims = []
		for feature in input_feature_transmap.keys():
			organisms = input_feature_transmap[feature]
			for org in organisms:
				if org not in all_organims:
					all_organims.append(org)
		print >> sys.stderr, 'No list of organisms was supplied \nFinished learning organisms. They are \n%s' %(','.join(all_organims))
	else:
		all_organims = options.organisms.split(',')
	df = {'Feature':[], 'Organism':[], 'TransMap':[]}
	for feature in input_feature_transmap.keys():
		transmap_feature_org = input_feature_transmap[feature]
		for org in all_organims:
			df['Feature'].append(feature)
			df['Organism'].append(org)
			if org in transmap_feature_org:
				df['TransMap'].append(1)
			else:
				df['TransMap'].append(0)
	print >> sys.stderr, 'Made dataframe'

	print >> sys.stderr, 'Plottig dataframe as a heatmap in R'
	ggplot.plot('/Users/chinmayshukla/Documents/Research/Local-Repeats/bin/r_scripts/transmap_bed.r', df, [options.out_pdf])

	print >> sys.stderr, 'Computation finished \nCleaning temp files now...'
	os.close(input_transmap_intersect_fd)
	os.remove(input_transmap_intersect_file)
	print >> sys.stderr, 'Done!'

################################################################################
#
################################################################################
if __name__ == '__main__':
	main()