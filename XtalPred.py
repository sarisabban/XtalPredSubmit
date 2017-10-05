#!/usr/bin/python3

import requests , Bio.PDB , re , urllib.request , bs4 , datetime , time , os , sys

#--------------------------------------------------------------------------------------------------------------------------------------
def Crystal(Protein):
	''' Submits the structur's FASTA sequence to the XtalPred server (http://ffas.burnham.org/XtalPred-cgi/xtal.pl) to calculate the probability of crystillisation '''
	''' Returns values between 1 and 5, 1 = Most Promissing 5 = Least Promissing '''
	Description = '>TEST2'
	parser = Bio.PDB.PDBParser()
	structure = parser.get_structure('X' , Protein)
	ppb = Bio.PDB.PPBuilder()
	aminos = list()
	for aa in ppb.build_peptides(structure):
		aminos.append(aa.get_sequence())
	Sequence = aminos[0]
	#1 - Post
	web = requests.get('http://www.robetta.org/fragmentsubmit.jsp')
	payload = {
		'query':Description + '\n' + Sequence,
		'mail':'',
		'agree':'on',
		'LabDir':'',
		'Submit':'Submit',
		'.cgifields':'CGM',
		'.cgifields':'SERP',
		'.cgifields':'agree',
	}
	session = requests.session()
	response = session.post('http://ffas.burnham.org/XtalPred-cgi/xtal.pl', data=payload , files=dict(foo='bar'))
	for line in response:
		line = line.decode()
		if re.search('Job id: ' , line):
			job =  re.findall('<b>Job id: (.*?)</b>' , line)
	JobURL = 'http://ffas.burnham.org/XtalPred-cgi/result.pl?dir=' + job[0] + '/0'
	print(datetime.datetime.now().strftime('%d %B %Y @ %H:%M'))
	print('Submitted to XtalPred. Results URL:' , JobURL)
	#2 - Check
	Job = urllib.request.urlopen(JobURL)
	jobdata = bs4.BeautifulSoup(Job , 'lxml')
	status = jobdata.find(string='Results of this job do not exist!')
	while True:
		time.sleep(60)
		if status == 'Results of this job do not exist!':
			print(datetime.datetime.now().strftime('%d %B %Y @ %H:%M') , 'Status: Still Calculating')
			continue
		else:
			print(datetime.datetime.now().strftime('%d %B %Y @ %H:%M') , 'Status: Done')
			break
	#3 - Get Result
	Job = urllib.request.urlopen('http://ffas.burnham.org/XtalPred-cgi/download.pl?dir=' + job[0] + '/0&type=summary')
	jobdata = bs4.BeautifulSoup(Job , 'lxml')
	for line in jobdata:
		line = line.decode()
		value = re.findall('Crystallization class:	([0-9])', line)[0]
		return(value)
#--------------------------------------------------------------------------------------------------------------------------------------
print(Crystal(sys.argv[1]))
