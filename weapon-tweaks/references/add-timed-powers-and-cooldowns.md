# Add a temporary weapon power with a cooldown

Use this guide for a draw-attack burst, temporary infinite combos, attack-speed windows, time slow and visible active/cooldown indicators. Use [kill rewards](reward-kills-and-build-streaks.md) when the design centres on accumulating kills or stacks.

## Separate activation, payload and cooldown

The activation prerequisite determines when the player earns the power. Apply a timed StatusEffect to Player; its packages contain the actual weapon-stat/time-slow effects. A separate cooldown status is checked before activation and applied when activation succeeds.

Use Perks.ApplyStatusEffectOnPlayer for a player reward; a target application can buff the enemy being hit instead. A five-second active status does not itself enforce a 60-second cooldown. Starting both statuses at activation allows another use at t=60; starting the cooldown when the buff expires allows t=65.

## A draw attack crits every time, but only sometimes starts the power

Give the attack crit its own prerequisite, independent from the buff's cooldown:

```yaml
Prereqs.MyDrawHit:
  $base: Perks.IsHitEquipAttack
  pipelineType: Damage
  processMiss: false
Effectors.MyDrawCrit:
  $base: Items.TakemuraKatanaWeaponModAbility_inline2
  prereqRecord: Prereqs.MyDrawHit
```

The donor's attack-crit modifier adds CritChance 1. Its original hit filter is a final-attack filter, so override prereqRecord for draw-only behavior. The buff gets a separate prerequisite that includes EquipAttack and checks the Instigator lacks both active buff and cooldown.

For those StatusEffectPresent hit conditions, use short status names such as MyDrawBuff/MyDrawCooldown; the condition prefixes BaseStatusEffect itself. The status application effector instead takes the full record ID BaseStatusEffect.MyDrawBuff.

processMiss=false means drawing into empty space does not earn the power. If activation should occur on the draw animation regardless of a hit, select a draw/equip event rather than changing only the duration or crit filter.

## Define the active duration and payload

A StatusEffect references a duration StatModifierGroup containing a BaseStats.MaxDuration modifier, a maxStacks group and packages. Decide whether reapplication adds stacks, refreshes duration or reapplies packages. For a single active window use a one-stack group and block activation while it is present.

A combo/speed payload should be a weapon-targeted stat group. Clone Perks.ApplyStatGroupOnWeapon, retain removeWithEffector=true and set reapplyOnWeaponChange according to whether the benefit should transfer to another equipped weapon.

The vanilla Wakako combo group contains CanMeleeInfinitelyCombo=1, CanWeaponInfinitlyCombo=1 and an AttackSpeed multiplier. The second stat's spelling is Infinitly. Use those controls for a combo window rather than reducing stamina and assuming the combo limit disappears too.

Put the cooldown application and the weapon payload in the active status package. Set removeWithEffector=false on the cooldown application so it survives the active buff. Give the cooldown its own duration, one-stack policy and empty packages. Savable controls whether its state persists through saves; it does not define whether its icon appears.

## Add Sandevistan-style time slow

Clone BaseStatusEffect.SynapticAcceleratorEffector, which uses SetTimeDilationEffector. Its fields include reason, dilation, duration, easing curves and affectsPlayer. Use a private reason so weapon cleanup does not share the cyberware's sandevistan ownership key.

```yaml
Effectors.MySlow:
  $base: BaseStatusEffect.SynapticAcceleratorEffector
  prereqRecord: Prereqs.AlwaysTruePrereq
  removeAfterActionCall: false
  removeAfterPrereqCheck: false
Effectors.MySlow.reason: n"my_weapon_slow"
Effectors.MySlow.dilation: 0.20
Effectors.MySlow.duration: 5.0
Effectors.MySlow.affectsPlayer: false
playerStateMachineTimeDilation.timeDilationAcceptedReasons.sandevistanEffectReasons:
  - !append-once n"my_weapon_slow"
```

Attach MySlow to the active status package. Dilation 0.20 means 20% world speed; affectsPlayer=false allows the player to act faster relative to that world. Keep the effector duration and the status MaxDuration aligned. Disable player/NPC dilation effects on the status duration when its lifetime should remain fixed instead of stretching with the slow.

The accepted-reasons entry selects Sandevistan presentation for that reason. It does not attach charge drain, cyberware perks or the whole Sandevistan player status package. An actual Sandevistan player-state prerequisite is a separate mechanism from this presentation list.

## Give the active window and cooldown their own indicators

StatusEffect.uiData references StatusEffectUIData; the ability's UIData is GameplayLogicPackageUIData and describes the iconic ability instead.

```yaml
BaseStatusEffect.MyBuffUI:
  $type: StatusEffectUIData
  displayName: LocKey("my_buff_name")
  iconPath: buff_melee
  priority: -3.0
BaseStatusEffect.MyCooldownUI:
  $type: StatusEffectUIData
  displayName: LocKey("my_cooldown_name")
  iconPath: buff_melee
  priority: -3.0
```

Reference MyBuffUI from the active status and MyCooldownUI from the cooldown status. Supply the localization entries. Empty cooldown packages do not create or hide an icon; UI data supplies the presentation.

## A short cinematic slow earned by a kill

The Witcher donor is a compact alternative to a long player-relative power. BaseStatusEffect.SwordWitcherTDBuff lasts 0.9 seconds; inline3 uses dilation 0.17, duration 0.9, delay 0.08, reason meleeHit and MeleeHitEaseIn/Out curves. Its package also starts a cooldown, and the applying weapon prerequisite excludes an existing TDEffect status.

Clone the status, duration group, package and slow effector if changing the lifetime. Keep the exclusion and cooldown separate from easing; removing the package's second effector removes part of the activation/reset behavior. See [kill streaks](reward-kills-and-build-streaks.md) for the original counter and low-health routes that earn this reward.
