# Mandatory-assigment-INF142
Team Local tactics. Making in into Team Network Tactics

Team members:
Nikita Kondratjuks,
Ivar Fatland,
Thomas Alme Matre

Instructions:

Start the server and the database. They are both acting as servers, listening for connections. The server will connect to the database when it needs to collect the champion list.

Start client 1 and choose "s" for singleplayer or "m" for multiplayer. If you select singleplayer, the game initiates with an AI opponent, controlled by the server. From this point, the player can select champions from the roster and the AI will subsequently randomly select its champions in turn. Next, the match result is calculated on the server and the result is sent to the player.

Selecting multiplayer will cause player 1 to wait until the second player connects. The first client to connect is assigned player 1. At this point, start client 2, and select multiplayer.

When both clients are connected and have selected multiplayer, they can start selecting champions from the table roster that is retrieved by the server from the database and sent to the clients. Clients, in turn, select two champions, after which the match results will be calculated by the server and served to the clients.
