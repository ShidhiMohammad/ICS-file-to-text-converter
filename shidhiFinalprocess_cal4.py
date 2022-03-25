#!/usr/bin/env python3

import sys
import re
import datetime
import argparse

class process_cal:
	def __init__(self,filename):
		self.filename=filename
		self.list_of_events = []
		self.temp_event = {}
		self.rrule_Event = {}

	'''
	Purpose: Parses the file and stores each line for reference later
	
	Parameters: Date given in command line
	Return: List that contains dictonaries
	'''
	def file_to_store(self, date):
		rruleExists = False
		Appended= False
		eventCounter = 0
	
		with open(self.filename,'r') as f:
			for line in f:
				line = line.strip('\n')
				Line = re.search(r'((.*):(.*)).*', line)

				if Line.group(1) == 'BEGIN:VEVENT':
					self.temp_event['DTSTART']=''
					self.temp_event['DTSTARTtime'] = ''
					self.temp_event['DTEND']=''
					self.temp_event['DTENDtime'] = ''
					self.temp_event['LOCATION']=''
					self.temp_event['SUMMARY']=''
					self.temp_event['RRULE']=''
					eventCounter += 1

				elif Line.group(2) == 'DTSTART':
					temp = Line.group(3)
					self.temp_event['DTSTART'] = datetime.datetime(int(temp[:4]), int(temp[4:6]), int(temp[6:8]))
					self.temp_event['DTSTARTtime'] = datetime.datetime(1,1,1, int(temp[9:11]), int(temp[11:13]), int(temp[13:15]))

				elif Line.group(2) == 'DTEND':
					temp = Line.group(3)
					self.temp_event['DTEND'] = datetime.datetime(int(temp[:4]), int(temp[4:6]), int(temp[6:8]), int(temp[9:11]), int(temp[11:13]), int(temp[13:15]))
					self.temp_event['DTENDtime'] = datetime.datetime(1,1,1, int(temp[9:11]), int(temp[11:13]), int(temp[13:15]))

				elif Line.group(2) == 'RRULE':
					rruleExists = True
					temp = re.search(r'.*IL=(.*);.*',Line.group(3))
					temp2 = temp.group(1)
					self.temp_event['RRULE'] = datetime.datetime(int(temp2[:4]), int(temp2[4:6]), int(temp2[6:8]))

				elif Line.group(2) == 'LOCATION':
					self.temp_event['LOCATION']=Line.group(3)

				elif Line.group(2) == 'SUMMARY':
					self.temp_event['SUMMARY']=Line.group(3)
					
				elif Line.group(1) == 'END:VEVENT':
					if(date == self.temp_event['DTSTART']):
						self.list_of_events.insert(0, self.temp_event)
						Appended = True
						# print(self.list_of_events)	

					if(self.temp_event['RRULE'] and rruleExists == True):
						
						incSt = self.temp_event['DTSTART']
						incE = self.temp_event['DTEND']

						while incSt <= self.temp_event['RRULE']:
							incSt = incSt + datetime.timedelta(days=7)
							incE = incE + datetime.timedelta(days=7)
							if incSt <= self.temp_event['RRULE']:
								self.rrule_Event['DTSTART'] = incSt
								self.rrule_Event['DTEND'] = incE
								self.rrule_Event['DTSTARTtime'] = self.temp_event['DTSTARTtime']
								self.rrule_Event['DTENDtime'] = self.temp_event['DTENDtime']
								self.rrule_Event['LOCATION'] = self.temp_event['LOCATION']
								self.rrule_Event['SUMMARY'] = self.temp_event['SUMMARY']
								self.list_of_events.append(self.rrule_Event)
								Appended = True
								self.rrule_Event = {}
					self.temp_event = {}

				elif Line.group(1) == 'END:VCALENDAR':
					break

		if Appended == True:
			return self.list_of_events
		else:
			return None
		
	'''
	Purpose: Final print code that shows on command line

	Parameters: Datetime object
	Return: Print output in command line
	'''
	def get_events_for_day(self, date):
		self.file_to_store(date)
		Inside = False		
		MultExists = False	
		out =''
		details = ''
		shortenedList = []		
		multipleEvent = []
		count = 0				
		numEvent = 0
		for i in self.list_of_events:
				
			if date == i['DTSTART']:
				count += 1
				shortenedList.append(i)
		if count > 1:
			MultExists = True

		if(MultExists == True):
			for j in shortenedList:
				Inside = True
				formatpart1= str(self.dateFormatter(j['DTSTART'])) + '\n'
				formatpart2= str('-'*len(self.dateFormatter(j['DTSTART'])))+'\n'
				formatpart3= str(self.timeFormatter(j['DTSTARTtime']))+' to '+str(self.timeFormatter(j['DTENDtime']))+': '+str(j['SUMMARY'])+' {{'+str(j['LOCATION'])+'}}'
				formatpart3 = str(formatpart3)
				if(numEvent > 0):
					l = len(multipleEvent)
					if(self.compareStrings(formatpart3, multipleEvent)) == False:
						multipleEvent.append(formatpart3)
				if(numEvent == 0):
					multipleEvent.append(formatpart3)
				numEvent += 1

			details = '\n'.join([str(item) for item in multipleEvent])
			if Inside == True:
				out = formatpart1+formatpart2+details
		else:
			for j in shortenedList:
				Inside = True
				formatpart1= str(self.dateFormatter(j['DTSTART'])) + '\n'
				formatpart2= str('-'*len(self.dateFormatter(j['DTSTART'])))+'\n'
				formatpart3= str(self.timeFormatter(j['DTSTARTtime']))+' to '+str(self.timeFormatter(j['DTENDtime']))+': '+str(j['SUMMARY'])+' {{'+str(j['LOCATION'])+'}}'
				formatpart3 = str(formatpart3)
				print('comp str in')
				out = formatpart1+formatpart2+formatpart3
				
		return out

	'''
	Purpose: Formats the date datetime object to be printed out a certain way

	Parameters: Datetime object
	Return: Returns formatted date given to print
	'''
	def dateFormatter(self, DS):
		return DS.strftime('%B %d, %Y (%a)')
		

	'''
	Purpose: Formats the time datetime object to be printed out a certain way

	Parameters: Datetime object
	Return: Returns formatted time given to print
	'''
	def timeFormatter(self, TF):
		h = TF.strftime('%I')
		if int(h) < 10:
			return TF.strftime(' %-I:%M %p')
		else:
			return TF.strftime('%-I:%M %p') 

	'''
	Purpose: Compares each string to each index in the list

	Parameters: A string and a list
	Return: True or false if string is in list
	'''
	def compareStrings(self, str1, list):
		bool = False
		for a_string in list:
			if(str1 == a_string):
				bool = True
		return bool
