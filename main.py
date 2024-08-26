import music21
import tkinter as tk
from tkinter import messagebox
import random
import os

def get_scale(key_note_name, scale_type):
    scale_dict = {
        'Major': music21.scale.MajorScale,
        'Minor': music21.scale.MinorScale,
        'Dorian': music21.scale.DorianScale,
        'Mixolydian': music21.scale.MixolydianScale
    }
    ScaleClass = scale_dict.get(scale_type)
    if ScaleClass:
        return ScaleClass(music21.pitch.Pitch(key_note_name))
    return None

def generate_solo_from_scale(scale_obj, length):
    solo = music21.stream.Stream()
    if scale_obj:
        notes = scale_obj.getPitches()
        motifs = []  # List to store motifs
        
        # Create several motifs with different patterns
        for _ in range(3):
            motif_length = random.randint(4, 8)
            motif = []
            last_note_index = random.randint(0, len(notes) - 1)
            
            for _ in range(motif_length):
                step_options = [last_note_index - 3, last_note_index - 2, last_note_index - 1, last_note_index, last_note_index + 1, last_note_index + 2, last_note_index + 3]
                step_options = [i for i in step_options if 0 <= i < len(notes)]
                note_index = random.choice(step_options)
                last_note_index = note_index
                
                pitch = notes[note_index]
                note_obj = music21.note.Note(pitch.name)
                note_obj.quarterLength = random.choice([0.25, 0.5, 1, 1.5, 2])
                motif.append(note_obj)
                
                if random.random() < 0.2:
                    rest = music21.note.Rest(quarterLength=random.choice([0.25, 0.5, 1, 1.5, 2]))
                    motif.append(rest)
            
            motifs.append(motif)
        
        while length > 0:
            motif = random.choice(motifs)
            for note_obj in motif:
                new_obj = music21.note.Note(note_obj.name) if isinstance(note_obj, music21.note.Note) else music21.note.Rest()
                new_obj.quarterLength = note_obj.quarterLength
                solo.append(new_obj)
                length -= new_obj.quarterLength
                if length <= 0:
                    break
            if length > 0:
                pause = music21.note.Rest(quarterLength=random.choice([0.25, 0.5, 1, 1.5, 2]))
                solo.append(pause)
    
    return solo

def export_solo(solo):
    i = 1
    while os.path.exists(f"generated_solo{i}.xml"):
        i += 1
    filename = f"generated_solo{i}.xml"
    try:
        solo.write('musicxml', fp=filename)
    except Exception as e:
        print(f"Error saving file: {e}")
        return None
    return filename

def generate_solo():
    key_name = key_entry.get().strip()
    scale_type = scale_entry.get().strip()
    length_str = length_entry.get().strip()

    try:
        length = int(length_str)
        length = length * 4
    except ValueError:
        messagebox.showerror("Error", "Length must be an integer.")
        return

    if key_name in valid_keys and scale_type in valid_scales:
        try:
            key_note = music21.pitch.Pitch(key_name)
        except music21.exceptions.Music21Exception:
            messagebox.showerror("Error", "Invalid key name.")
            return
        
        scale_obj = get_scale(key_name, scale_type)

        if scale_obj:
            solo = generate_solo_from_scale(scale_obj, length)
            filename = export_solo(solo)
            if filename:
                messagebox.showinfo("Info", f"Solo generated and saved as '{filename}'!")
            else:
                messagebox.showerror("Error", "Failed to save the solo.")
        else:
            messagebox.showerror("Error", "Invalid scale type. Please choose a valid scale.")
    else:
        messagebox.showerror("Error", "Please enter valid key and scale type.")

valid_keys = {'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B'}
valid_scales = {'Major', 'Minor', 'Dorian', 'Mixolydian'}

app = tk.Tk()
app.title("Jazz Solo Generator")

tk.Label(app, text="Select Key (e.g., C, D#, Bb):").pack()
key_entry = tk.Entry(app)
key_entry.pack()

tk.Label(app, text="Scale Type (e.g., Major, Minor, Dorian, Mixolydian):").pack()
scale_entry = tk.Entry(app)
scale_entry.pack()

tk.Label(app, text="Length (in measures):").pack()
length_entry = tk.Entry(app)
length_entry.pack()

tk.Button(app, text="Generate Solo", command=generate_solo).pack()

app.mainloop()
