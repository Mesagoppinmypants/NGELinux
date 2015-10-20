Small blurb about command syntax:
    /command
    
    /command <argument you must specify> <>
    
    /command [optional argument you may not need to specify] []
    
    /command -parameter means you need to actually type -whatever -parameter
    
    /command [TARGET] simply means it must be your current target. [TARGET]
    
    /command <argument | argument2> means there is more than one option. Pick 1. | ARGUMENT |
    
    
#Enabling God Mode (Admin)
Note: Your localOptions.cfg file must have "adminGodToAll=1" in the [GameServer] section. Alternatively, if you would only like certain users to have access to the God Mode abilities, you can toggle that bool to 0 in localOptions and instead you will need to edit both the "qa_admin" and "us_admin" .tab files with the account username you'd like to have. Set their GodLevel to 55 for all commands and abilities, and their skill to "admin". Then compile it with the miff.exe tool. It is recommended that once you have compiled this file once, you only make future revisions with TRE Explorer as compiling the .tab document can get complex.

Once you have either globally enabled login or have enabled it for your account, login to the game and type:

    /setGodMode
    # Turns on God Mode
    /setGodMode 50
    # If you have adminGodToAll Enabled, do this instead.
    /setGodMode off
    # Disables the features of God Mode
    
# Making Admin Commands Work In Your Client
You need to edit your user.cfg file and add the following:
(Note: You only need what's under [ClientGame], the UserInterface modifications just make everything so much easier.

    [ClientGame]
    0fd345d9 = true
    [ClientUserInterface] 
    debugExamine=1 
    debugClipboardExamine=1 
    allowTargetAnything=1 
    drawNetworkIds=1
 
0fd345d9 enables the admin commands in your client. Without it your client will not send the commands to the server and will return the "no such command" error.

debugExamine allows you to /examine an object and get the ObjectID, and various other information like it's template.

debugClipboardExamine makes the debug info you get from /examine get placed on your clipboard so you can paste it with Ctrl+v

allowTargetAnything enables the ability to target objects like entire structures or objects you normally cannot to fix issues.

drawNetworkIds puts the ObjectID and NetworkID above every objects name.


# Basic God Mode Commands - Teleportation

    /planetWarp <planet>
    # Teleports you to the specified planet/terrain.
    /planetWarpTarget <planet>
    # Teleports your target to the specified planet/terrain.
    /teleport <x> <z> <y>
    # Teleports you to the specified coordinates on the current terrain.
    /teleportTo <player>
    # Teleports you to the specified player anywhere in the galaxy. 
    /teleportTarget <x> <z> <y>
    # Teleports your target to the specified coordinates on the current terrain.
    /npeGoToMedicalBay
    # Teleports your character to the opening medical bay instance (don't do with invulnerable on)
    /npeGotoMilleniumFalcon
    # Teleports your character to the opening millenium falcon instance.
    /npeGoToStationGamma
    # Teleports your character to Station Gamma.
    /npeGoToTansariiStation
    # Teleports your character to Tansarii Station.

# Basic God Mode Commands - Managing Your Character

    /invulnerable
    # Toggles Invulnerability - Makes your character invulnerable (removes health/action) and you appear as a NPC.
    /aiIgnore
    # Toggles aiIgnore - Artificial Intelligence ignore you (no aggro).
    /setSpeed <speed>
    # Changes the speed by which your character negotiates terrain. Recommended that you don't go higher than 5.
    /getPlayerId <name>
    # Returns the object ID (oid) of your character. This will be used frequently.
    /object hide <oid> <bool>
    # Hides your character from non God Mode characters. Set bool to 0 for visible and 1 for hidden. Make a macro for 0 and 1. It's easier. 

# Basic God Mode Commands - Managing Other Characters

    /getAccountInfo <player FIRST name>
    # Returns various account information about the specified character including their IP Address. They must be online.
    /getStationName <player FIRST name>
    # Returns the username of the specified player character. Does not work if player is offline.
    /getPlayerId <player FIRST name>
    # Returns the object ID (oid) of the specified player character. Does not work if player is offline.
    /server getCharacterInfo <oid or player FIRST name>
    # Returns Station ID, and Object ID of a character, even when they are offline. Along with other info.
    /freezePlayer <player FIRST name>
    # Freezes the player preventing them from moving. It's like being rooted.
    /unfreezePlayer <player FIRST name>
    # Reverses the effects of /freezePlayer
    /squelch [TARGET]
    # Prevents your target from talking, using mail, spatial, or tells. Must be your TARGET (don't type TARGET)
    /unsquelch [TARGET]
    # Reverses the effects of /squelch
    /csDisconnectPlayer <player>
    # Disconnects the specified player.
    /kick <player FIRST name>
    # Kicks the specified player from the server and returns them to the character screen.
    /findPlayer <player name or partial name with *>
    # Searches the galaxy for any players with matching names.
    /cityInfo
    # Displays an SUI window in which you can search and manage cities across the galaxy.
    /listGuilds
    # Spams your chat box with information on all active guilds of the galaxy.
    /credits [-target] <cash | bank> <+|- value>
    # Gives you (or optionally your target) the specified (or subtracts the specified) amount of credits from/to the bank or cash.

Attach QATool:

    /script attach test.qatool <your network id>
    
To see what QAtool can do:
    
    /qatool
    
# Planet Persist

Set your localOptions.cfg to only have 1 persister thread and loadWholePlanets=1. Teleport to the planet you want to persist, attach the QATool, and as god, run

    /qatool persistplanet <planetname>
    
Once you have persisted all planets, shutdown the server and optionally remove the data/sku.0/sys.server/compiled/game/datatables/buildout/<planetname/*_ws.iff but only the ws files. You can then restart the server, optionally turning loadWholePlanet off to make it load faster and use less memory.
# Server Shutdown

    /server shutdown 1 1 1 1
    
# Spawn NPCs In Eisley Cantina

    /script attach theme_park.tatooine.mos_eisley.masterspawner 1082874

# Testing

    /setgodmode 50 
    /getPlayerId <player first name only> 
    /script attach test.qatool <id>

# Resteuss

* Find all the objects in the Imperial and Rebel base with ph1 attached to them, and run completeResteussStageOne on each (4830 80 5829 and 5900 81 5638 for the bases)
* Go to the center of Resteuss and find the ph1 marker, and execute startResteussStageTwo
* After Resteuss is fully spawned, create an object 400m away from /waypoint 5192.928223 77.937180 6074.740234 and use any random item to attach a script.

    /script attach theme_park.restuss_event.pvp_region

* Make sure to also use the GM command /hide "objectID" 1to make the object non visible to player eg   /object hide 8762345533 1

# Spawning From Master Items table

    dsrc/sku.0/sys.server/complied/game/datatables/item/master_item/master_item.tab 
    /createStaticItem <id> 
    /createStaticItem armor_stormtrooper_bicep_camo_l_04_01 
    /object spawn object/tangible/terminal/terminal_character_builder.iff 
    /object spawn heroic_echo_stormcommando 

# Beast Master

    Isomerase- /object spawn object/tangible/loot/beast/enzyme_1.iff 
    Lyase- /object spawn object/tangible/loot/beast/enzyme_2.iff 
    Hydrolase- /object spawn object/tangible/loot/beast/enzyme_3.iff 
    Pet Likes/dislikes showHappiness 

# Misc

     Set objvar = /objvar set 

# User.cfg

    [ClientUserInterface] 
    debugExamine=1 
    debugClipboardExamine=1 
    allowTargetAnything=1 
    drawNetworkIds=1
