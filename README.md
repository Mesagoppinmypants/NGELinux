# Game Server Readme

Please put in a pull request for any and all useful changes and fixes you make! It is advisable to use a VPN and username you don't normally use online, to protect your identity. The focus of this project is Linux, but it may work on Windows.

We are not associated with SWGLegends or SWGReborn. They may be using some of our work but we do not have any association.

## Emulators

We anons working on this fully support all the SWG emus out there and recognize the fact that they are superior in quality, efficiency, and completion to this one. This is for fun, and not profit, and not competition with any existing emulation project. You would be stupid to host a public server with this code.

## Missing NPCs

As for the missing NPC's, the majority of them are in the sku.0/sys.server/compiled/game/datatables/buildouts _ws.iff files, but so far we have been unable to load them. There is a method to persist them to the database but it has been hit and miss. This method is documented in the USEFUL_COMMANDS.md file.

## Contact

Please file a bug/issue first. If you need to contact us, send message on reddit to https://www.reddit.com/user/swgmasters as our old email address no longer works.
# Building

See README_LINUX.md and README_WINDOWS.md

# Database

See ORACLE.md

# Notes and Commands

See NOTES.md and USEFUL_COMMANDS.md

# Client Files

## Client

First, download and setup ProjectSWG to get the tre files you need. Then, unzip the contents of the below over the top, replacing any files you are prompted to. Make sure to edit login.cfg to point to your SWG server IP.

https://mega.nz/#F!mZw2BLJJ!-vcXi2_NN-WoslIjiY32Gw

# Additional Server /data Files

## Clientdata 

More may be required from the .tocs and .tres later but this is bare minimum. So far getting searchTree and searchTOC hasn't been successful in the server config files.

https://mega.nz/#F!mZw2BLJJ!-vcXi2_NN-WoslIjiY32Gw


## Appearance/SSA Files

https://mega.nz/#F!mZw2BLJJ!-vcXi2_NN-WoslIjiY32Gw


# Mirrors

Git: http://repo.or.cz/w/swg-src.git


Static (only at initial commit): https://mega.nz/#F!mZw2BLJJ!-vcXi2_NN-WoslIjiY32Gw


Feel free to fork and mirror yourself with caution. Please share useful changes you make on Reddit.com/r/swg or Voat.co/v/swg if the git repos are ever taken down.

### Developers VM Download Links

SID(testing):

https://docs.google.com/uc?export=download&confirm=k1dz&id=0Bw5QxmhEYpyzdFVPV2x3LVYzWUE

https://docs.google.com/uc?export=download&confirm=sfMW&id=0B8qYSmfamAxsalhBNG5xSjR1QTg

Comes with newest libs and buildtools, and no prebuilded server/empty db with precreated users.
You have to build your own server first before you can start it. Follow the instructions of the sid_readme.md