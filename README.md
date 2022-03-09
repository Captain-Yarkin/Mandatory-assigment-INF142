# Mandatory-assigment-INF142
Team Local tactics. Making in into Team Network Tactics

Team members:
Nikita Kondratjuks,
Ivar Fatland,
Thomas Alme Matre

Instructions:

Start the server and the database. They are both acting as servers, listening for connections. The server will connect to the database when it needs to collect the champion list.

Start client one and choose "s" for singleplayer or "m" for multiplayer 

If you choose "s" for singleplayer the games starts without the need of the another client since the player is playing against an AI. From this point the player can choose champions from the roster and the AI will randomly choose after the player in 2 rounds of picking champions. After that the game begins and the result gets sent to the player,

 
if you choose multiplayer it will connect to the servers and start waiting for a seconed player to connect then start client 2. They will both try to connect to the server either as player 1 or player 2. The first client to connect is assigned as player 1, and the second client to connect is assigned as player 2.

From this point you can play the game from the client’s side. Selecting champions from the table roster that is sent to the client. Clients in turn select two champions, after which the match results will be calculated by the server and served to the clients.
