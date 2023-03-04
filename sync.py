import simplenote
import json
import os

# Authenticate
credentials = os.popen("pass simplesync").read().splitlines()
sn = simplenote.Simplenote(credentials[1], credentials[0]) # username and psw

# Get remote notes 
remote_index = sn.get_note_list()[0]
remote_index = [x for x in remote_index if x['deleted'] == False] # Ignore trash

# Update local notes
with open("index.json", "r") as out_file:
    local_index = json.load(out_file)

update_index = []
for note in remote_index:
    key = note["key"]
    title = note["content"].partition('\n')[0].replace('#','').lstrip()+".md"
    version = note["version"]

    # Check wheter the file doesn't already exist or it's been updated
    update_note = [x for x in local_index if x["key"] == key]
    if not update_note or int(update_note[0]["version"]) < version:
        with open(title, "w") as out_file:
            out_file.write(note["content"])

    update_index.append({
        "key": key,
        "title": title,
        "version": str(version)
    })

# Update index file
with open("index.json", "w") as out_file:
    json.dump(update_index, out_file, indent=1)
