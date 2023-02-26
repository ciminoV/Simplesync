import simplenote
import json
import os

# Authenticate
credentials = os.popen("pass simplesync").read().splitlines()
password = credentials[0]
user = credentials[1]

sn = simplenote.Simplenote(user, password)

# Get remote notes 
remote_index = sn.get_note_list()[0]
remote_index = [x for x in remote_index if x['deleted'] == False] # Ignore trash

# Open local notes
with open("index.json", "r") as out_file:
    local_index = json.load(out_file)

# TODO
# Check for updates if remote version > local version
# Create new file if not present

# Update local notes
update_index = []
for file in remote_index:
    update_index.append({
            "key": file["key"],
            "title": file["content"].partition('\n')[0].replace('#','').lstrip()+".md",
            "version": str(file["version"])
    })

with open("index.json", "w") as out_file:
    json.dump(update_index, out_file, indent=1)
