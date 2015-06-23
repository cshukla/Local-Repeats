#!/usr/bin/env python

from optparse import OptionParser
import os, subprocess, tempfile, sys, ggplot

################################################################################
# repeat_distribution.py
#
# Given a GTF File find the distribution of local repeats for the features.
################################################################################
def main():
	usage = 'usage:%prog [options] <gtf_file> <genome_fasta>'
	parser = OptionParser(usage)
	parser.add_option('-o', dest='output_pre', default='repeat_distribution')
	(options, args) = parser.parse_args()

	if len(args)!=2:
		parser.error('Must provide GFF file')
	else:
		gtf_file = args[0]
		genome_fasta = args[1]

	df = {'Local.Repeats':[], 'Tandem.Repeats':[], 'Total.Repeats':[], 'Position':[], 'Gene_ID':[], 'Gene_Name':[]}
	for line in open(gtf_file):
		a = line.split('\t')
		chromosome, start, end = a[0], a[3], a[4]
		#feature_details = a[8]
		#gene_id = feature_details.split(';')[0].split('"')[1]
		#gene_name = feature_details.split(';')[4].split('"')[1]
		position = chromosome + ':' + start + '-' + end
		#print '\t'.join([position, gene_id, gene_name])
		local_repeats, tandem_repeats = get_repeats(chromosome, start, end, genome_fasta)
		#print >> sys.stderr, local_repeats
		#print >> sys.stderr, tandem_repeats
		#df['Gene_ID'].append(gene_id)
		#df['Gene_Name'].append(gene_name)
		df['Position'].append(position)
		df['Local.Repeats'].append(local_repeats)
		df['Tandem.Repeats'].append(tandem_repeats)
		df['Total.Repeats'].append(local_repeats + tandem_repeats)

	#print >> sys.stderr, df
	df_file = open(options.output_pre + '_df.txt', 'w')
	#print >> df_file, '\t'.join(['Position', 'Gene_ID', 'Gene_Name', 'Local.Repeats', 'Tandem.Repeats', 'Total.Repeats'])
	print >> df_file, '\t'.join(['Position', 'Local.Repeats', 'Tandem.Repeats', 'Total.Repeats'])
	for i in range(0, len(df['Local.Repeats'])):
		#print >> df_file, '\t'.join([str(df['Position'][i]), df['Gene_ID'][i], df['Gene_Name'][i], str(df['Local.Repeats'][i]), str(df['Tandem.Repeats'][i]), str(df['Total.Repeats'][i])])
		print >> df_file, '\t'.join([str(df['Position'][i]), str(df['Local.Repeats'][i]), str(df['Tandem.Repeats'][i]), str(df['Total.Repeats'][i])])

	df_file.close()
	#r_script = '/n/rinn_data1/users/cshukla/firre/bin/repeat_distribution.R'
	#ggplot.plot(r_script, df, [options.output_pre])

def get_repeats(chromosome, start, end, genome_fasta):
	############################################
	# Get feature sequence
	############################################
	sequence_fd, sequence_file = make_fasta(chromosome, start, end, genome_fasta)

	############################################
	# Get Local Repeats in the sequence
	############################################
	lmer_fd, lmer_file = tempfile.mkstemp()
	subprocess.call('build_lmer_table -l 16 -sequence %s -freq %s' %(sequence_file, lmer_file), shell=True)
	repeatscout_fd, repeatscout_file = tempfile.mkstemp()
	subprocess.call('RepeatScout -sequence %s -output %s -freq %s -l 16' %(sequence_file, repeatscout_file, lmer_file), shell=True)
	local_repeats = 0
	for line in open(repeatscout_file):
		if line[0] == '>':
			local_repeats += 1

	############################################
	# Get Tandem Repeats in the sequence
	############################################
	tandem_repeats_count = 0
	trf_fd, trf_file = tempfile.mkstemp()
	subprocess.call('trf407b.linux %s 2 7 7 80 10 50 500 -d -ngs -h > %s' %(sequence_file, trf_file), shell=True)
	tandem_repeats_count = sum(1 for line in open(trf_file)) - 1
	if tandem_repeats_count < 0:
		tandem_repeats_count = 0

	############################################
	# clean
	############################################
	os.close(sequence_fd)
	os.remove(sequence_file)
	os.close(lmer_fd)
	os.remove(lmer_file)
	os.close(repeatscout_fd)
	os.remove(repeatscout_file)
	os.close(trf_fd)
	os.remove(trf_file)

	return [local_repeats, tandem_repeats_count]

def make_fasta(chromosome, start, end, genome_fasta):
	feature_gtf_fd, feature_gtf = tempfile.mkstemp()
	feature_gtf_file = open(feature_gtf,'w')
	gtf_line = '\t'.join([chromosome, 'Cufflinks', 'Exon', start, end, '.', '+', '.', 'Feature_GTF'])
	print >> feature_gtf_file, gtf_line
	feature_gtf_file.close()
	sequence_fd, sequence_file = tempfile.mkstemp()
	subprocess.call('gtf_to_fasta %s %s %s' %(feature_gtf, genome_fasta, sequence_file),shell=True)

	############################################
	# clean
	############################################
	os.close(feature_gtf_fd)
	os.remove(feature_gtf)

	return sequence_fd, sequence_file

################################################################################
#
################################################################################
if __name__ == '__main__':
	main()
