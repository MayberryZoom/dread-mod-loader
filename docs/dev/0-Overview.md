DML makes use of open-dread-rando (ODR for short). ODR is a program that provides features for modifying Dread in a high-level way. It was created as the game patcher for Dread's implementation in Randovania, but has many features that are unused in randomizer that can be made use of for making Dread mods.

DML mods can come in two forms, which will be referred to as a DreadMod and a JsonMod.

JsonMods are considered the easier form of a DML mod, and make use of ODR's standard JSON format. With this format, most aspects of the game can be modified with a fairly simple data format, including:
- Pickups
- Door locks
- Breakable tiles
- Transport destinations
- Text
- Starting location/items
- Tunables (i.e. enemy properties)
- ..and much more

DreadMods are a more complicated but much more powerful form of a mod that consist of Python code. DML can load a custom Python class that defines exactly how the game should be patched. This class will have access to all of ODR's functions, which can be imported and used freely.

So which mod type should you use? It's important to understand the limitations of a JsonMod. ODR has a lot of restrictions, and will force many aspects of the game to be randomized. To list some of the more important ones:
- By default, every pickup must be modified. It's possible to revert many of these to their vanilla states using specific functions of ODR, but without a lot of effort, small aspects will be different.
- Beams are handled entirely differently. As a part of the standard patching process, ODR entirely overhauls the way beams are handled, making them work as "split" pickups (i.e. picking up Wave Beam first will not grant Wide Beam, unlike the vanilla game). This can be worked around, but there are still some bugs that come as a result (i.e. beam pickups granted from EMMIs will break until the player resets to checkpoint).
- New pickups are added to Kraid, Z-57, and Drogyga. These cannot be removed, they can only be set to grant nothing.
- Frozen ZDR is gone. This cannot be readded in any way using a JsonMod. (Note: Z-57 can still be accessed by releasing the X, then using the morph launcher)
- Outside of the features in the previous list, a JsonMod cannot modify any files other than the BRFLD (the file containing actor data). This includes:
  - Map icons
  - Model data
  - Room boundaries
  - Any Lua scripts

If you're a beginner and you're okay with those limitations (i.e. you want to create something closer to a plandomizer), you should create a JsonMod. It requires no programming knowledge, and most of it can be generated from a Randovania rdvgame.

If you want to make a fully custom mod or extend the functionality of a JsonMod, you should create a DreadMod. This will allow you to only modify the parts of the game you want changed and give you access to the rest of the Dread files.

The rest of this guide will be a walkthrough on the creation of mods.
