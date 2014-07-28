#!/usr/bin/python
try:
   import urllib.request
except:
   import urllib
try:  
   from bs4 import BeautifulSoup
except:
   try:
      from BeautifulSoup import BeautifulSoup
   except: 
      import BeautifulSoup.py
remaining = [
"ECEL 304"
,"ECEC 302"
,"ECEC 101"
,"CS 260"
]
baseURL = "https://duapp2.drexel.edu"
classAtt = ['Subject_Code', 'Course_Code', 'Instr_Type', 'Online_Integration', 'Section', 'CRN', 'Course_Title', 'Day(s)', 'Instructor' ]
MAX_LEN = 1500 # Maximum parse length of a course attribute

def getTerms(url):
	terms = {}
	htmlSoup = getContents(url)
	# All divs containing Quarter/Semester info have class="term"
	if(htmlSoup):
		for div in htmlSoup.findAll('div', 'term'):
			href = div.find('a')
			termName = href.getText()
			url = href.get('href').replace('&amp;', '&')
			thisTerm = getColleges(url)
			if(thisTerm):
				terms[termName] = thisTerm
	return terms
    
         
def getColleges(url):
	colleges ={}
	htmlSoup = getContents(url)
	# Colleges are the only hyperlinks in the left sidebar
	schools = htmlSoup.find(id='sideLeft')
	if(schools):
		for school in schools.findAll('a'):
			schoolName = school.getText()
			nextUrl = school.get('href').replace('&amp;', '&')
			thisCollege = getSubjects(url)
			if(thisCollege):
				colleges[schoolName] = thisCollege
	return colleges
     

def getSubjects(url):
	subjects = {}
	htmlSoup = getContents(url)

	# The Subjects are listed in a table of class='collegePanel'
	subjectTable = htmlSoup.find('table', 'collegePanel')
	if(subjectTable):
		for subject in subjectTable.findAll('a'):
			subjectName = subject.getText()
			nextUrl = subject.get('href').replace('&amp;', '&')
			thisSubject = getClasses(nextUrl)
			if(thisSubject):
				subjects[subjectName] = thisSubject
	return subjects
   
def getClasses(url):
	classes = {}
	htmlSoup = getContents(url)
	if(htmlSoup):
		for course in htmlSoup.findAll('tr'):
			if 'courseDetails' in str(course) and str(course).__len__() <= MAX_LEN:
				count = 0 
				newClass = getClass(course)
				className = newClass[classAtt[0]] + " " + newClass[classAtt[1]]
				if(newClass and isRemaining(className)):
					classes[className] = newClass
	return classes
         
def getClass(course):
	count = 0
	thisClass ={}
	if(course):
		for attribute in course.findAll('td', recursive=False):
			if attribute.get('colspan'):
				day = attribute.find('td')
				time = day.findNextSibling('td')
				thisClass['days'] = day.getText().strip()
				time = getTime(attribute)
				if(time):
					thisClass['time'] = time
			else: 
				# Attribute is a regular tag
				attributeString = attribute.getText().replace('&amp;', '&').strip()
				if(attributeString):
					try:
						thisClass[classAtt[count]] = attributeString
						#print(classAtt[count])
					except:
						thisClass[str(count)] = attributeString
						#print(str(count))
		      
			count += 1
	#dump(thisClass)
	return thisClass
	
def getTime(attribute):
	# Attribute is a day/time child tag
	day = attribute.find('td')
	time = day.findNextSibling('td')
	#thisClass['days'] = day.getText().strip()
	time12 = time.getText().strip()
	if(not time12 == "TBD"):
		start = int(time12[:4].strip().replace(":",""))
		end = int(time12[-7:-2].strip().replace(":",""))
		if(time12.find("pm", 4, 8) > 0):      
			start = start + 1200
		if(time12.find("pm", -3) > 0):
			end = end + 1200
	else:
		start = "TBD"
		end = "TBD"
	# NEED TO ADD A LINE TO CONVERT TO 24 hour clock
	return {'start' : start, 'end' : end}
          
def isRemaining(className):
	# cross reference with my remaining classes
	#print(className)
	if className in remaining:
		return True
	return False
   
	
def dump(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                dump(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v)
            else:
                print v
    else:
        print obj
        
def findScheduales(classes):
	print('')
	
def getContents(url):
   try: 
      with urllib.request.urlopen(baseURL + url) as url2:
         response = str(url2.read())
   except:
      response = urllib.urlopen(baseURL + url)
   
   return BeautifulSoup(response)
   
def main():
   allPosted = getTerms("/webtms_du/app")
   dump(allPosted)
   dump(findScheduales)

if __name__ == '__main__':
   main()
