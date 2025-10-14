import tkinter as tk
from tkinter import messagebox
import pygame
import time
import random
import math
import os  # Import os module for path manipulation

# Function to validate the date
def validate_date(month, day):
    try:
        month = int(month)
        day = int(day)
        if 1 <= month <= 12 and 1 <= day <= 31:
            return True
    except ValueError:
        pass
    return False

# Function to handle the Continue button click
def on_continue():
    month = month_entry.get()
    day = day_entry.get()
    if not month or not day:
        messagebox.showerror("Error", "Both fields must be filled!")
        return

    if validate_date(month, day):
        messagebox.showinfo("Success", f"Your birthday is: {month}/{day}")
        root.destroy()  # Close the Tkinter window

        # Create a new window to display the birthday cake
        cake_window = tk.Tk()
        cake_window.title("Happy Birthday!")
        cake_window.geometry("800x600")
        cake_window.configure(bg="black")

        # Play background music
        pygame.mixer.init()
        # Dynamically generate the path to the music file
        music_path = os.path.join(os.path.dirname(__file__), "happy_birthday.mp3")
        pygame.mixer.music.load(music_path)  # Ensure the file is in the same directory
        pygame.mixer.music.play(-1)  # Loop the music indefinitely

        # Clear the window and create new content
        for widget in cake_window.winfo_children():
            widget.destroy()

        # Display the birthday date
        date_label = tk.Label(cake_window, text=f"Your Birthday: {month}/{day}", font=("Silkscreen", 24), fg="white", bg="black")
        date_label.pack(pady=20)

        # Display the main message
        message_label = tk.Label(cake_window, text="🎂 HAPPY BIRTHDAY 🎂", font=("Silkscreen", 40), fg="pink", bg="black")
        message_label.pack(pady=50)

        # Display cakes on both sides
        left_cake_label = tk.Label(cake_window, text="🎂", font=("Silkscreen", 48), fg="pink", bg="black")
        left_cake_label.place(x=150, y=250)

        right_cake_label = tk.Label(cake_window, text="🎂", font=("Silkscreen", 48), fg="pink", bg="black")
        right_cake_label.place(x=550, y=250)

        # Update the window to ensure everything is displayed
        cake_window.update()

        # Create a canvas for fireworks
        canvas = tk.Canvas(cake_window, width=800, height=400, bg="black", highlightthickness=0)
        canvas.pack()

        # Add instructional text
        instruction_label = tk.Label(cake_window, text="Try clicking or dragging", font=("Silkscreen", 16), fg="white", bg="black")
        instruction_label.place(x=300, y=350)

        def blink_text():
            current_color = instruction_label.cget("fg")
            new_color = "black" if current_color == "white" else "white"
            instruction_label.config(fg=new_color)
            cake_window.after(500, blink_text)  # Toggle every 500ms

        blink_text()

        class ParticleSystem:
            def __init__(self, canvas):
                self.canvas = canvas
                self.particles = []

            def add_particle(self, x, y, dx, dy, size, color, lifetime):
                particle = {
                    "x": x,
                    "y": y,
                    "dx": dx,
                    "dy": dy,
                    "size": size,
                    "color": color,
                    "lifetime": lifetime,
                    "opacity": 1.0,
                    "start_time": time.time()
                }
                self.particles.append(particle)

            def update(self):
                current_time = time.time()
                self.canvas.delete("particle")
                new_particles = []

                for particle in self.particles:
                    elapsed = current_time - particle["start_time"]
                    if elapsed < particle["lifetime"]:
                        particle["x"] += particle["dx"]
                        particle["y"] += particle["dy"] + 0.1  # Gravity effect
                        particle["size"] *= 0.95  # Gradually shrink
                        particle["opacity"] -= 1 / (particle["lifetime"] * 60)  # Linear fade

                        if particle["opacity"] > 0:
                            color = particle["color"]
                            self.canvas.create_oval(
                                particle["x"] - particle["size"],
                                particle["y"] - particle["size"],
                                particle["x"] + particle["size"],
                                particle["y"] + particle["size"],
                                fill=color,
                                outline="",
                                tags="particle"
                            )
                        new_particles.append(particle)

                self.particles = new_particles
                self.canvas.after(16, self.update)  # 60 FPS

        particle_system = ParticleSystem(canvas)
        particle_system.update()

        click_start_time = None
        last_position = None
        instruction_visible = True

        def create_short_firework(x, y):
            for _ in range(20, 30):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 5)
                dx = speed * math.cos(angle)
                dy = speed * math.sin(angle)
                color = random.choice(["red", "yellow", "blue", "green", "purple"])
                particle_system.add_particle(x, y, dx, dy, random.randint(4, 6), color, random.uniform(0.8, 1.2))

        def create_layered_firework(x, y, duration):
            if duration > 0.5:
                for _ in range(30):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 5)
                    dx = speed * math.cos(angle)
                    dy = speed * math.sin(angle)
                    color = random.choice(["red", "orange", "yellow"])
                    particle_system.add_particle(x, y, dx, dy, random.randint(4, 6), color, random.uniform(0.8, 1.2))
            if duration > 1.5:
                for _ in range(50):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 5)
                    dx = speed * math.cos(angle)
                    dy = speed * math.sin(angle)
                    color = random.choice(["blue", "green", "purple"])
                    particle_system.add_particle(x, y, dx, dy, random.randint(4, 6), color, random.uniform(0.8, 1.2))
            if duration > 2.0:
                for _ in range(100):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 5)
                    dx = speed * math.cos(angle)
                    dy = speed * math.sin(angle)
                    color = random.choice(["gold", "white"])
                    particle_system.add_particle(x, y, dx, dy, random.randint(4, 6), color, random.uniform(0.8, 1.2))

        def create_trail_particles(x, y, speed):
            colors = ["blue", "purple"] if speed < 5 else ["red", "yellow"]
            for _ in range(5):
                angle = random.uniform(-math.pi / 4, math.pi / 4)
                dx = speed * math.cos(angle) + random.uniform(-1, 1)
                dy = speed * math.sin(angle) + random.uniform(-1, 1)
                particle_system.add_particle(x, y, dx, dy, random.randint(3, 5), random.choice(colors), random.uniform(0.5, 1.0))

        def on_mouse_down(event):
            nonlocal click_start_time, last_position, instruction_visible
            click_start_time = time.time()
            last_position = (event.x, event.y)

            # Hide the instruction label on first click
            if instruction_visible:
                instruction_label.place_forget()
                instruction_visible = False

        def on_mouse_up(event):
            nonlocal click_start_time
            if click_start_time:
                duration = time.time() - click_start_time
                if duration < 0.5:
                    create_short_firework(event.x, event.y)
                else:
                    create_layered_firework(event.x, event.y, duration)
                click_start_time = None

        def on_mouse_motion(event):
            nonlocal last_position
            if last_position is not None:
                x1, y1 = last_position
                x2, y2 = event.x, event.y
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

                if distance > 10:
                    speed = distance / 10
                    create_trail_particles(event.x, event.y, speed)
                    last_position = (event.x, event.y)

        # Bind mouse events
        canvas.bind("<Button-1>", on_mouse_down)
        canvas.bind("<ButtonRelease-1>", on_mouse_up)
        canvas.bind("<B1-Motion>", on_mouse_motion)

        # Add an Easter egg animation when clicking the 'HAPPY BIRTHDAY' text
        def show_cat_animation():
            cat_row = tk.Label(cake_window, text="😺😺😺😺😺😺😺😺😺😺", font=("Silkscreen", 24), fg="white", bg="black")
            cat_row.place(x=100, y=500)

        # Bind the click event to the 'HAPPY BIRTHDAY' text
        message_label.bind("<Button-1>", lambda event: show_cat_animation())

        # Ensure the window updates its content
        cake_window.update_idletasks()

        # Keep the window open
        cake_window.mainloop()
    else:
        messagebox.showerror("Error", "Invalid date! Please enter a valid date.")

# Create the main window
root = tk.Tk()
root.title("Birthday Celebration")
root.geometry("600x450")
root.configure(bg="black")

# Add a label to ask for the user's birthday
title_label = tk.Label(root, text="What is your birthday date?", font=("Silkscreen", 18), fg="white", bg="black")
title_label.pack(expand=True, pady=20)

# Replace the calendar design with a pixel art cat
cat_art = """
   /\_/\\
  ( o.o )
   > ^ <
"""
cat_label = tk.Label(root, text=cat_art, font=("Courier", 12), fg="black", bg="peachpuff", justify="center")
cat_label.pack(pady=10)

# Adjust the pixel art cat's mouth position in the animation frames
frames = [
    "   /\\_/\\\n  ( o.o )\n   >^<\n",
    "   /\\_/\\\n  ( -.- )\n   >^<\n",
    "   /\\_/\\\n  ( o.o )\n   >^<\n"
]

frame_index = 0

def animate_cat():
    global frame_index
    cat_label.config(text=frames[frame_index])
    frame_index = (frame_index + 1) % len(frames)
    root.after(500, animate_cat)  # Change frame every 500ms

# Start the animation
animate_cat()

# Create the input fields
center_frame = tk.Frame(root, bg="black")
center_frame.pack(expand=True)

month_frame = tk.Frame(center_frame, bg="black")
month_frame.pack(pady=20)
month_label = tk.Label(month_frame, text="Month:", font=("Silkscreen", 14), fg="white", bg="black")
month_label.pack(side="left", padx=5)
month_entry = tk.Entry(month_frame, font=("Silkscreen", 14), fg="black", justify="center")
month_entry.pack(side="left", padx=5)
month_entry.insert(0, "1-12")

day_frame = tk.Frame(center_frame, bg="black")
day_frame.pack(pady=20)
day_label = tk.Label(day_frame, text="Day:", font=("Silkscreen", 14), fg="white", bg="black")
day_label.pack(side="left", padx=5)
day_entry = tk.Entry(day_frame, font=("Silkscreen", 14), fg="black", justify="center")
day_entry.pack(side="left", padx=5)
day_entry.insert(0, "1-31")

# Continue button
continue_button = tk.Button(center_frame, text="Continue", font=("Silkscreen", 14), command=on_continue, state="normal")
continue_button.pack(pady=20)

# Run the main loop
root.mainloop()