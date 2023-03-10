import sync
import sys
import json
import os

# Note title
note = os.path.basename(os.path.normpath(sys.argv[1]))

# Authenticate
sn = sync.authenticate();

# Open notes index
with open("index.json") as out_file:
    local_index = json.load(out_file)

# Trash remote note and sync
trash_note = [x for x in local_index if x["title"] == note]
if trash_note:
    key = trash_note[0]["key"]
    sn.trash_note(key)
    sync.remote_sync(local_index,sn)
else:
    print("Missing note")
