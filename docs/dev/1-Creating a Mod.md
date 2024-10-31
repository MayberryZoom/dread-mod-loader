To start, let's create a new folder within the mods directory that will contain our mod files.

Next, all mods require a `mod_info.toml` file, which will define all the information necessary to load the mod. This file must be located within the root of your mod's folder and must be named `mod_info.toml`, exactly.

To populate this toml file, we'll first need to come up with an identifier for our mod. If two mods share the same identifier, only one will load, so this should be as unique as possible. The best practice for this is to first put the mod developer's name, followed by the mod's name, i.e. `mod_developer.mod_name`. For this guide, let's assume our name is "Developer". We'll start the toml file by adding this identifier, like so:

```toml
identifier = "developer.my_mod"
```

Next, we'll need to declare what type of mod this is. This should either be `py` or `json`, depending on whether this is a DreadMod or JsonMod. For now, let's focus on a JsonMod, and add that to our toml:

```toml
identifier = "developer.my_mod"

patch_type = "json"
```

Now we need to tell DML where our patch file is located. This can be located anywhere in your mod's files, as long as you give a path to it, relative to the mod's root. Let's say for this mod, we've placed our JSON next to the `mod_info.toml` and named it `patcher.json`:

```toml
identifier = "developer.my_mod"

patch_type = "json"
patch_file = "patcher.json"
```

This is actually all that's required for the mod to load, but we should add some more information about the mod. We can provide the mod's name, author, version, and description like so:

```toml
identifier = "developer.my_mod"

patch_type = "json"
patch_file = "patcher.json"

name = "My Mod"
author = "Developer"
version = "1.0.0"
description = "This is my first mod"
```

All of these will be displayed in the mod list in the main window. If they aren't provided, they will default to "Unkown". Note that if this description is too long, it'll get cut off. This field should be used for a short summary about the mod.

When the user exports the mod, they'll first be presented with a screen showing info about the mod. This window is where we can provide the user with a longer description about the mod. We'll do this by putting a path to a markdown file in our toml:

```toml
identifier = "developer.my_mod"

patch_type = "json"
patch_file = "patcher.json"

name = "My Mod"
author = "Developer"
version = "1.0.0"
description = "This is my first mod"
readme_path = "README.md"
```

The contents of this file will be loaded into the export window when the user double clicks on the mod. This file can be as long as you want; a scroll bar will be added automatically. If this path isn't provided, the export window will instead display the description.

We can also define a custom thumbnail for our mod, to  be displayed in the mod list as well. Like the patch file, this is a relative path:

```toml
identifier = "developer.my_mod"

patch_type = "json"
patch_file = "patcher.json"

name = "My Mod"
author = "Developer"
version = "1.0.0"
description = "This is my first mod"
readme_path = "README.md"
thumbnail = "thumbnail.png"
```

With that, all the basic parts of the toml are finished.
