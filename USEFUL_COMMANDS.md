# QATool and Godmode

Become God:

    /setgodmode 50

Get your network ID:

    /setspeed 1
    
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

# Travel

    /planetwarp +name 
    /planetwarp rori 

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
