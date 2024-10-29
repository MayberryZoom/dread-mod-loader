A mod can include custom assets to replace existing ones. To do this, a new folder within a mod's folder should be created to contain a ROMFS mod. For example, if we want to include a custom Burenia track in our mod, our file structure might look like this:

```
.
|__ assets/
|   |__ sounds/
|       |__ streams/
|           |__ s_aqua_001.dspadpcm.bfstm
|           |__ s_aqua_002.dspadpcm.bfstm
|__ mod_info.toml
|__ patcher.json
```

The path to this folder should then be set in the toml, like so:
```toml
identifier = "developer.my_mod"

patch_type = "json"
patch_file = "patcher.json"

name = "My Mod"
author = "Developer"
version = "1.0.0"
description = "This is my first mod"
thumbnail = "thumbnail.png"

assets_path = "assets"

disabled_settings = [
    "boss_lifebar",
    "door"
]
```

Now, when the mod is exported, these files will automatically be included in the mod, applied last.
