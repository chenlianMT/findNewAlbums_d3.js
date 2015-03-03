import json

    # for file in os.listdir("data/"):
    #     file_path = os.path.join("data/", file)
    #     with open(file_path) as f:
    #         content = f.read()
    #         #print file + str(len(content))

json_data = open("data/FINAL_TOP100_RELATIONS.json").read()
data = json.loads(json_data)

file_for_v = {"name": "WTF", "children": []}
for i in xrange(18):
    relation = data[i]["relation"]
    j = 0
    for key in relation:
        values = {}
        values["album"] = key
        values["artist"] = relation[key]["artist"]
        values["count"] = relation[key]["count"]
        file_for_v["children"].append(values)

        j += 1
        if j > 100:
            break

with open("data/File_for_v.json", 'w') as outfile:
    json.dump(file_for_v, outfile)

print "Albums included have been writen to file."
print json.dumps(file_for_v, indent=4)