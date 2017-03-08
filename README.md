# simplefeed

A website written in Django which generates notifications when there are some changes in the static content of any of the websites entered by a user. The server regularly queries the status of the wesites entered by the user and compares it with their latest hash stored in a database. Upon identifying a change, a notification in the form of an RSS feed is served. 
