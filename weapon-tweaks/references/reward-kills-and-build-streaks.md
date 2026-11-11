# Reward kills and build streaks

Use this guide for a buff earned by a kill, a heal on execution, consecutive-kill stacks or a threshold payoff. Keep the kill event, accumulated counter, per-stack reward and final payoff separate so each can have its own reset rule.

A kill prerequisite must observe the outcome of damage processing. The donors below use TargetKilledHitPrereqCondition in Damage/PostProcess and also distinguish defeated/unconscious targets. Reusing a Process-stage ordinary-hit prerequisite changes the reward from on-kill to on-hit.

## A kill starts a temporary berserker window

**Use for:** attack speed, recoil control, reload bonuses or infinite combo earned by killing an enemy.

Wakako's chain is `Items.WakakoKatanaWeaponModAbility_inline1 -> inline2 -> BaseStatusEffect.Wakako_Tiger_Buff -> inline3 -> inline4 -> inline5`. The trigger is a melee kill in Damage/PostProcess, with an inverted Defeated type condition. The status lasts ten seconds; its weapon-targeted group grants both combo flags and AttackSpeed *1.175.

Clone each layer that changes. Keeping the vanilla status while editing its group would change the donor weapon too. This adaptation gives six seconds of infinite combo and AttackSpeed *1.3:

```yaml
Effectors.MyKillWindow:
  $base: Items.WakakoKatanaWeaponModAbility_inline1
  statusEffect: BaseStatusEffect.MyKillWindow

BaseStatusEffect.MyKillWindow:
  $base: BaseStatusEffect.Wakako_Tiger_Buff
  duration: MyKillWindow.Duration
  packages:
    - MyKillWindow.Package

MyKillWindow.Duration:
  $type: StatModifierGroup
  statModifiers:
    - $type: ConstantStatModifier
      statType: BaseStats.MaxDuration
      modifierType: Additive
      value: 6.0

MyKillWindow.Package:
  $type: GameplayLogicPackage
  effectors:
    - Effectors.MyKillWindowStats

Effectors.MyKillWindowStats:
  $base: BaseStatusEffect.Wakako_Tiger_Buff_inline4
  statGroup: MyKillWindow.Stats

MyKillWindow.Stats:
  $type: StatModifierGroup
  statModifiers:
    - $base: BaseStatusEffect.Wakako_Tiger_Buff_inline6
    - $base: BaseStatusEffect.Wakako_Tiger_Buff_inline7
    - $base: BaseStatusEffect.Wakako_Tiger_Buff_inline8
      value: 1.3
```

This keeps the melee-kill trigger. For a ranged variant clone inline2 and its weapon-type condition, replacing Melee with Ranged; don't change only the status. For an on-hit variant choose a Process-stage hit donor instead of retaining TargetKilled in PostProcess. For a one-off proc, add a cooldown marker as a separate condition/status rather than turning MaxStacks into a cooldown.


## Consecutive kills build a streak, then unlock a stronger effect

**Use for:** increasing crit, earning a short slow after multiple kills, or rewarding sustained aggression.

The Witcher sword separates three jobs:

1. `Items.WitcherSwordWeaponModAbility_inline9` applies `BaseStatusEffect.Witcher_Multikill_Buff` on a qualifying melee kill.
2. That status has MaxStacks 2 and a five-second duration. Its inline5 package is stackable and applies a weapon CritChance +50 group. Its separate inline9 package is also stackable and adds MultiKill_Counter +1.
3. `Items.WitcherSwordWeaponModAbility_inline0` applies SwordWitcherTDBuff through an AND prerequisite. One nested branch is `(MultiKill_Counter >= 2 OR Witcher_Wounded_Buff present)`, another is the melee-kill event, and another requires no status tagged TDEffect.

To make a three-kill design, clone the status, its max-stack group and the threshold prerequisite together. Raising only the threshold to 3 while the counter is capped at 2 makes the reward unreachable. Clone all modified nested prerequisite parents so their references point to the new leaves.

To change streak timeout, change the status duration group's MaxDuration. To change reward per stack, change its stackable weapon group. Keep the counter package separate from the reward package: removing the counter because it appears to be an unrelated stat disables threshold activation.

The source's low-health alternative means the reward can occur without reaching the ordinary streak threshold. Remove that OR branch when the design must strictly require a kill streak. Preserve or replace the no-TDEffect guard deliberately; otherwise repeated kills can compete with an already active time-slow owner.


## Heal on kill versus regeneration from a debuff interaction

**Use for:** lifesteal, executions that heal the player, or a sustained heal while a marked target bleeds.

`Items.CyberspadeWeaponModAbility_inline1` modifies a stat pool, usePercent=true, setValue=false, referencing inline4 (Health, statPoolValue 12.5). Its inline2 prerequisite is Damage/PostProcess, TargetKilled plus an inverted Unconscious type check. This is an immediate percentage pool update after the qualifying kill, not a heal-over-time status.

```yaml
Effectors.MyKillHeal:
  $base: Items.CyberspadeWeaponModAbility_inline1
  statPoolUpdates:
    - $base: Items.CyberspadeWeaponModAbility_inline4
      statPoolValue: 8.0
```

The donor's applicationTarget is None; do not reinterpret that as Target. Preserve the donor's owner context when attaching it. To make damage-based lifesteal instead of a fixed percentage heal, this constant pool-update shape is insufficient by itself: find a modifier/effector that consumes damage dealt, or implement the missing calculation.

For regeneration, start from `BaseStatusEffect.Saburo_Healing` and follow its duration, package and ModifyStatPoolModifierEffector. For a bleed-dependent heal, also keep the SaburoKatana prerequisite/status interaction. Copying only Saburo_Healing bypasses the original condition that earns it.

