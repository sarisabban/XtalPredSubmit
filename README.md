# XtalPredSubmit
A script that submits a query to the XtalPred server for protein crystallisability prediction

## About:
This script takes a .pdb protein structure file and submits its FASTA sequence to the [XtalPred](http://ffas.burnham.org/XtalPred-cgi/xtal.pl) server to predict how easy it is to crystalise this protein.

## Requirements:
Use the following commands (in GNU/Linux) to install all nessesary programs and Python libraries for this script to run successfully:

`sudo apt install python3-pip python-lxml -y && sudo python3 -m pip install biopython bs4`

## How To Use:
Use the following command to run the script:

`python3 XtalPred.py FILENAME.pdb`

## Result
As per the XtalPred server's documentation a score of 1 is predicted to be most promising to crystalise and a score of 5 is predicted to be least promising to crystalise. The script prints out the date, time, and link of the submitted query (for reference) and when the computation is done it simply prints out an integer from 1 to 5. If there are errors with the submission it is probably the protein .pdb file itself, make sure the file has continuous chains, and that the script is printing the correct FASTA sequence (a simple print statement after line 16). 
