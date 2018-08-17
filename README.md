# gene_lights
Turn a genome into scrolling Christmas lights

## Summary
Read in a fasta file and turn each base into a trail of lights.
RUNX1.fa  

![](/gene_lights_RUNX1.GIF)

## Requirements
Raspberry Pi  
LED strip  
Python  
Neopixel library  

## Usage
Copy gene_lights.py into a directory with a fasta file or the default RUNX1.fa
python gene_lights.py [options]  
-f name of fasta file  
-l length of each light  
-d delay, how fast the lights move  
-s separation between lights  

## Acknowledgements
This script was based off strandtest.py.
