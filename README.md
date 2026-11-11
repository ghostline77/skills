# Ghostline skills

Agent skills for authoring Cyberpunk 2077 mods. Each skill contains a `SKILL.md`
entry point and the references or tools needed for its task.

## Available skills

| Skill | Use |
| --- | --- |
| [weapon-tweaks](weapon-tweaks/SKILL.md) | Create or modify weapon records, iconic effects, triggered abilities and cooldowns with TweakXL. |

## Install and use

Copy the complete `weapon-tweaks` directory into your agent's skills directory.
For Codex on Windows, the default destination is
`%USERPROFILE%/.codex/skills/weapon-tweaks`. Keep its `references`, `data`
and `scripts` directories together with `SKILL.md`.

Ask the agent to use `$weapon-tweaks` and describe the desired weapon or effect.
The skill routes to a task guide and queries its bundled record data. It does
not install generated mods into the game.

To query records directly, run from the skill directory with Python installed:

```powershell
python scripts/query.py search Slaught --values
python scripts/query.py get Items.Preset_Unity_Default
python scripts/query.py chain Items.Preset_Unity_Default
```

See the [database reference](weapon-tweaks/references/database.md) for the data
format and query options. Generated records still need the appropriate TweakXL
installation and in-game checks.

## Add a skill

Create a directory with a `SKILL.md` containing `name` and `description`
frontmatter. Put task instructions in that entry point and link longer references
from it. Use relative paths within the skill so copying the directory preserves
its tools and documentation. Add the skill to the table above.
