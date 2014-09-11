# output the tags for the omics portal
python manage.py dumpdata tags --indent 4 > tags_sqlite.json

# Level 0:
Genomics Transcriptomics Epigenomics Proteomics Foodomics Otheromics

# Level 1:
# Genomics:
Structural variation
Population genetics
Comparative genomics
Genome resequencing

# Epigenomics
Transcription factor
Histone modification

