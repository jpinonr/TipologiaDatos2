#####################
# Code for get information from website
# jpinon
#####################
#--------------------
# Loading libraries
#--------------------
import re
import time
from bs4 import BeautifulSoup
from dateutil import parser
import requests
import pandas as pd 
import numpy as np 

#--------------------
# Function to get information
#--------------------
def get_information(time): #parameters for time are 
	if time != '30dias' and time != '10dias' and time != 'Anio':
		return 'ERROR. Acceptable periods are: 10dias, 30dias or Anio'
	else:
		url = "https://www.ign.es/web/ign/portal/ultimos-terremotos"
		# Get URL
		url = url+'/-/ultimos-terremotos/get'+time	
		# Get response from the url
		page = requests.get(url)
		#check response
		if page.status_code==200:
			print ('Status page OK')
		else:
			print (page.status_code)
			print ('Status page Error')
		# Get page content
		soup=BeautifulSoup(page.content)
		print(soup.prettify())
		#Find information based on tags 'td'
		tds = soup.findAll('td')
		# Get title and source
		title=soup.p.next_element 
		source=soup.title.next_element
		#Create empty list
		terremotos = []
		datos=[] #list of lists
		for i,td in enumerate(tds):
			if i+1 == len(tds):
				break
			a = td.next_element
			terremotos.append(a)
			if tds[i].next_element == ' ' and tds[i+1].next_element[:2]=='es':
				datos.append(terremotos)
				terremotos=[] #initializing
		# Format data
		print('Total of :' + str(len(datos)) + ' earthquake get from the webpage')
		# Convert to data frame
		datos = pd.DataFrame(datos)
		#Save data to csv
		datos.to_csv('Terremotos_'+time+'.csv',header=F)


#--------------------
# Example of result
#--------------------		
get_information('10dias')
get_information('30dias')
get_information('Anio')
