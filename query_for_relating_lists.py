import logging, json, os
from importio import importio
from importio import latch

dataRows = []
def findList(albumName, url):
    # To use an API key for authentication, use the following code:
    client = importio.Importio(user_id="c9c1a7b6-3ac3-499e-91f2-db84aa002336", api_key="/dtdffYudgO9w7GgltphpMpKlCwIdRf2bGEdt7kiCWhnqI7mrhTV5B+dBqvM0SexxnPrdcFLK7Vhi4/CJ1Q95w==", host="https://query.import.io")

    # Once we have started the client and authenticated, we need to connect it to the server:
    client.connect()

    # Because import.io queries are asynchronous, for this simple script we will use a "latch"
    # to stop the script from exiting before all of our queries are returned
    # For more information on the latch class, see the latch.py file included in this client library
    queryLatch = latch.latch(1)

    # In order to receive the data from the queries we issue, we need to define a callback method
    # This method will receive each message that comes back from the queries, and we can take that
    # data and store it for use in our app
    def callback(query, message):
      global dataRows
      # Disconnect messages happen if we disconnect the client library while a query is in progress
      if message["type"] == "DISCONNECT":
        print "Query in progress when library disconnected"
        dataRows = message

      # Check the message we receive actually has some data in it
      if message["type"] == "MESSAGE":
        if "errorType" in message["data"]:
          # In this case, we received a message, but it was an error from the external service
          print "Got an error!"
          dataRows = message
        else:
          # We got a message and it was not an error, so we can process the data
          # print "Got data!"
          # print json.dumps(message["data"], indent = 4)
          # Save the data we got in our dataRows variable for later
          dataRows = message

      # When the query is finished, countdown the latch so the program can continue when everything is done
      if query.finished(): queryLatch.countdown()

    # Issue queries to your data sources and with your inputs
    # You can modify the inputs and connectorGuids so as to query your own sources
    # Query for tile get rym containing lists'url

    print albumName + ":    " + url
    queryUrl = url + "lists/"
    client.query({
      "connectorGuids": [
        "f6b3171a-bc13-4280-b858-64e9f549db79"
      ],
      "input": {
        "webpage/url": queryUrl
      }
    }, callback)

    #print "Queries dispatched, now waiting for results"

    # Now we have issued all of the queries, we can "await" on the latch so that we know when it is all done
    queryLatch.await()

    #print "Latch has completed, all results returned"

    # It is best practice to disconnect when you are finished sending queries and getting data - it allows us to
    # clean up resources on the client and the server
    client.disconnect()

    global dataRows
    if dataRows["type"] == "DISCONNECT":
        return findList(albumName, url)

      # Check the message we receive actually has some data in it
    if dataRows["type"] == "MESSAGE":
        if "errorType" in dataRows["data"]:
          # In this case, we received a message, but it was an error from the external service
          return findList(albumName, url)
        else:
          # We got a message and it was not an error, so we can process the data
          # print "Got data!"
          # print json.dumps(message["data"], indent = 4)
          # Save the data we got in our dataRows variable for later
          dataRows = dataRows["data"]

    # Now we can print out the data we got
    #print "All data received."
    if "/" in albumName:
        albumName = "_".join(albumName.split("/"))
    with open("data/lists in "+albumName+".json", 'w') as outfile:
        json.dump(dataRows, outfile)

    #print "Included lists have been writen to file."
    # print "dataRows:"
    # print json.dumps(dataRows, indent=4)
    return dataRows

# if __name__ == "__main__":
#findList("ok computer", "https://rateyourmusic.com/release/album/massive_attack/mezzanine/")