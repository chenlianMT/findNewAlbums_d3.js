import json, query_for_relating_lists, query_for_relating_albums, os

def getData():
    # for file in os.listdir("data/"):
    #     file_path = os.path.join("data/", file)
    #     with open(file_path) as f:
    #         content = f.read()
    #         #print file + str(len(content))

    json_data = open("data/top_100_album.json").read()
    data = json.loads(json_data)

    if "data" not in data:
        print "Error: data error!"
        raise
    else:
        top_100_list = []
        for i in xrange(20):
            album = {"name": 0, "rating": 0, "artist": 0,
                     "link": 0, "relation": {}}
            album["name"] = data["data"][i]["album/_text"][0]
            album["rating"] = float(data["data"][i]["rating"][0])
            album["artist"] = data["data"][i]["artist"]
            album["link"] = data["data"][i]["album"][0]
            getRelations(album)
            top_100_list.append(album)
        with open("data/FINAL_TOP100_RELATIONS.json", 'w') as outfile:
            json.dump(top_100_list, outfile)

        print "Albums included have been writen to file."
        print json.dumps(top_100_list, indent=4)


def getRelations(album):
    query = album["link"]
    result = query_for_relating_lists.findList(album["name"], query)
    if "results" in result:
        lists = result["results"]
        for i in xrange(10):
            list = lists[i]
            listName = list["list_url/_text"]
            listUrl = list["list_url"]
            result = query_for_relating_albums.findAlbum(listName, listUrl)
            #print json.dumps(result, indent = 4)
            if "results" in result:
                items = result["results"]
                for item in items:
                    if "album/_text" in item:
                        if album["name"] != item["album/_text"]:
                            if item["album/_text"] in album["relation"]:
                                name = item["album/_text"]
                                album["relation"][name]["count"] += 1
                            else:
                                rAlbum = {"count": 1, "artist": item["artist"]}
                                album["relation"][item["album/_text"]] = rAlbum
            else:
                print "Error: query for relating albums error!"

    else:
        print "Error: query for relating lists error!"

getData()