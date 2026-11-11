# Weapon reference lookup

`../data/weapons.jsonl` has one JSON object per record: `name`, `type`, `fields`. It includes every vanilla WeaponItem, every Items record tagged WeaponMod, iconic ability records, and their transitive record dependencies. Shared status effects, quickhacks, prerequisites, part lists and prices are included where a weapon references them.

```powershell
python scripts/query.py get Items.Preset_Saratoga_Default
python scripts/query.py get Items.SaratogaMaelstromWeaponModAbility_inline1
python scripts/query.py search 'RicochetCount' --values --limit 15
python scripts/query.py chain Items.SaratogaMaelstromWeaponModAbility_inline1 --depth 2
rg -n 'CanWeaponInfinitlyCombo' data/weapons.jsonl
```

`search` accepts a case-insensitive regular expression; `--values` searches fields too. `chain` follows references to other included records. Use small depth/limits, then retrieve the relevant records directly.

`@HEX` preserves an unresolved ID; `@type:HEX` is an unresolved class, not a usable TweakXL type name. Empty TweakDBID is `@0000000000000000`. `scriptFlats` groups a configuration path rather than a clonable record. The data contains resolved vanilla values: clone with `$base` rather than pasting every inherited field into YAML.
