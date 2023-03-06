import simplenote
import sys
import os

try:
    note = sys.argv[1]

    # Authenticate
    credentials = os.popen("pass simplesync").read().splitlines()
    sn = simplenote.Simplenote(credentials[1], credentials[0]) # username and psw
    
    # Get note file
    with open(note, "r") as out_file:
        content = out_file.readlines()
    
    # Add new note
    sn.add_note({"content": ''.join(content)})
#    print(''.join(content))
except:
    print("No note file provided")

