#!/usr/bin/python
import re

genes = set()

with open('GLBRCY22-3.gff','r') as gffFile:
	for line in gffFile:
		match = re.search('gene=(\w+)',line)
		if match:
			genes.add(match.group(1))
for gene in genes:
	print(gene)