# TODO:
# Handle files with same title
# Remove local notes trashed remote notes: don't ignore trash and add proper entry
# in index.json
import simplenote
import json
import os

# Local notes path
path = "/home/cimino/documents/notes/"


# Authenticate
def authenticate():
    credentials = os.popen("pass simplesync").read().splitlines()
    return simplenote.Simplenote(credentials[1], credentials[0])  # username and psw


# Check wheter the file doesn't already exist or it's been updated
def sync_index(local_index, sn):
    # Get remote notes
    remote_index = sn.get_note_list()[0]
    remote_index = [x for x in remote_index if x["deleted"] == False]  # Ignore trash

    update_index = []
    for note in remote_index:
        key = note["key"]
        title = note["content"].partition("\n")[0].replace("#", "").lstrip() + ".md"
        version = note["version"]

        update_note = [x for x in local_index if x["key"] == key]
        if not update_note or int(update_note[0]["version"]) < version:
            with open(path + title, "w") as out_file:
                out_file.write(note["content"])

        update_index.append({"key": key, "title": title, "version": str(version)})

    # Update local notes
    with open("index.json", "w") as out_file:
        json.dump(update_index, out_file, indent=1)


if __name__ == "__main__":
    sn = authenticate()

    # Open local notes
    with open("index.json", "r") as out_file:
        local = json.load(out_file)

    sync_index(local,sn)
