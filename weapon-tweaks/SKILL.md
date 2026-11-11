---
name: weapon-tweaks
description: Create and modify Cyberpunk 2077 TweakXL weapons and iconic abilities using vanilla weapon records and practical adaptations.
---

Find a close vanilla donor in `data/weapons.jsonl`, trace the records that produce the desired behavior, then clone and override those records under custom IDs. Use `python scripts/query.py get RECORD`, `search PATTERN --values` or `chain RECORD`; paths are relative to this skill.

Read the guide matching what the user wants:
- [Create or rebalance a weapon](references/create-and-rebalance-weapons.md): damage, handling, firing, projectiles, quality and prices.
- [Make hits do something extra](references/add-effects-to-hits.md): quickhacks, EMP, chain attacks, marks and debuffs.
- [Reward kills and build streaks](references/reward-kills-and-build-streaks.md): healing, earned buffs, stacks and threshold rewards.
- [Change behavior with player state](references/change-behavior-with-player-state.md): aiming, charge, movement, health, reload and cyberware.
- [Add timed powers and cooldowns](references/add-timed-powers-and-cooldowns.md): draw bursts, combos, time slow and indicators.
- [Look up records](references/database.md): reference format and search commands.

Preserve inherited behavior unless changing it is part of the design. Check record types, field spelling, recipient, modifier units and removal/reset rules against the donor chain.
