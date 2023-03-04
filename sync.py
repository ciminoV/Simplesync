import simplenote
# import itertools
import json
import os

# Authenticate
credentials = os.popen("pass simplesync").read().splitlines()
sn = simplenote.Simplenote(credentials[1], credentials[0]) # username and psw

# Get remote notes 
remote_index = sn.get_note_list()[0]
remote_index = [x for x in remote_index if x['deleted'] == False] # Ignore trash

# Open local notes
with open("index.json", "r") as out_file:
    local_index = json.load(out_file)

# TODO
# Iterate over remote index
# Check for updates if remote version > local version
# Create new file if not present
update_index = []
for note in remote_index:
    if [x for x in local_index if x["key"] == note["key"]]:
        print("Check the version on this one {}".format(note["key"]))
    else:
        # Create the note otherwise
        print("Gotta create this one")

    update_index.append({
        "key": note["key"],
        "title": note["content"].partition('\n')[0].replace('#','').lstrip()+".md",
        "version": str(note["version"])
    })

with open("index.json", "w") as out_file:
    json.dump(update_index, out_file, indent=1)
