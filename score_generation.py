import subprocess
from PIL import Image
import os
import re
def format_melody(melody):
  formatted = []
  for note in melody:
      # Remove unwanted characters
      note = note.replace("'", "").replace(',', '').strip()#.replace('"', '')
      formatted.append(note)
  # Join the list into a string and return
  return ' '.join(formatted)


def format_h_melody(melody):
    formatted = []
    for note in melody:
        formatted_note = f"{note[0]}{note[1]}"
        formatted.append(formatted_note)
    formatted_string = ' '.join(formatted)
    return formatted_string

def format_chord(melody):
    formatted = []
    for note in melody:
        chord_notes = ' '.join(note[1])
        string = f"{note[0]}{chord_notes}{note[2]}{note[3]}"
        formatted.append(string)
    return ' '.join(formatted)

def plain_melody(melody):
  plain_melody =[]
  for note in melody:
    plain_melody.append(note[0]+note[1])
  return plain_melody

def lilypond_generation(melody, name, uppertime, lowertime):
    melody = plain_melody(melody)
    lilypond_score = f"""
\\version "2.24.1"  
\\header {{
  tagline = "" \\language "english"
}}

#(set-global-staff-size 26)

\\score {{

    \\fixed c' {{
      \\time {uppertime}/{lowertime}
      {format_melody(melody)}
      \\bar "|"
    }}
    \\layout {{
      indent = 0\\mm
      ragged-right = ##f
      \\context {{
        \\Score
        \\remove "Bar_number_engraver"
      }}
    }}
}}

\\score {{
    \\unfoldRepeats \\fixed c' {{
      \\time {uppertime}/{lowertime}
      {format_melody(melody)}
      \\bar "|"
    }}
    \\midi {{ }}
}}
"""

    with open('score.ly', 'w') as f:
        f.write(lilypond_score)

    # Generate PNG image and MIDI file
    subprocess.run(['lilypond', '-dpreview', '-dbackend=eps', '--png', '-dresolution=300', '--output=score', 'score.ly'],
                   check=True)

    # Generate MP3 file
    # subprocess.run(['fluidsynth', '-ni', '/Users/chakhangchan/Documents/VS_code/Music_theory_app/melody_key/GeneralUser/GeneralUserGSv1.471.sf2', 'score.midi', '-F', f'static/{name}.mp3', '-r', '44100'],
               # check=True)

    with Image.open('score.png') as img:
        width, height = img.size
        crop_height = height
        crop_rectangle = (0, 75, width, crop_height / 10)
        cropped_img = img.crop(crop_rectangle)

        os.makedirs('static', exist_ok=True)
        cropped_img.save(f'static/cropped_score_{name}.png')
    return f'static/cropped_score_{name}.png'
