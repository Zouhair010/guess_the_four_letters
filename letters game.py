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
window.iconbitmap("C:\\Users\\dell\\Desktop\\guess the four letters\\windy_icon-icons.com_67496.ico") #to change the default icon

# Load and resize a background image
background_image = Image.open("C:\\Users\\dell\\Desktop\\guess the four letters\\Gemini_Generated_Image_416cbs416cbs416c.jpg") 
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

def random_letters(size):
	start_time = datetime.today() # Start time for the game
	alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	letters = []
	while alphabet and len(letters) < size:		
		letter = random.choice(alphabet)
		alphabet.remove(letter)# Remove selected letter to avoid duplication
		letters.append(letter)
	return letters,start_time

def easyLevel():
	easy_level.grid_forget()
	medium_level.grid_forget()
	hard_level.grid_forget()
	# Restart the game by resetting key variables and UI components
	def restart_function():
		global letters,alphabet,false_position,start_time,right_positions #globalisation these variables to use them in the chick function
		right_positions = []# Reset correct position letters
		false_position = 0
		restart_button.grid_forget()# Hide the restart button
		entry_letter.grid_forget()
		check_button.grid_forget()
		easy_level.grid(row=0, column=0, pady=45,padx=(53,0))
		medium_level.grid(row=0, column=1, pady=45,padx=(15))
		hard_level.grid(row=0, column=2, pady=45,padx=(0,53))

	# Initialize game variable
	letters,start_time = random_letters(2)
	
	right_positions = [] # Holds letters in correct positions
	# Check function to evaluate the player's guess
	def check():
		player = entry_letter.get() # Get letters entered by the player
		if len(player) < 2: # Check if less than 2 letters are entered
			messagebox.showerror("error",'you should enter two letters, but you give less than two!')
			entry_letter.delete('0', 'end')
			return
		
		elif len(player) > 2: #didecte if the letters given by the player more than the recquired letters
			messagebox.showerror("error",'you should enter two letters, but you give more than two!')		
			entry_letter.delete('0', 'end')
			return
		
		elif list(player) == letters: # Check if player guessed all letters correctly
			end_time = datetime.today() #the end time 
			scour = (end_time-start_time).total_seconds() #Calculate time taken

			headers = ['easy','medium','hard']
			file_path = 'C:\\Users\\dell\\Desktop\\\highScour.csv' 
			# Check if high score file exists, if not, create it with headers   
			if not os.path.exists(file_path):
				with open(file_path, 'w', newline='') as highScour:
					writer = csv.DictWriter(highScour, fieldnames=headers)
					writer.writeheader()
				with open(file_path, 'a+', newline='') as highScour:
					writer = csv.DictWriter(highScour, fieldnames=headers)
					writer.writerow({'easy': 'inf','medium': 'inf', 'hard': 'inf'})
			# Read existing scores to determine if the player has a new high score
			with open(file_path, 'r') as highScour:
				reader = csv.DictReader(highScour)
				scours = list(reader)
			scours = [float(scour['easy']) for scour in scours]
			highScour = min(scours,default=float('inf'))

			# Check if the player set a new high score
			if highScour > (end_time-start_time).total_seconds():
				messagebox.showinfo("",f"congratulation! you've broken the record for finding all four letters in {scour} s")		
				entry_letter.delete('0', 'end')	
				check_button.place_forget()
				restart_button.grid(row=2, column=2, pady=4,padx=(105,0))
				with open(file_path, 'a+', newline='') as highScour:
					writer = csv.DictWriter(highScour, fieldnames=headers)
					writer.writerow({'easy': scour,'medium': 'inf', 'hard': 'inf'})
				return

			# Congratulate the player on completing the game
			messagebox.showinfo("",f'great! you found the two letters in {scour} s') 	#congrat the player and show the duration of playing
			entry_letter.delete('0', 'end')
			check_button.place_forget()
			restart_button.grid(row=2, column=2, pady=4,padx=(105,0))
			return
		false_position = 0 # Counter for letters in incorrect positions
		for i in range(2):
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
	entry_letter.insert(0,'               insert two letters')
	entry_letter.bind("<FocusIn>", lambda e:on_click(entry_letter))
	entry_letter.grid(row=0, column=2, sticky='nsew', padx=(100,0), pady=(23, 0))
	# Buttons to check answer and restart the game
	check_button = tk.Button(canvas,text='check',bg='cyan',font=('Arial',10,'bold'),command=check,compound=tk.LEFT,width='77',image=photo4)
	check_button.grid(row=1, column=2, pady=4,padx=(105,0))
	restart_button = tk.Button(canvas,text='restart',bg='cyan',font=('',10,'bold'),command=restart_function,compound=tk.LEFT,width='77',image=photo5)
	restart_button.grid(row=2, column=2, pady=4,padx=(105,0))
	# Hide restart button initially
	restart_button.grid_forget()

def mediumLevel():
	easy_level.grid_forget()
	medium_level.grid_forget()
	hard_level.grid_forget()
	# Restart the game by resetting key variables and UI components
	def restart_function():
		global letters,alphabet,false_position,start_time,right_positions #globalisation these variables to use them in the chick function
		right_positions = []# Reset correct position letters
		false_position = 0
		restart_button.grid_forget()# Hide the restart button
		entry_letter.grid_forget()
		check_button.grid_forget()
		easy_level.grid(row=0, column=0, pady=45,padx=(53,0))
		medium_level.grid(row=0, column=1, pady=45,padx=(15))
		hard_level.grid(row=0, column=2, pady=45,padx=(0,53))
	# Initialize game variable
	letters,start_time = random_letters(4)
	
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

			headers = ['easy','medium','hard']
			file_path = 'C:\\Users\\dell\\Desktop\\\highScour.csv' 
			# Check if high score file exists, if not, create it with headers   
			if not os.path.exists(file_path):
				with open(file_path, 'w', newline='') as highScour:
					writer = csv.DictWriter(highScour, fieldnames=headers)
					writer.writeheader()
				with open(file_path, 'a+', newline='') as highScour:
					writer = csv.DictWriter(highScour, fieldnames=headers)
					writer.writerow({'easy': 'inf','medium': 'inf', 'hard': 'inf'})
			# Read existing scores to determine if the player has a new high score
			with open(file_path, 'r') as highScour:
				reader = csv.DictReader(highScour)
				scours = list(reader)
			scours = [float(scour['medium']) for scour in scours ]
			highScour = min(scours,default=float('inf'))
			# Check if the player set a new high score
			if highScour > (end_time-start_time).total_seconds():
				messagebox.showinfo("",f"congratulation! you've broken the record for finding all four letters in {scour} s")		
				entry_letter.delete('0', 'end')	
				check_button.place_forget()
				restart_button.grid(row=2, column=2, pady=4,padx=(105,0))
				with open(file_path, 'a+', newline='') as highScour:
					writer = csv.DictWriter(highScour, fieldnames=headers)
					writer.writerow({'easy': 'inf','medium': scour, 'hard': 'inf'})
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
	check_button = tk.Button(canvas,text='check',bg='cyan',font=('Arial',10,'bold'),command=check,compound=tk.LEFT,width='77',image=photo4)
	check_button.grid(row=1, column=2, pady=4,padx=(105,0))
	restart_button = tk.Button(canvas,text='restart',bg='cyan',font=('',10,'bold'),command=restart_function,compound=tk.LEFT,width='77',image=photo5)
	restart_button.grid(row=2, column=2, pady=4,padx=(105,0))
	# Hide restart button initially
	restart_button.grid_forget()

def hardLevel():
	easy_level.grid_forget()
	medium_level.grid_forget()
	hard_level.grid_forget()
	# Restart the game by resetting key variables and UI components
	def restart_function():
		global letters,alphabet,false_position,start_time,right_positions #globalisation these variables to use them in the chick function
		right_positions = []# Reset correct position letters
		false_position = 0
		restart_button.grid_forget()# Hide the restart button
		entry_letter.grid_forget()
		check_button.grid_forget()
		easy_level.grid(row=0, column=0, pady=45,padx=(53,0))
		medium_level.grid(row=0, column=1, pady=45,padx=(15))
		hard_level.grid(row=0, column=2, pady=45,padx=(0,53))
	# Initialize game variable
	letters,start_time = random_letters(8)
	
	right_positions = [] # Holds letters in correct positions
	# Check function to evaluate the player's guess
	def check():
		player = entry_letter.get() # Get letters entered by the player
		if len(player) < 8: # Check if less than 8 letters are entered
			messagebox.showerror("error",'you should enter eight letters, but you give less than eight!')
			entry_letter.delete('0', 'end')
			return
		
		elif len(player) > 8: #didecte if the letters given by the player more than the recquired letters
			messagebox.showerror("error",'you should enter eight letters, but you give more than eight!')		
			entry_letter.delete('0', 'end')
			return
		
		elif list(player) == letters: # Check if player guessed all letters correctly
			end_time = datetime.today() #the end time 
			scour = (end_time-start_time).total_seconds() #Calculate time taken

			headers = ['easy','medium','hard']
			file_path = 'C:\\Users\\dell\\Desktop\\\highScour.csv' 
			# Check if high score file exists, if not, create it with headers   
			if not os.path.exists(file_path):
				with open(file_path, 'w', newline='') as highScour:
					writer = csv.DictWriter(highScour, fieldnames=headers)
					writer.writeheader()
				with open(file_path, 'a+', newline='') as highScour:
					writer = csv.DictWriter(highScour, fieldnames=headers)
					writer.writerow({'easy': 'inf','medium': 'inf', 'hard': 'inf'})
			# Read existing scores to determine if the player has a new high score
			with open(file_path, 'r') as highScour:
				reader = csv.DictReader(highScour)
				scours = list(reader)
			scours = [float(scour['hard']) for scour in scours ]
			highScour = min(scours,default=float('inf'))
			# Check if the player set a new high score
			if highScour > (end_time-start_time).total_seconds():
				messagebox.showinfo("",f"congratulation! you've broken the record for finding all four letters in {scour} s")		
				entry_letter.delete('0', 'end')	
				check_button.place_forget()
				restart_button.grid(row=2, column=2, pady=4,padx=(105,0))
				with open(file_path, 'a+', newline='') as highScour:
					writer = csv.DictWriter(highScour, fieldnames=headers)
					writer.writerow({'easy': 'inf','medium': 'inf', 'hard': scour})
				return
			
			# Congratulate the player on completing the game
			messagebox.showinfo("",f'great! you found the eight letters in {scour} s') 	#congrat the player and show the duration of playing
			entry_letter.delete('0', 'end')
			check_button.place_forget()
			restart_button.grid(row=2, column=2, pady=4,padx=(105,0))
			return
		false_position = 0 # Counter for letters in incorrect positions
		for i in range(8):
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
	entry_letter.insert(0,'               insert eight letters')
	entry_letter.bind("<FocusIn>", lambda e:on_click(entry_letter))
	entry_letter.grid(row=0, column=2, sticky='nsew', padx=(100,0), pady=(23, 0))
	# Buttons to check answer and restart the game
	check_button = tk.Button(canvas,text='check',bg='cyan',font=('Arial',10,'bold'),command=check,compound=tk.LEFT,width='77',image=photo4)
	check_button.grid(row=1, column=2, pady=4,padx=(105,0))
	restart_button = tk.Button(canvas,text='restart',bg='cyan',font=('',10,'bold'),command=restart_function,compound=tk.LEFT,width='77',image=photo5)
	restart_button.grid(row=2, column=2, pady=4,padx=(105,0))
	# Hide restart button initially
	restart_button.grid_forget()

# Load and resize the images for the buttons
image1 = Image.open("C:\\Users\\dell\\Desktop\\guess the four letters\\speedometer_slow_icon_136177.ico").resize((20, 18))
photo1 = ImageTk.PhotoImage(image1)
image2 = Image.open("C:\\Users\\dell\\Desktop\\guess the four letters\\speedometer_medium_icon_137158.ico").resize((20, 18))
photo2 = ImageTk.PhotoImage(image2)
image3 = Image.open("C:\\Users\\dell\\Desktop\\guess the four letters\\speedometer_icon_137157.ico").resize((20, 18))
photo3 = ImageTk.PhotoImage(image3)
image4 = Image.open("C:\\Users\\dell\\Desktop\\guess the four letters\\1492790860-8check_84164.ico").resize((20, 18))
photo4 = ImageTk.PhotoImage(image4)
image5 = Image.open("C:\\Users\\dell\\Desktop\\guess the four letters\\4213447-arrow-load-loading-refresh-reload-restart-sync_115423.ico").resize((20, 18))
photo5 = ImageTk.PhotoImage(image5)

# Create the "Easy" button with a green background and associated image
easy_level = tk.Button(canvas,bg='green' ,text="easy",command=easyLevel  # Function to execute when the button is clicked
					   ,font=('Arial',10,'bold'),compound=tk.LEFT # Position of the image relative to the text
					   ,width='77',image=photo1) 
# Position the button on the grid
easy_level.grid(row=0, column=0, pady=45,padx=(53,0))

# Create the "Medium" button with a yellow background and associated image
medium_level = tk.Button(canvas,bg='yellow' ,text="medium",command=mediumLevel  # Function to execute when the button is clicked
						 ,font=('Arial',10,'bold'),compound=tk.LEFT # Position of the image relative to the text
						 ,width='77',image=photo2)
# Position the button on the grid
medium_level.grid(row=0, column=1, pady=45,padx=(15))

# Create the "Hard" button with a red background and associated image
hard_level = tk.Button(canvas,bg='red', text="hard",command=hardLevel  # Function to execute when the button is clicked
					   ,font=('Arial',10,'bold'),compound=tk.LEFT # Position of the image relative to the text
					   ,width='77',image=photo3)
# Position the button on the grid
hard_level.grid(row=0, column=2, pady=45,padx=(0,53))

# Start the main event loop to run the application
window.mainloop()