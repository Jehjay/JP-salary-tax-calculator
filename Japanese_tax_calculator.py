# importing modules 
import re
import datetime
from tabulate import tabulate
from texttable import Texttable
from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors

raw_salary_entry = input("Enter the Japenese Yen Annual salary equivalent IN FULL: ")

if not type(raw_salary_entry) is str:
  raise TypeError("Your input is NOT valid, Please enter a Valid input - empty space, non-numeric characters or NO input are not valid")
  
else:
	# create a regular expression to handle the following cases:
	# check if the raw_salary_entry starts with non numeric character and remove it e.g. JPY 3000 -> 3000
	# check if raw_salary_entry ends with non numeric character and remove it e.g. 3000 Japanese Yen only -> 3000
	# check if raw_salary_entry has a space and remove it e.g 30 000 -> 30000
	# check if raw_salary_entry has a comma and remove it e.g 30,000 -> 30000
	# check if raw_salary_entry has a special character such as !;:? and remove it

	numeric_salary = re.sub("[^\d.]+", "", raw_salary_entry)

	#remove all characters after the last digit at the end e.g. 3000. and remove it
	numeric_salary = re.sub(r'(\d)\D+$', r'\1', numeric_salary)

	try:
		salary = float(numeric_salary)
	except ValueError:
		print("Your input is NOT valid")
	else:
		
		def japan_tax(salary):
			salary = salary
			gross_salary = (round(salary,5))

			def national_tax(salary):
				if(salary<1950000):
					nat_tax = salary * 0.05
					nat_tax = round(nat_tax,5)
				
				elif(1950000<=salary<=3300000):
					nat_tax = (salary-97500) * 0.1
					nat_tax = round(nat_tax,5)
		
				elif(3300001<=salary<=6950000):
					nat_tax = (salary-427500) * 0.2
					nat_tax = round(nat_tax,5)
		
				elif(6950001<=salary<=9000000):
					nat_tax = (salary-636000) * 0.23
					nat_tax = round(nat_tax,5)
		
				elif(9000001<=salary<=18000000):
					nat_tax = (salary-1536000) * 0.33
					nat_tax = round(nat_tax,5)
		
				elif(18000001<=salary<=40000000):
					nat_tax = (salary-2796000) * 0.4
					nat_tax = round(nat_tax,5)
		
				elif(40000001<salary):
					nat_tax = (salary-4796000) * 0.45	
					nat_tax = round(nat_tax,5)

				return nat_tax
		
			nat_tax = national_tax(salary)
		
			def prefectural_tax(salary):
				pref_tax = salary * 0.04
				pref_tax = round(pref_tax,5)
			
				return pref_tax

			pref_tax = prefectural_tax(salary)

			def municipal_tax(salary):
				mun_tax = salary * 0.06
				mun_tax = round(mun_tax,5)

				return mun_tax

			mun_tax = municipal_tax(salary)
	
			#jap_annual_tax = national_tax[0]+Prefectural_tax[0]+municipal_tax[0]
			#jap_annual_salary = national_tax[1]+Prefectural_tax[1]+municipal_tax[1]

			jap_annual_tax = nat_tax+pref_tax+mun_tax
			jap_annual_salary = salary-jap_annual_tax
			
			jap_month_tax = jap_annual_tax/12
			jap_month_salary = jap_annual_salary/12

			answer = "Your Annual Gross Salary is" + " JPY " + str(gross_salary)+"\n"+"\n"\
					"National Annual Income Tax is " + str(nat_tax) + "\n"\
					"Prefectural Annual Income Tax @ 4% is " + str(pref_tax) + "\n"\
					"Municipal Annual Income Tax @ 6% is " + str(mun_tax) + "\n"+"\n"\
					"Your Annual Total Tax Contribution is" + " JPY " + str(jap_annual_tax)+"\n"+"\n"\
					"Your Annual Net Salary is" + " JPY " + str(jap_annual_salary)+"\n"+"\n"\
					"Your Monthly Total Tax Contribution is" + " JPY " + str(jap_month_tax)+"\n"+"\n"\
					"Your Monthly Net Salary is" + " JPY " + str(jap_month_salary)

			print(answer + "\n")
			
			# TIME STAMP
			# using datetime module
			
			# ct stores current time
			ct = datetime.datetime.now()
			#print("Current Time: %s"%(ct))

			# ts store timestamp of current time
			ts = ct.timestamp()
			#print("Timestamp: %s"%(ts))


			# PRINT A TABLE FOR RESULTS
			# Sample data: list of lists
			data = [
			    [gross_salary, nat_tax, pref_tax, mun_tax, jap_annual_tax, jap_annual_salary, jap_month_tax, jap_month_salary]
			]
			headers = ["Annual Gross Salary", " National Tax", "Prefecture Tax", "Municipal Tax", "Annual Net Salary", "Total Monthly Tax", "Monthly Net Salary"]
			# Customizing table appearance
			table = tabulate(
			    data,
			    headers=headers,
			    tablefmt="fancy_grid",
			    numalign="right",
			    stralign="center",
			    maxcolwidths=[10, 10, 10, 10, 10, 10, 10, 10]  # Set maximum width for the Description column
			)

			#print(table)

			# Displaying sales data using the 'html' format
			table_html = tabulate(data, headers=headers, tablefmt="HTML")
			#print(table_html)

			# PRINT A TABLE FOR RESULTS
			data = [gross_salary, nat_tax, pref_tax, mun_tax, jap_annual_tax, jap_annual_salary, jap_month_tax, jap_month_salary]
			t = Texttable()
			t.add_rows([["Annual Gross Salary", " National Tax", "Prefecture Tax", "Municipal Tax", "Total Annual Tax", "Annual Net Salary","Total Monthly Tax", "Monthly Net Salary"], data])
			print(t.draw())


			#GENERATE PDF
			# initializing variables with values 
			fileName = 'JP_salary_tax_invoice.pdf'
			documentTitle = 'salary_tax_invoice'
			title = 'Total salary Tax Contributions'
			subTitle = 'Tax payer\'s salary taxes due'
			textLines = [ 
				"Tax payer's Annual Gross Salary is: JPY " + str(gross_salary),
				" " ,
				"National Annual Income Tax is " + str(nat_tax),
				"Prefecture Annual Income Tax @ 4% is " + str(pref_tax),
				"Municipal Annual Income Tax @ 6% is " + str(mun_tax),
				" " ,
				"Tax payer's Total Annual Tax Contribution is: JPY " + str(jap_annual_tax),
				" ",
				"Tax payer's Annual Net Salary is: JPY " + str(jap_annual_salary),
				" ",
				"Tax payer's Total Monthly Tax Contribution is: JPY " + str(jap_month_tax),
				" ",
				"Tax payer's Monthly Net Salary is: JPY " + str(jap_month_salary),
				" ", " ", " ", " ", " ",
				"Current Time: " + str(ct),
				"Timestamp: " + str(ts)
			] 
			image = 'Japan.png'

			# creating a pdf object 
			pdf = canvas.Canvas(fileName) 

			# setting the title of the document 
			pdf.setTitle(documentTitle) 

			# registering a external font in python 
			pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
			pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
			pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
			pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

			# creating the title by setting it's font 
			# and putting it on the canvas 
			pdf.setFont('Vera', 32) 
			pdf.drawCentredString(300, 570, title) 

			# creating the subtitle by setting it's font, 
			# colour and putting it on the canvas 
			pdf.setFillColorRGB(0, 0, 255) 
			pdf.setFont("Courier-Bold", 24) 
			pdf.drawCentredString(290, 520, subTitle) 

			# drawing a line 
			pdf.line(30, 510, 550, 510) 

			# creating a multiline text using 
			# textline and for loop 
			text = pdf.beginText(20, 400) 
			text.setFont("Courier", 15) 
			text.setFillColor(colors.black) 
			for line in textLines: 
				text.textLine(line) 
			pdf.drawText(text) 

			# drawing a image at the 
			# specified (x.y) position 
			pdf.drawInlineImage(image, 130, 640) 

			# saving the pdf 
			pdf.save()
	
			return answer

		japan_tax(salary)

