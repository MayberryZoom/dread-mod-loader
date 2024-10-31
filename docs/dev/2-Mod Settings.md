When a user exports a mod, the export window will include a button to open a settings window, specific to the mod. By default, this includes the following settings:
- Display:
  - Boss lifebars
  - Enemy lifebars
  - Damage dealt by player
  - Damage dealt by enemies
  - Death counter
  - Room names on HUD
- Volume:
  - Master
  - Music
  - SFX
  - Environment
  - Speech
  - Grunt
  - GUI
- Door cover models:
  - Diffusion Beam
  - Ice Missile
  - Storm Missile
  - Bomb
  - Cross Bomb
  - Power Bomb
  - Permanently Closed

For a JsonMod, these are automatically applied to the mod's JSON when exporting. A DreadMod will need to implement the functionality for all of these itself, which will be covered in detail in a later guide.

Additionally, DML provides a system for removing any of these settings for your mod. This can be useful if a developer wants to enforce a specific vision (i.e. forcing boss lifebars off to avoid spoiling HP changes) or to remove irrelevant options (i.e. removing toggles for door covers that are unused). This can be done using the `disabled_settings` field in the `mod_info.toml`, and referencing the setting name. As well, an entire group of settings can be disabled at once. In the same order as the above list, the IDs for these are as follows:
- `display`
  - `boss_lifebar`
  - `enemy_lifebar`
  - `player_damage`
  - `enemy_damage`
  - `death_counter`
  - `room_names`
- `volume`
  - `master_volume`
  - `music_volume`
  - `sfx_volume`
  - `environment_volume`
  - `speech_volume`
  - `grunt_volume`
  - `gui_volume`
- `door`
  - `diffusion_beam_door`
  - `ice_missile_door`
  - `storm_missile_door`
  - `bomb_door`
  - `cross_bomb_door`
  - `power_bomb_door`
  - `permanently_closed_door`

There's also a special keyword that can be included, `all`, which will disable all of the settings at once.

Let's say for our mod, we want to disable all the door settings, and force the boss lifebars to off. To add these to our toml, we'll need to create an list of them like so:

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

disabled_settings = [
    "boss_lifebar",
    "door"
]
```

It's also possible to change the default settings for a mod. This is done by creating a new toml section, `default_settings`, then assigning a value to each one. Note that this field uses the actual names stored in settings, rather than a separate set of IDs, so they'll be in the format of `default_<setting>_<element>`, i.e. `default_diffusion_beam_radio_button_group = diffusion_beam_radio_alternate`.

Let's say we want to default the music volume to 50% and the death counter to on:

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

disabled_settings = [
    "boss_lifebar",
    "door"
]

[default_settings]
default_death_counter_checkbox = true
default_music_slider = 50
```

Creating a custom settings menu will be explained in a later guide.
