import sync
import json
import sys
import os

# Full path of the note
note_path = sys.argv[1]

# Authenticate
sn = sync.authenticate();

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
    sync.remote_sync(local_index,sn)
