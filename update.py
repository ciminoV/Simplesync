import simplenote
import json
import sys
import os

try:
    note = sys.argv[1]

    # Authenticate
    credentials = os.popen("pass simplesync").read().splitlines()
    sn = simplenote.Simplenote(credentials[1], credentials[0])  # username and psw

    # Get note file
    with open(note, "r") as out_file:
        content = out_file.readlines()

    with open("index.json") as out_file:
        local_index = json.load(out_file)
    
    # TODO:
    # check if the file already exists in the index and if so update remote note
    # getting the note key and content
    # update_note create a new note if the key is not given: can be used to add
    # a new note
    note = os.path.basename(os.path.normpath(note))
    update_note = [x for x in local_index if x["title"] == note]
    if update_note:
        key = update_note[0]["key"]

        sn.update_note({"key": key, "content": "".join(content)})
    else:
        sn.add_note({"content": "".join(content)})

except:
    print("No note file provided")
