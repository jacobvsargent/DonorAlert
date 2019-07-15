import sys
import time
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import Select

#add chromedriver to environmental variables in sys
path = "C:\\Drivers\\chromedriver.exe"
sys.path.append(path)
driver = webdriver.Chrome(path)

relevant_input = []

def read_raw():
	global relevant_input

	with open('found_data.csv', 'r') as csvFile:
		read_data = csv.reader(csvFile)
		for row in read_data:
			if (not row[0]=="NAME"):
				relevant_input.append(row)

	print("Data has been read!")

def get_bios():
	driver.get("http://www.google.com")




def main():
	read_raw()
	get_bios()

main()