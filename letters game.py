import random
import tkinter as tk
from datetime import datetime
import csv
import os

# a window
window = tk.Tk()
window.configure(bg='#ccff9c')
window.title('geuss the four letters')
# window.geometry('400x200')

# function to generat 4 random latters none duplecated
def random_letters():
	start_time = datetime.today() #start time 
	alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	letter1 = random.choice(alphabet)
	alphabet.remove(letter1)
	letter2 = random.choice(alphabet)
	alphabet.remove(letter2)
	letter3 = random.choice(alphabet)
	alphabet.remove(letter3)
	letter4 = random.choice(alphabet)
	letters = [letter1,letter2,letter3,letter4]
	alphabet.extend(letters)
	return letters,start_time
# function to restart te game and return all the variables to the first state 
def restart_function():
	global letters,alphabet,false_position,start_time,right_positions #globalisation these variables to use them in the chick function
	letters,start_time = random_letters()
	right_positions = []
	result1_lebel['text'] =''
	#print(letters)
	false_position = 0
	restart_button.grid_forget()
	check_button.grid(row=4, column=0, pady=4)

letters,start_time = random_letters()
print(letters)

right_positions = [] #set of letters that exist on their position

# function that check the positions of letters given by the player
def check():
	
	player = entry_letter.get() #letters given by the player
	if len(player) < 4: #didecte if the letters given by the player less than the recquired letters
		result1_lebel['fg'] = 'red'
		result1_lebel['text'] = 'you should enter four letters, but you give less than four!'
		return
	
	elif len(player) > 4: #didecte if the letters given by the player more than the recquired letters
		result1_lebel['fg'] = 'red'
		result1_lebel['text'] = 'you should enter four letters, but you give more than four!'
		return
	
	elif list(player) == letters: #didecte if the player got the latters
		end_time = datetime.today() #the end time 
		scour = (end_time-start_time).total_seconds()
		headers = ['scours']
		file_path = 'C:\\Users\\dell\\Desktop\\\highScour.csv'    
		if not os.path.exists(file_path):
			with open(file_path, 'w', newline='') as highScour:
				writer = csv.DictWriter(highScour, fieldnames=headers)
				writer.writeheader()
		with open(file_path, 'r') as highScour:
			reader = csv.DictReader(highScour)
			scours = list(reader)
		scours = [float(scour['scours']) for scour in scours]
		highScour = min(scours,default=float('inf'))
		if highScour > (end_time-start_time).total_seconds():
			result1_lebel['fg'] = '#34940f'
			result1_lebel['text'] = f"congratulation! you've broken the record for finding all four letters in {scour} s"
			check_button.place_forget()
			restart_button.grid(row=5, column=0, pady=4)
			with open(file_path, 'a+', newline='') as highScour:
				writer = csv.DictWriter(highScour, fieldnames=headers)
				writer.writerow({'scours': scour})
			return
		result1_lebel['fg'] = '#34940f'
		result1_lebel['text'] = f'great! you found the four letters in {scour} s' #congrat the player and show the duration of playing
		check_button.place_forget()
		restart_button.grid(row=5, column=0, pady=4)
		return

	false_position = 0 #false positions counter
	for i in range(4):
		if player[i] == letters[i]: #if the player found a letter in the right position
			right_positions.append(letters[i]) #add the letter that is in the right to the sit of letters that exist on their position
		elif player[i] != letters[i] and player[i] in letters: #if the player found a letter but in false position
			false_position += 1
	if false_position == 0 and len(right_positions) == 0:
		result1_lebel['text'] = ''
	elif false_position == 0 and len(right_positions) > 0:
		result1_lebel['fg'] = '#34940f'
		result1_lebel['text'] = f'you got these latters in their places: {' ,'.join(right_positions)}'
	elif false_position > 0 and len(right_positions) == 0:
		result1_lebel['fg'] = '#FF5733'
		result1_lebel['text'] = f'you found {false_position} letters but not in their places'
	else:
		result1_lebel['text'] = f'you found these latters in their places: {' ,'.join(right_positions)}\nand {false_position} letters but not in their places'
		result1_lebel['fg'] = '#34940f'
		
	del right_positions[:] #refrish the letters in the right position


window.resizable(False,False)
frame = tk.Frame(window)
frame.configure(bg='#c7ff91',border=1 ,relief='solid', pady=100 ,padx=100, height=200)
frame.pack()

# label that tells whate the game about
result0_lebel = tk.Label(frame,text='insert four letters',bg='#33af46',font=('Arial',20,'bold'),fg='gold' ,border=1 ,relief='solid' ,padx=10)
result0_lebel.grid(row=0, column=0, padx=10)
# label of results: for the exist letters but not in the right position
result1_lebel = tk.Label(frame,text='',bg='#c7ff91',font=('Arial',10,'bold'), fg='black')
result1_lebel.grid(row=1, column=0)
# entry of the player
entry_letter = tk.Entry(frame,width='30',border=1 ,relief='solid')
entry_letter.grid(row=3, column=0)
# buttons
check_button = tk.Button(frame,text='check',bg='#6dd10f',font=('Arial',10,'bold'),width='10',command=check)
check_button.grid(row=4, column=0, pady=4)
restart_button = tk.Button(frame,text='restart',bg='#6dd10f',font=('',10,'bold'),width='10',command=restart_function)
restart_button.grid(row=5, column=0, pady=4)

restart_button.grid_forget()

window.mainloop()