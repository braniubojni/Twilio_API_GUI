# -*- coding: utf-8 -*-

from tkinter import filedialog,messagebox
from tkinter import *
from tkinter.ttk import *
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import csv
from phonenumbers import is_valid_number, parse

# To make this source code to binary you need pyinstaller !!! "pip install pyinstaller"
# Here an example of command pyinstaller --onefile --windowed yourFileName.py

# Functions

def smsValidation():
	'''
	This function first check if you fill text and to field, 
	then it checks only text and only to field also it check for correct number.
	If everything okay he will send your data to Twilio and disable button to not click twice
	'''
	if textFld.get("1.0", END) == '\n' and not toFld.get():
		return messagebox.showerror('Error','Fill "to" field, also text field')
	elif textFld.get("1.0", END) == '\n':
		return messagebox.showerror('Error','Please fill text field, it is body of your message!!!')
	elif not toFld.get():
		return messagebox.showerror('Error','Please fill "to" field or upload numbers with csv file!!!')
	elif not countryValidation(radioVar.get()):
		return messagebox.showinfo('Notification','Please check to what country you want to sent the sms!!!')
	else:
		response = checkIrNum(toFld.get()[-10:]) if ShowChoice() == '1' else checkIqNum(toFld.get()[-10:]) if ShowChoice() == '2' else checkTuNum(toFld.get()[-10:])
		return twilioAPI(response, textFld.get("1.0", END)) if response else messagebox.showerror('Error','Your provided number is incorrect!!!')


def countryValidation(country):
	''' Checks which country you've choose if nothing it will return False '''
	return messagebox.showinfo('FYI', f"You have choose {'Farsi' if country == '1' else 'Kurdish' if country == '2' else 'Turkey'}") if country else False

def twilioAPI(number, bodyText):
	'''This is default function that was created from twilio team, do not touch'''
	btn.config(state=DISABLED)
	account_sid = 'Put your own account sid' 
	auth_token = 'Put your own auth token' 
	client = Client(account_sid, auth_token) 
	try:
		message = client.messages.create(  
								messaging_service_sid='Don\'t forget about msg service',
								body=bodyText,     
								to=number 
							)
	except TwilioRestException as e:
		print(e)


def clearFun():
	'''Just clears all fields'''
	for field in [toFld, textFld]:
		field.delete(0, END) if field != textFld else textFld.delete('1.0', END) 
		
# buttons activation part !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def activateBtn():
	''' This function disables and enables button '''
	if btnVariable.get() == 1:          
		btn.config(state=NORMAL)
	elif btnVariable.get() == 0:        
		btn.config(state=DISABLED)

def activateBtn2():
	''' This function disables and enables button '''
	if btnVariable2.get() == 1:          
		btnUpload.config(state=NORMAL)
	elif btnVariable2.get() == 0:        
		btnUpload.config(state=DISABLED)



# buttons activation part !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def checkTuNum(num):
	''' Function need to check the exact country that need to be checked '''
	return is_valid_number(parse(f'+90{num}', 'TR')) and f'+90{num}'

def checkIrNum(num):
	''' Function need to check the exact country that need to be checked '''
	return is_valid_number(parse(f'+98{num}', 'IR')) and f'+98{num}'

def checkIqNum(num):
	''' Function need to check the exact country that need to be checked '''
	return is_valid_number(parse(f'+964{num}', 'IQ')) and f'+964{num}'

def showData(validNums:set, invalidNums:list):
	'''
	Function shows how many recipients you have and if you have some invalid numbers
	then it will ask you to export it(by default should be no)
	'''
	if not len(invalidNums):
		return messagebox.showinfo('Notification',f'You have {len(validNums)} recipients')
	else:
		if messagebox.askyesnocancel('Notification',f"You have {len(validNums)} recipients and {len(invalidNums)} invalid numbers, type 'Yes' if you wish to import them!!!", default='no'):
			with open(r'incorrectNumbers.csv', 'w') as file:
				writer = csv.writer(file)
				for num in invalidNums:
					writer.writerow([num])
	

def UploadAction():
	''' 
	function need to be sure that you want to send bulk message not only one message
	1) it will ask you to remove from "to" field everything
	2) and he will need first to have sms content, because without that you can't continue
	3) also user need to provide which country he is going to send
	4) when provide nothing or non csv file it will show you an error 
	'''
	if toFld.get():
		return messagebox.showinfo('Notification','If you want to upload csv file\nPlease remove from "to" field number')
	if textFld.get("1.0", END) == '\n':
		return messagebox.showerror('Error','Please first write sms that you are going to sent')
	if not countryValidation(radioVar.get()):
		return messagebox.showerror('Error','You have to choose which country you need to sent')
	filename = filedialog.askopenfilename()
	btnUpload.config(state=DISABLED)
	if filename[-3:] != 'csv':
		return messagebox.showerror('Error','Sorry, your selected file is not csv file')
	return checkNumbers(filename)

def checkNumbers(arg):
	'''
	Function reads csv file and creates a valid numbers set and invalid numbers list
	Returns valid numbers list
	'''
	validNumbers = set()
	invalidNumbers = []
	with open(arg) as f:
		reader = csv.reader(f)
		func = checkIrNum if ShowChoice() == '1' else checkIqNum if ShowChoice() == '2' else checkTuNum
		for num in reader:
			try:
				valid = func(num[0][-10:])
				if valid:
					validNumbers.add(valid)
				else:
					invalidNumbers.append(num[0])
			except:
				print('Something went wrong')
	showData(validNumbers,invalidNumbers) 
	return sendOneByOne(validNumbers)

def sendOneByOne(numbers):
	'''
	The last function that asks to sent to that recipients,
	REMEMBER if process started you can't stop it,
	when it will over it will show how many is he sent by twilio API
	'''
	btn.config(state=DISABLED)
	count = 0
	ask = messagebox.askyesnocancel('Notification',f"Do you want to send sms to provided numbers?", default='yes')
	if ask:
		for number in numbers:
			twilioAPI(number, textFld.get("1.0", END))
			count += 1
		messagebox.showinfo('Notification',f'You have sent sms to {count} recipients')
		
def ShowChoice():
	''' Function just returns your chosen country option '''
	return radioVar.get()

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!	

window = Tk()

# Variables & Objects
btnVariable = IntVar()
btnVariable2 = IntVar()
textVariable = StringVar()
btnStyle = Style()
radioVar = StringVar()



# Style place
btnStyle.configure('TButton',
                  foreground='black',
				  background='#9933ff')




window.title("Bulk sms program")
window.geometry("750x400")
window.resizable(width=False, height=False)


# Buttons
btn=Button(window, text="Send sms", width=30, state=DISABLED, command=smsValidation)
btn.place(x=450, y=100)
btnCheck = Checkbutton(window, variable=btnVariable, command=activateBtn)
btnCheck.pack()
btnCheck.place(x=650, y=99)

clearbtn=Button(window, text="Clear fields", state=NORMAL, width=20, command=clearFun)
clearbtn.place(x=490, y=200)

toLbl=Label(window, text="To", font=("Ubuntu", 12))
toLbl.place(x=54, y=80)
toFld=Combobox(window, width=50, values = ['09131130418','+989131664707'])
toFld.place(x=80, y=80)

textLbl=Label(window, text="Text", font=("Ubuntu", 12))
textLbl.place(x=43, y=112)
textFld=Text(window)
textFld.place(x=80, y=110, width=323, height=180)



btnUpload = Button(window, text="Upload", state=DISABLED, command=UploadAction)
btnUpload.place(x=515, y=150)

btnUploadCheck = Checkbutton(window, variable=btnVariable2, command=activateBtn2)
btnUploadCheck.pack()
btnUploadCheck.place(x=610, y=150)



radioFarsi=Radiobutton(window, variable = radioVar, value=1, command=ShowChoice)
radioFarsi.place(x=450, y=275)
farsiLbl=Label(window, text="Farsi", font=("Ubuntu", 12))
farsiLbl.place(x=450, y=300)

radioKurdish=Radiobutton(window, variable = radioVar, value=2, command=ShowChoice)
radioKurdish.place(x=550, y=275)
kurdishLbl=Label(window, text="Kurdish", font=("Ubuntu", 12))
kurdishLbl.place(x=550, y=300)

radioTurkey=Radiobutton(window, variable = radioVar, value=3, command=ShowChoice)
radioTurkey.place(x=650, y=275)
turkeyLbl=Label(window, text="turkey", font=("Ubuntu", 12))
turkeyLbl.place(x=650, y=300)





window.mainloop()
