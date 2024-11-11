import os
import glob

# Directorul unde sunt fișierele
folder_path = 'D:/depTrack/'

# Fișierul final în care vom combina toate fișierele
output_file = os.path.join(folder_path, 'comp.sql')

# Lista fișierelor în ordine
files = sorted(glob.glob(os.path.join(folder_path, 'dep*.sql')), key=lambda x: int(''.join(filter(str.isdigit, x))))

# Deschide fișierul de ieșire și adaugă conținutul fiecărui fișier
with open(output_file, 'w', encoding='utf-8') as outfile:
    for file in files:
        with open(file, 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())
            outfile.write('\n')  # Adaugă o linie nouă între fișiere pentru lizibilitate

print("Fișierul comp.sql a fost creat cu succes în D:/depTrack.")
