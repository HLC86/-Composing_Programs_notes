#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:08:25 2022

@author: hongliangchai
"""

from urllib.request import urlopen
shakespeare = urlopen('http://composingprograms.com/shakespeare.txt')

words = set(shakespeare.read().decode().split())
{w for w in words if len(w) == 6 and w[::-1] in words}

#%%

# book (ICPUP) chp 4 
def factI(n):
    """Assumes n an int > 0
        Return n!"""
    result = 1
    while n > 1:
        result = result * n
        n -= 1
    return result

def factR(n):
    """Assumes n an int > 0
        Return n!"""
    
    if n == 1:
        return n
    else:
        return n*factR(n - 1)

#%% chp 8 OOP

class IntSet(object):
    
    def __init__(self):
        self.vals = []
    
    def insert(self, e):
        if e not in self.vals:
            self.vals.append(e)
    
    def member(self, e):
        return e in self.vals
    
    def remove(self, e):
        try:
            self.vals.remove(e)
        except:
            raise ValueError(str(e) + ' not found')

    def getMembers(self):
        return self.vals[:]
    
    def __str__(self):
        self.vals.sort()
        result = ''
        for e in self.vals:
            result = result + str(e) + ','
        return '{' + result[:-1] + '}' # -1 omits trailing comma
    
s = IntSet()

# class variables vs instance variables
#%%
import datetime
class Person(object):
    
    def __init__(self, name):
        self.name = name
        try:    
            lastBlank = name.rindex(' ')
            self.lastName = name[lastBlank+1:]
        except:
            self.lastName = name
        self.birthday = None
    
    def getName(self):
        return self.name
    
    def getLastName(self):
        return self.lastName
    
    def setBirthday(self, birthdate):
        self.birthday = birthdate
    
    def getAge(self):
        if self.birthday == None:
            raise ValueError
        return (datetime.date.today() - self.birthday).days
    
    def __lt__(self, other):
        if self.lastName == other.lastName:
            return self.name < other.name
        return self.lastName < other.lastName
    
    def __str__(self):
        return self.name

#%%
# 8.2 inheritance
class MITPerson(Person):
    nextIdNum = 0 # class variable
    
    def __init__(self, name):
        Person.__init__(self, name)
        self.idNum = MITPerson.nextIdNum
        MITPerson.nextIdNum += 1
        
    def getIdNum(self):
        return self.idNum
    
    def __lt__(self, other):
        return self.idNum < other.idNum
    
    def isStudent(self):
        return isinstance(self, Student)

p1 = MITPerson('Barbare Beaver')
print(str(p1) + '\'s id number is ' + str(p1.getIdNum()))         


class Student(MITPerson):
    pass

class UG(Student):
    def __init__(self, name, classYear):
        MITPerson.__init__(self, name)
        self.year = classYear
    
    def getClass(self):
        return self.year
    
class Grad(Student):
    pass

p6 = UG('Billy Beaver', 1984)

#%%
#encapsulation and information hiding
class Grades(object):
    def __init__(self):
        self.students = []
        self.grades = {}
        self.isSorted = True
    
    def addStudent (self, student):
        if student in self.students:
            raise ValueError('Duplicate student')
        self.students.append(student)
        self.grades[student.getIdNum()] = []
        self.isSorted = False
        
    def addGrade(self, student, grade):
        try:
            self.grades[student.getIdNum()].append(grade)
        except:
            raise ValueError('Student not in mapping')

    def getGrades(self, student):
        try:
            return self.grades[student.getIdNum()][:]
        except:
            raise ValueError('Student not in mapping')
        
    # def getStudents(self):
    #     if not self.isSorted:
    #         self.students.sort()
    #         self.isSorted = True
    #     return self.students[:]
    def getStudents(self):
        """Return the students in the grade book one at a time"""
        if not self.isSorted:
            self.students.sort()
            self.isSorted = True
        for s in self.students:
            yield s
            
            
            
#%%
def gradeReport(course):
    report = ''
    for s in course.getStudents():
        tot = 0.0
        numGrades = 0
        for g in course.getGrades(s):
            tot += g
            numGrades += 1
        try:
            average = tot/numGrades
            report = report + '\n'\
                     + str(s) + '\'s mean grade is ' + str(average)
        except ZeroDivisionError:
            report = report + '\n'\
                        + str(s) + ' has no grades'
                        
    return report
          
#%%

ug1 = UG('Jane Doe', 2014)
g1 = Grad('Billy Buckner')
ug3 = UG('David Henry', 2003)

sixHundred = Grades()
sixHundred.addStudent(ug1)
sixHundred.addStudent(g1)            
sixHundred.addStudent(ug3)
for s in sixHundred.getStudents():
    sixHundred.addGrade(s, 75)

sixHundred.addGrade(g1, 25)
print(gradeReport(sixHundred))    


#%%
monthNumbers = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5,
                1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May'}
keys = []
for e in monthNumbers:
    keys.append(str(e))
print(keys)     
keys.sort()
print(keys)

test = monthNumbers.keys()
print(test)

monthNumbers[6] = 'June'

#%%
def findPayment(loan, r, m):
    """return the monthly pmt for a mortgage of size 
        loan at a monthly rate of r for m months"""         
    return loan*((r*(1+r)**m)/((1+r)**m - 1))        
           
class Mortgage(object):
    def __init__(self, loan, annRate, months):
        """
        create a new mortgage of size loan, duration months, and annual rate annRate
        """
        self.loan = loan
        self.rate = annRate/12
        self.months = months
        self.paid = [0.0]
        self.outstanding = [loan]
        self.payment = findPayment(loan, self.rate, months)
        self.legend = None #description of mortgage
        
    def makePayment(self):
        self.paid.append(self.payment)
        reduction = self.payment - self.outstanding[-1]*self.rate
        self.outstanding.append(self.outstanding[-1] - reduction)
        
    def getTotalPaid(self):
        return sum(self.paid)
    
    def __str__(self):
        return self.legend

class Fixed(Mortgage):
    def __init__(self, loan, r, months):
        Mortgage.__init__(self, loan, r, months)
        self.legend = 'Fixed,' + str(round(r*100, 2)) + '%'

class FixedWithPts(Mortgage):
    def __init__(self, loan, r, months, pts):
        Mortgage.__init__(self, loan, r, months)
        self.pts = pts
        self.paid = [loan* (pts/100)]
        self.legend = 'Fixed,' + str(round(r*100, 2)) + '%, '\
                        + str(pts) + ' points'

class TwoRate(Mortgage):
    def __init__(self, loan, r, months, teaserRate, teaserMonths):
        Mortgage.__init__(self, loan, teaserRate, months)
        self.teaserMonths = teaserMonths
        self.teaserRate = teaserRate
        self.nextRate = r/12
        self.legend = str(teaserRate*100)\
                        + '% for ' + str(self.teaserMonths)\
                            + ' months, then ' + str(round(r*100, 2)) + '%'

    def makePayment(self):
        if len(self.paid) == self.teaserMonths + 1:
            self.rate = self.nextRate
            self.payment = findPayment(self.outstanding[-1], self.rate, self.months - self.teaserMonths)
        Mortgage.makePayment(self)
        
def compareMortgages(amt, years, fixedRate, pts, ptsRate, varRate1, varRate2, varMonths):
    totMonths = years * 12
    fixed1 = Fixed(amt, fixedRate, totMonths)
    fixed2 = FixedWithPts(amt, ptsRate, totMonths, pts)
    twoRate = TwoRate(amt, varRate2, totMonths, varRate1, varMonths)
    morts = [fixed1, fixed2, twoRate]
    for m in range(totMonths):
        for mort in morts:
            mort.makePayment()
    for m in morts:
        print(m)
        print(' Total payments = $' + str(int(m.getTotalPaid())))
            
compareMortgages(amt = 20000, years = 30, fixedRate = 0.07, pts = 3.25, ptsRate = 0.05,
                 varRate1 = 0.045, varRate2 = 0.095, varMonths = 48)

#%%
def sum_naturals(n):
    """Return the sum of the first n natural numbers.

    >>> sum_naturals(10)
    55
    """
    total, k = 0, 1
    while k <= n:
        total, k = total + k, k + 1
    return total

from doctest import testmod
testmod()

# %%
from doctest import run_docstring_examples
run_docstring_examples(sum_naturals, globals(), True)
# %%
# function decorators
def trace(fn):
    def wrapped(x):
        print('-> ', fn, '(', x, ')')
        return fn(x)
    return wrapped

@trace
def triple(x):
    return 3 * x
