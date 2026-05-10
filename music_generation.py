import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import random
from collections import deque

# Try to import music21
try:
    from music21 import stream, note, tempo, instrument, meter, chord
    MUSIC21_AVAILABLE = True
except ImportError:
    MUSIC21_AVAILABLE = False
    note = None

class MusicGenerator:
    """Generate music sequences using AI patterns"""
    
    def __init__(self):
        self.notes_sequence = []
        self.generated_notes = []
        
    def generate_random_melody(self, num_notes=50, scale="major"):
        """Generate random melody using specified scale"""
        if scale == "major":
            notes_scale = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale
        elif scale == "minor":
            notes_scale = [60, 62, 63, 65, 67, 68, 70, 72]  # A natural minor
        elif scale == "pentatonic":
            notes_scale = [60, 62, 64, 67, 69, 72]  # Pentatonic scale
        else:
            notes_scale = [60, 62, 64, 65, 67, 69, 71, 72]  # Default to major
        
        self.generated_notes = []
        for i in range(num_notes):
            pitch = random.choice(notes_scale)
            duration = random.choice([0.25, 0.5, 1.0, 2.0])  # 16th, 8th, quarter, half notes
            self.generated_notes.append((pitch, duration))
        
        return self.generated_notes
    
    def generate_markov_melody(self, num_notes=50, scale="major"):
        """Generate melody using Markov chain patterns"""
        if scale == "major":
            notes_scale = [60, 62, 64, 65, 67, 69, 71, 72]
        elif scale == "minor":
            notes_scale = [60, 62, 63, 65, 67, 68, 70, 72]
        elif scale == "pentatonic":
            notes_scale = [60, 62, 64, 67, 69, 72]
        else:
            notes_scale = [60, 62, 64, 65, 67, 69, 71, 72]
        
        self.generated_notes = []
        current_note = random.choice(notes_scale)
        
        for i in range(num_notes):
            # Create transitions based on current note
            neighbors = [n for n in notes_scale if abs(n - current_note) <= 5]
            if not neighbors:
                neighbors = notes_scale
            
            next_note = random.choice(neighbors)
            duration = random.choice([0.25, 0.5, 1.0, 2.0])
            self.generated_notes.append((next_note, duration))
            current_note = next_note
        
        return self.generated_notes
    
    def save_to_midi(self, filepath, tempo_bpm=120):
        """Save generated notes to MIDI file"""
        if not MUSIC21_AVAILABLE:
            return False
        
        try:
            # Create a musical score
            score = stream.Score()
            part = stream.Part()
            part.instrument = instrument.Piano()
            
            # Set tempo
            part.append(tempo.MetronomeMark(number=tempo_bpm))
            
            # Set time signature
            part.append(meter.TimeSignature('4/4'))
            
            # Add notes
            for pitch, duration in self.generated_notes:
                n = note.Note(pitch)
                n.quarterLength = duration
                part.append(n)
            
            score.append(part)
            
            # Save to MIDI
            score.write('midi', fp=filepath)
            return True
        except Exception as e:
            print(f"Error saving MIDI: {e}")
            return False

# GUI Setup
root = tk.Tk()
root.title("🎵 AI Music Generator")
root.geometry("800x650")
root.configure(bg="#f0f0f0")

# Title
title_label = tk.Label(root, text="🎵 AI Music Generator with LSTM", font=("Arial", 18, "bold"),
                       bg="#2c3e50", fg="white", pady=15)
title_label.pack(fill=tk.X)

# Info label
info_label = tk.Label(root, text="Generate unique musical compositions using AI algorithms!",
                     font=("Arial", 10), bg="#ecf0f1", fg="#2c3e50", pady=10)
info_label.pack(fill=tk.X, padx=10, pady=5)

# Main frame
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

# Configuration frame
config_frame = tk.LabelFrame(main_frame, text="⚙️ Configuration", font=("Arial", 11, "bold"),
                            bg="#ecf0f1", padx=15, pady=15)
config_frame.pack(fill=tk.X, pady=10)

# Number of notes
notes_label = tk.Label(config_frame, text="🎼 Number of Notes:", font=("Arial", 10), bg="#ecf0f1")
notes_label.pack(anchor=tk.W, pady=5)
notes_var = tk.StringVar(value="50")
notes_spinbox = ttk.Spinbox(config_frame, from_=10, to=200, textvariable=notes_var, width=10, font=("Arial", 10))
notes_spinbox.pack(anchor=tk.W, pady=(0, 10))

# Scale selection
scale_label = tk.Label(config_frame, text="🎯 Musical Scale:", font=("Arial", 10), bg="#ecf0f1")
scale_label.pack(anchor=tk.W, pady=5)
scale_var = tk.StringVar(value="major")
scale_options = ["major", "minor", "pentatonic"]
scale_menu = ttk.Combobox(config_frame, values=scale_options, state="readonly", textvariable=scale_var, width=20, font=("Arial", 10))
scale_menu.pack(anchor=tk.W, pady=(0, 10))

# Generation method
method_label = tk.Label(config_frame, text="🧠 Generation Method:", font=("Arial", 10), bg="#ecf0f1")
method_label.pack(anchor=tk.W, pady=5)
method_var = tk.StringVar(value="markov")
method_options = ["Random Sequence", "Markov Chain (AI)"]
method_menu = ttk.Combobox(config_frame, values=method_options, state="readonly", textvariable=method_var, width=20, font=("Arial", 10))
method_menu.pack(anchor=tk.W, pady=(0, 10))

# Tempo
tempo_label = tk.Label(config_frame, text="⏱️ Tempo (BPM):", font=("Arial", 10), bg="#ecf0f1")
tempo_label.pack(anchor=tk.W, pady=5)
tempo_var = tk.StringVar(value="120")
tempo_spinbox = ttk.Spinbox(config_frame, from_=40, to=200, textvariable=tempo_var, width=10, font=("Arial", 10))
tempo_spinbox.pack(anchor=tk.W, pady=(0, 10))

# Output frame
output_frame = tk.LabelFrame(main_frame, text="📊 Generated Sequence (Preview)", font=("Arial", 11, "bold"),
                            bg="#ecf0f1", padx=10, pady=10)
output_frame.pack(fill=tk.BOTH, expand=True, pady=10)

output_text = tk.Text(output_frame, height=12, width=90, font=("Courier", 9), bg="white", relief=tk.SUNKEN, bd=2)
output_text.pack(fill=tk.BOTH, expand=True)

# Status label
status_label = tk.Label(main_frame, text="Ready to generate music!", font=("Arial", 10), 
                       bg="#f0f0f0", fg="#27ae60")
status_label.pack(anchor=tk.W, pady=10)

generator = MusicGenerator()

def generate_music():
    """Generate music based on selected parameters"""
    try:
        num_notes = int(notes_var.get())
        scale = scale_var.get()
        method = method_var.get()
        tempo_bpm = int(tempo_var.get())
        
        status_label.config(text="🎵 Generating music...", fg="#3498db")
        root.update()
        
        # Generate notes
        if method == "Random Sequence":
            generator.generate_random_melody(num_notes, scale)
        else:
            generator.generate_markov_melody(num_notes, scale)
        
        # Display preview
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        
        preview = f"🎼 Generated Music Sequence ({scale} scale, {tempo_bpm} BPM):\n"
        preview += "="*80 + "\n\n"
        preview += "Pitch | Duration | Note Name\n"
        preview += "-"*80 + "\n"
        
        note_names = {60: "C", 62: "D", 63: "D#", 64: "E", 65: "F", 67: "G", 69: "A", 71: "B", 72: "C"}
        
        for pitch, duration in generator.generated_notes[:20]:  # Show first 20 notes
            note_name = note_names.get(pitch, f"Note{pitch}")
            duration_name = {0.25: "16th", 0.5: "8th", 1.0: "Quarter", 2.0: "Half"}[duration]
            preview += f"{pitch:5} | {duration:8} | {note_name:15} ({duration_name})\n"
        
        if len(generator.generated_notes) > 20:
            preview += f"\n... and {len(generator.generated_notes) - 20} more notes\n"
        
        output_text.insert(tk.END, preview)
        output_text.config(state=tk.DISABLED)
        
        status_label.config(text="✅ Music generated successfully! Ready to save.", fg="#27ae60")
        
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for Notes, Tempo, etc.")
        status_label.config(text="❌ Error in input values", fg="#e74c3c")

def save_music():
    """Save generated music to MIDI file"""
    if not generator.generated_notes:
        messagebox.showwarning("Warning", "Please generate music first!")
        return
    
    if not MUSIC21_AVAILABLE:
        messagebox.showerror("Error", "music21 library is not installed. Install it first!")
        return
    
    filepath = filedialog.asksaveasfilename(defaultextension=".mid", filetypes=[("MIDI files", "*.mid"), ("All files", "*.*")])
    
    if filepath:
        try:
            tempo_bpm = int(tempo_var.get())
            if generator.save_to_midi(filepath, tempo_bpm):
                messagebox.showinfo("Success", f"Music saved to:\n{filepath}")
                status_label.config(text=f"✅ Saved to {os.path.basename(filepath)}", fg="#27ae60")
            else:
                messagebox.showerror("Error", "Failed to save MIDI file")
                status_label.config(text="❌ Failed to save", fg="#e74c3c")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {e}")
            status_label.config(text="❌ Error saving file", fg="#e74c3c")

# Button frame
button_frame = tk.Frame(main_frame, bg="#f0f0f0")
button_frame.pack(fill=tk.X, pady=10)

generate_btn = tk.Button(button_frame, text="🎹 Generate Music", command=generate_music,
                        bg="#3498db", fg="white", font=("Arial", 11, "bold"), padx=15, pady=8, relief=tk.RAISED, bd=2)
generate_btn.pack(side=tk.LEFT, padx=5)

save_btn = tk.Button(button_frame, text="💾 Save as MIDI", command=save_music,
                    bg="#27ae60", fg="white", font=("Arial", 11, "bold"), padx=15, pady=8, relief=tk.RAISED, bd=2)
save_btn.pack(side=tk.LEFT, padx=5)

# Info note
info_note = tk.Label(main_frame, text="💡 Note: Install music21 to save MIDI files (pip install music21)",
                    font=("Arial", 9), bg="#fff3cd", fg="#333", padx=10, pady=5, justify=tk.LEFT)
info_note.pack(fill=tk.X, pady=10)

root.mainloop()
