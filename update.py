import simplenote
import sync
import json
import sys
import os

try:
    # Full path of the note
    note_path = sys.argv[1]

    # Authenticate
    credentials = os.popen("pass simplesync").read().splitlines()
    sn = simplenote.Simplenote(credentials[1], credentials[0])  # username and psw

    # Open note file and notes index 
    with open(note_path, "r") as out_file:
        content = out_file.readlines()

    with open("index.json") as out_file:
        local_index = json.load(out_file)
    
    note = os.path.basename(os.path.normpath(note_path))
    update_note = [x for x in local_index if x["title"] == note]
    if update_note:
        key = update_note[0]["key"]

        sn.update_note({"key": key, "content": "".join(content)})
    else:
        sn.add_note({"content": "".join(content)})

    #TODO
    # Sync entire index only if new file is added otherwise only entry updated
    sync.sync_index(local_index,sn)

except:
    print("No valid note file provided")
