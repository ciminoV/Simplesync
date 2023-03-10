from copy import deepcopy
import simplenote
import json
import os

# Local notes PATH
PATH = "/home/cimino/documents/notes/"


# Authenticate
def authenticate():
    credentials = os.popen("pass simplesync").read().splitlines()
    return simplenote.Simplenote(credentials[1], credentials[0])  # username and psw


# Sync local notes with remote notes
def remote_sync(local_index, sn):
    remote_index = sn.get_note_list()[0]
    remote_index = [x for x in remote_index if x["deleted"] == False]  # Ignore trash

    update_index = []
    for note in remote_index:
        key = note["key"]
        title = (
            note["content"].partition("\n")[0].replace("#", "").lstrip() or "new_note"
        ) + ".md"
        version = note["version"]

        # Check for duplicate remote notes
        if update_index:
            duplicate = [x for x in update_index if title in x["title"]]

            num = ""
            if duplicate:
                num = "(%i)" % (len(duplicate))

            title = title + "%s" % num

        # Add or update notes
        update_note = [x for x in local_index if x["key"] == key]
        if not update_note or int(update_note[0]["version"]) < version:
            with open(PATH + title, "w") as out_file:
                out_file.write(note["content"])

        update_index.append({"key": key, "title": title, "version": str(version)})

    # Check for deleted remote notes
    local_copy = deepcopy(local_index)
    for x in local_copy: x.pop("version")
    update_copy = deepcopy(update_index)
    for x in update_copy: x.pop("version")

    delete_note = [
        i
        for i in local_copy + update_copy
        if i in local_copy and i not in update_copy
    ]
    for delete in delete_note:
        os.remove(PATH + delete["title"])

    # Update the index of local notes
    with open("./index.json", "w") as out_file:
        json.dump(update_index, out_file, indent=1)


if __name__ == "__main__":
    sn = authenticate()

    # Open the index of local notes
    with open("./index.json", "r") as out_file:
        local = json.load(out_file)

    remote_sync(local, sn)
