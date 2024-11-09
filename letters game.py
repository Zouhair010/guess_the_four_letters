import random
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk
import csv
import os

# Create a main window for the game with a specified background color, title, size, and icon
window = tk.Tk()
window.configure(bg='#ccff9c')
window.title('geuss the four letters')
window.geometry('400x200')
window.resizable(False, False)

# Set a custom icon for the window
window.iconbitmap("C:\\Users\\dell\\Desktop\\mygame\\windy_icon-icons.com_67496.ico") #to change the default icon

# Load and resize a background image
background_image = Image.open("C:\\Users\\dell\\Desktop\\mygame\\Gemini_Generated_Image_416cbs416cbs416c.jpg") 
background_image = background_image.resize((400, 200), Image.LANCZOS)  
background_photo = ImageTk.PhotoImage(background_image)

# Create a canvas to hold the background image
canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Function to clear default text in entry when clicked and change text color to black
def on_click(tool):
    tool.delete(0,'end')
    tool.config(fg="black")

# Generate 4 unique random letters and start a timer
def random_letters():
	start_time = datetime.today() # Start time for the game
	alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	letters = []
	while alphabet and len(letters) < 4:		
		letter = random.choice(alphabet)
		alphabet.remove(letter)# Remove selected letter to avoid duplication
		letters.append(letter)
	return letters,start_time

# Restart the game by resetting key variables and UI components
def restart_function():
	global letters,alphabet,false_position,start_time,right_positions #globalisation these variables to use them in the chick function
	letters,start_time = random_letters()# Generate new letters and reset timer
	right_positions = []# Reset correct position letters
	false_position = 0
	restart_button.grid_forget()# Hide the restart button
	check_button.grid(row=1, column=2, pady=4,padx=(105,0))# Show the check button

# Initialize game variables
letters,start_time = random_letters()
right_positions = [] # Holds letters in correct positions

# Check function to evaluate the player's guess
def check():
	player = entry_letter.get() # Get letters entered by the player
	if len(player) < 4: # Check if less than 4 letters are entered
		messagebox.showerror("error",'you should enter four letters, but you give less than four!')
		entry_letter.delete('0', 'end')
		return
	
	elif len(player) > 4: #didecte if the letters given by the player more than the recquired letters
		messagebox.showerror("error",'you should enter four letters, but you give more than four!')		
		entry_letter.delete('0', 'end')
		return
	
	elif list(player) == letters: # Check if player guessed all letters correctly
		end_time = datetime.today() #the end time 
		scour = (end_time-start_time).total_seconds() #Calculate time taken
		headers = ['scours']
		file_path = 'C:\\Users\\dell\\Desktop\\\highScour.csv' 
		# Check if high score file exists, if not, create it with headers   
		if not os.path.exists(file_path):
			with open(file_path, 'w', newline='') as highScour:
				writer = csv.DictWriter(highScour, fieldnames=headers)
				writer.writeheader()
		# Read existing scores to determine if the player has a new high score
		with open(file_path, 'r') as highScour:
			reader = csv.DictReader(highScour)
			scours = list(reader)
		scours = [float(scour['scours']) for scour in scours]
		highScour = min(scours,default=float('inf'))
		# Check if the player set a new high score
		if highScour > (end_time-start_time).total_seconds():
			messagebox.showinfo("",f"congratulation! you've broken the record for finding all four letters in {scour} s")		
			entry_letter.delete('0', 'end')	
			check_button.place_forget()
			restart_button.grid(row=2, column=2, pady=4,padx=(105,0))
			with open(file_path, 'a+', newline='') as highScour:
				writer = csv.DictWriter(highScour, fieldnames=headers)
				writer.writerow({'scours': scour})
			return
		# Congratulate the player on completing the game
		messagebox.showinfo("",f'great! you found the four letters in {scour} s') 	#congrat the player and show the duration of playing
		entry_letter.delete('0', 'end')
		check_button.place_forget()
		restart_button.grid(row=2, column=2, pady=4,padx=(105,0))
		return
	false_position = 0 # Counter for letters in incorrect positions
	for i in range(4):
		if player[i] == letters[i]: # Check if a letter is in the correct position
			right_positions.append(letters[i]) # Add to correct position set
		elif player[i] != letters[i] and player[i] in letters: # Check if letter exists but in incorrect position
			false_position += 1
	# Provide feedback based on the player's guess
	if false_position == 0 and len(right_positions) == 0:
		messagebox.showinfo("","you got no letter")
		entry_letter.delete('0', 'end')
	elif false_position == 0 and len(right_positions) > 0:
		messagebox.showinfo("",f'you got these latters in their places: {' ,'.join(right_positions)}')
		entry_letter.delete('0', 'end')
	elif false_position > 0 and len(right_positions) == 0:
		messagebox.showinfo("",f'you found {false_position} letters but not in their places')
		entry_letter.delete('0', 'end')
	else:
		messagebox.showinfo("",f'you found these latters in their places: {' ,'.join(right_positions)}\nand {false_position} letters but not in their places')
		entry_letter.delete('0', 'end')
	# Refresh the correct position letters for the next round
	del right_positions[:] 

# Entry for player input with a default prompt text
entry_letter = tk.Entry(canvas,width='30',border=1 ,relief='solid')
entry_letter.config(fg='gray') #change the color of the default text to gray
entry_letter.insert(0,'               insert four letters')
entry_letter.bind("<FocusIn>", lambda e:on_click(entry_letter))
entry_letter.grid(row=0, column=2, sticky='nsew', padx=(100,0), pady=(23, 0))

# Buttons to check answer and restart the game
check_button = tk.Button(canvas,text='check',bg='cyan',font=('Arial',10,'bold'),width='10',command=check)
check_button.grid(row=1, column=2, pady=4,padx=(105,0))
restart_button = tk.Button(canvas,text='restart',bg='cyan',font=('',10,'bold'),width='8',command=restart_function)
restart_button.grid(row=2, column=2, pady=4,padx=(105,0))

# Hide restart button initially
restart_button.grid_forget()

# Start the main event loop to run the application
window.mainloop()