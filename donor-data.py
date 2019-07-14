from selenium import webdriver
from selenium.webdriver.support.ui import Select
from tkinter import *

import sys
import time
import csv

#create the root
gui = Tk()

#for my ego
gui.title("DONOR ALERT V A0.0")
Label(gui, text="DONOR ALERT: VERSION ALPHA 0.0").pack()
Label(gui, text="Created by: Jacob Sargent").pack()

#breathing room
Label(gui, text="--------------------------------------------------------------------").pack()
Label(gui, text="").pack()



#makes arrays for the mack daddys
relevant_input = []
relevant_output = []

#variables
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSebufKaJNx0ERViyxIwij19XeEuY6GT-4ALlXhEhsdJjTue4g/viewform"
moneyline_url = "http://politicalmoneyline.com/tr/tr_MG_IndivDonor.aspx?&tm=3"

#add chromedriver to environmental variables in sys
path = "C:\\Drivers\\chromedriver.exe"
sys.path.append(path)
driver = webdriver.Chrome(path)

all_don_t = []
all_don_d = []
p_dem = []
f_names = []
l_names = []
donor_texts = []

def read_raw():
	global relevant_input

	with open('data.csv', 'r') as csvFile:
		read_data = csv.reader(csvFile)
		for row in read_data:
			if (not row[0]=="NAME"):
				relevant_input.append(row)

	print("Data has been read!")
	
def search_moneyline():
	global all_don_t
	global all_don_d
	global p_dem
	global f_names
	global l_names

	data_count = 0

	while (data_count < len(relevant_input)):

		driver.get(moneyline_url)

		time.sleep(1)

		donor_name_input = driver.find_element_by_id("ctl00_ContentPlaceHolder1_TabContainer1_TC1TP4_tbDonor")
		donor_name_input.send_keys(relevant_input[data_count][0])

		state_input = (driver.find_element_by_id("ctl00_ContentPlaceHolder1_TabContainer1_TC1TP4_ddlStateDropDownList6"))
		state_input.click()
		state_input.send_keys(relevant_input[data_count][3])

		a2020box = driver.find_element_by_id("ctl00_ContentPlaceHolder1_TabContainer1_TC1TP4_gv4_ListView_ctrl0_ctl00_RowLevelCheckBox")
		a2020box.click()
		a2014box = driver.find_element_by_id("ctl00_ContentPlaceHolder1_TabContainer1_TC1TP4_gv4_ListView_ctrl0_ctl03_RowLevelCheckBox")
		a2014box.click()
		a2012box = driver.find_element_by_id("ctl00_ContentPlaceHolder1_TabContainer1_TC1TP4_gv4_ListView_ctrl0_ctl04_RowLevelCheckBox")
		a2012box.click()
		a2016box = driver.find_element_by_id("ctl00_ContentPlaceHolder1_TabContainer1_TC1TP4_gv4_ListView_ctrl0_ctl02_RowLevelCheckBox")
		a2016box.click()

		time.sleep(1)

		search_me = driver.find_element_by_id("ctl00_ContentPlaceHolder1_TabContainer1_TC1TP4_Button5")
		search_me.click()

		time.sleep(2)

		table_data = driver.find_element_by_id("ctl00_ContentPlaceHolder1_TabContainer1_TC1TP4_GridView4")

		trs = table_data.find_elements_by_tag_name("tr")

		tds = []


		
		"""
		0: #
		1: name
		2: position
		3: city
		4: state
		5: zip
		6: to whom
		7: party
		8: type irrelevant
		9: date
		10: amount
		"""

		#donor_history = []
		tds_text = []

		for tr in trs:
			tds = tr.find_elements_by_tag_name("td")

			for td in tds:
				tds_text.append(td.text)
				#print("TABLE DATA TEXT: " + td.text)

			#donor_history.append(tds)
		#print("sub test: " + donor_history[0][0].text + ", " + donor_history[0][5].text)
		#print("donor_history: " + str(len(donor_history)))
		#print("tds_text test" + tds_text[4])

		year_dict = {
			"2012": 0,
			"2013": 1,
			"2014": 2,
			"2015": 3,
			"2016": 4,
			"2017": 5,
			"2018": 6
		}

		inv_year_dict = {v: k for k, v in year_dict.items()}

		#2012=0, 2013=1, 2014=2, 2015=3, 2016=4, 2017=5, 2018=6
		yearly_donations_total = [0, 0, 0, 0, 0, 0, 0]
		yearly_donations_dem = [0, 0, 0, 0, 0, 0, 0]
		percent_dem = [0, 0, 0, 0, 0, 0, 0]

		index = 0
		t_year = 0
		t_amount = 0


		for entry in tds_text:
			if "Page Total" in entry:
				break
			if "$" in entry:
				t_amount = int(entry.replace("$", "").replace(",", ""))
				last_four = tds_text[index-1][-4:]
				if "2010" in last_four or "2011" in last_four:
					last_four = "2012"
				t_year = year_dict.get(last_four)
				yearly_donations_total[t_year] = yearly_donations_total[t_year] + t_amount

				if "D" in tds_text[index - 3] or "Democrat" in tds_text[index-4] or "ActBlue" in tds_text[index-4]:
					#print("DEM TRIGGERED")
					yearly_donations_dem[t_year] = yearly_donations_dem[t_year] + t_amount

			index = index + 1

		for year in range(0, 7):
			if yearly_donations_total[year] != 0:
				percent_dem[year] = float(float(yearly_donations_dem[year]) / float(yearly_donations_total[year])) * 100
				percent_dem[year] = int(percent_dem[year])
			

		print("Total amount contributed in 2018: " + str(yearly_donations_total[6]))
		print("Total amount contributed to dems in 2018: " + str(yearly_donations_dem[6]))
		print("Percent contributed to dems in 2018: " + str(percent_dem[6]))


		comma_index = relevant_input[data_count][0].find(',')
		f_name = relevant_input[data_count][0][comma_index+1:].lower().strip().capitalize()
		l_name = relevant_input[data_count][0][0:comma_index].lower().strip().capitalize()

		print("Should be first name: " + f_name)





		donor_text = ""
		a_year = ""

		for x in range(0,7):
			a_year = inv_year_dict.get(x, "2XXX")
			donor_text = donor_text + "Total amount contributed in " + a_year + ": $" + str(yearly_donations_total[x]) + ".\n"
			donor_text = donor_text + "Total amount contributed to dems in " + a_year + ": $" + str(yearly_donations_dem[x])+ ".\n"
			donor_text = donor_text + "Percent contributed to dems in " + a_year + ": " + str(percent_dem[x]) + "%.\n"

		all_don_t.append(yearly_donations_total.copy())
		all_don_d.append(yearly_donations_dem.copy())
		p_dem.append(percent_dem.copy())
		f_names.append(f_name)
		l_names.append(l_name)
		donor_texts.append(donor_text)


		print("Profile has been searched!")
		data_count = data_count + 1

	print("ALL PROFILES HAVE BEEN SEARCHED!")


def enter_into_spreadsheet():
	counter = 0

	with open('found_data.csv', 'w+', newline = "") as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(['First Name', 'Last Name', 'Phone Number', 'Email', 'City', 'State', 'Bio', 'Donor History', 'Other'])
		while counter < len(relevant_input):
			writer.writerow([f_names[counter], l_names[counter], 'X Phone Number', 'X Email', relevant_input[counter][2].lower().capitalize(), relevant_input[counter][3], 'X Bio', donor_texts[counter], 'X Other'])
			counter = counter + 1
	
	print("Spreadsheet has been created!")


def main():
	for x in range(len(f_names)):
		print("t: " + f_names[x] + ",    " + donor_texts[x])





read_button = Button(gui, text="Read the Data", command=read_raw)
read_button.pack()

search_button = Button(gui, text="Search Moneyline", command=search_moneyline)
search_button.pack()

spreadsheet_button = Button(gui, text="Enter Spreadsheet", command=enter_into_spreadsheet)
spreadsheet_button.pack()

the_button = Button(gui, text="Do The Thing", command=main)
the_button.pack()

gui.mainloop()




