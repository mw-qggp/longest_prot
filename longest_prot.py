from Bio import SeqIO
import sys
import gzip
import re


def read_file(input_file):

	dict_fasta = {}

	fasta_sequences = SeqIO.parse(gzip.open(input_file,"rt"),'fasta')
	
	for fasta in fasta_sequences:
        	
		name, sequence = str(fasta.id), str(fasta.seq)

		name2 = name.split('.')
		

		if name[0] not in dict_fasta:
			
			dict_fasta[name2[0]+name2[1]] = [name2[0]+"_"+name2[1]+"-"+sequence]

		else:

			dict_fasta[name2[0]+name2[1]].append(name2[0]+"_"+name2[1]+"-"+sequence)

	return dict_fasta


def longest_seq(dict_input):

	dict_longest_seq = {}

	for groups in dict_input.keys():
		
		index_sign = str(dict_input[groups]).find("-")
	
		index_sign = index_sign - 1
	
		dict_longest_seq[str(max(dict_input[groups], key=len))[:index_sign]] = str(max(dict_input[groups], key=len))[index_sign:]

	return dict_longest_seq


def write_output(dict_longest,outfile):

	with open(outfile, 'w') as handle:
    
		for seqs in dict_longest.keys():

			handle.write(re.sub("(.{60})", "\\1\n",">"+seqs+"\n"+dict_longest[seqs]+"\n", re.DOTALL))


dict_fasta = read_file(sys.argv[1])
dict_longest = longest_seq(dict_fasta)

write_output(dict_longest,sys.argv[2])
