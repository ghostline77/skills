# Change a weapon while aiming, charging, moving or using cyberware

Use this guide for alternate firing modes, charge thresholds, movement/distance bonuses, low-health builds and cyberware-dependent bonuses. Decide whether the bonus exists continuously while a condition holds or is earned as a timed reward when an event occurs.

For a continuous weapon change, clone an ApplyStatGroupEffector targeted at Weapon, with the appropriate state prerequisite and removeWithEffector=true. For a conditionally available attack effect, an outer ApplyEffectorEffector can watch the player state while an inner effector filters attacks. These serve different purposes and should not be collapsed into a broad always-on effect.

## A charge threshold switches the weapon's behavior

**Use for:** a precision mode, extra projectiles, stronger ricochet or a different spread pattern above a charge level.

`Items.TiconWeaponModAbility_inline0` applies Ticon_Projectile_Pattern_Change_Ability to Player while inline1 is satisfied. Inline1 is a Weapon-targeted StatPoolPrereq on WeaponCharge, compared as a percentage against an array containing inline2, whose Charge modifier is 30. The application uses removeWithEffector=true.

```yaml
Prereqs.MyChargeThreshold:
  $base: Items.TiconWeaponModAbility_inline1
  valueToCheck:
    - $base: Items.TiconWeaponModAbility_inline2
      value: 60.0

Effectors.MyChargeMode:
  $base: Items.TiconWeaponModAbility_inline0
  prereqRecord: Prereqs.MyChargeThreshold
```

This retains the vanilla mode payload and raises its trigger to 60%. To change the mode itself, clone the status and trace its packages to the weapon stat group. Replacing valueToCheck with a bare Float is the wrong schema: it is an array of modifier records. Removing removeWithEffector changes the mode from a state-bound effect to something that may persist after charge drops.


## Aiming changes the projectile pattern, not just accuracy

**Use for:** hip-fire bullets versus ADS pellets, tighter distributed shots, or an ADS cadence trade-off.

`Items.HerculesWeaponModAbility_inline0` applies a Weapon stat group under Perks.PlayerIsAiming. Its group combines CycleTimeBonus +0.75, ProjectilesPerShotBonus +2, NumShotsToFire +2, spread layout controls, ADS spread, FirePower *3 and DamagePerHit *1.33.

Clone the group and select only the controls needed for the new design. For a tighter ADS spread without extra pellets, copying the entire Hercules group would accidentally change shot count, damage and cadence. For a shotgun-like ADS mode, retain the projectile count and spread-distribution controls, then balance damage separately.

Use removeWithEffector=true and reapplyOnWeaponChange=false as in the donor so the alternate mode is scoped to aiming with that weapon. An always-attached stat group with the same modifiers changes hip fire too. If the weapon cannot fire the intended projectile package, changing spread stats alone does not create that projectile behavior.


## A bonus exists only while Sandevistan is active

**Use for:** guaranteed melee crits, bleeding or other effects conditional on the player using time-slow cyberware.

`Items.SurgeonKatanaWeaponModAbility_inline0` is ApplyEffectorEffector gated by inline1, a TimeDilationPSMPrereq with stateName Sandevistan. It activates inline2, a ModifyAttackCritChanceEffector with Perks.IsWeaponMelee. A second outer/inner pair (inline4 -> inline6) adds Bleeding under the same state condition.

```yaml
Effectors.MySandevistanCritGate:
  $base: Items.SurgeonKatanaWeaponModAbility_inline0
  effectorToApply: Effectors.MySandevistanCrit

Effectors.MySandevistanCrit:
  $base: Items.SurgeonKatanaWeaponModAbility_inline2
  critChance:
    - $base: Items.SurgeonKatanaWeaponModAbility_inline3
      value: 0.5
```

The outer prerequisite tracks the player state; the inner prerequisite selects affected attacks. Attaching only the inner crit effector makes the bonus available outside Sandevistan. Changing the inner weapon filter creates a ranged variant without replacing the outer state gate. Entering the Sandevistan visual-reason list is a different mechanism: a screen presentation reason does not itself establish that the player state prerequisite is satisfied.


## Reload randomizes elemental damage and debuff application

**Use for:** an unpredictable gun with a new damage/debuff combination between firing sequences.

RoyceWeaponModAbility uses ChaosWeaponCustomEffector for crit/debuff groups and ChaosWeaponDamageTypeEffector for the elemental selection, with Perks.PlayerNotReloading. This is specialized runtime behavior, not a list of four elemental modifiers picked at random by TweakXL.

Clone the ability and the groups whose ranges/modifiers change. Inspect each custom class's consumed fields before adding a field such as randomChance: a new arbitrary flat does not make the script read it. Keep elemental allocation, crit changes and application-rate groups coordinated. Copying all elemental groups simultaneously creates mixed damage rather than reproducing the random choice.

If the design must select among a new set of effects beyond the custom class's supported choices, it needs a compatible existing selection effector or runtime code; renaming the record alone does not extend the class.


## Ammo refund only in an alternate firing state

**Use for:** charge-mode efficiency, a headshot refund or a reward during a temporary buff.

GwentTiconWeaponModAbility_inline1 uses CeaselessLeadAmmoEffector and percentToRefund 0.16. Its prerequisite is an AND of Ticon_Projectile_Pattern_Change_Ability present and a Damage/Process hit filter.

```yaml
Effectors.MyModeRefund:
  $base: Items.GwentTiconWeaponModAbility_inline1
  percentToRefund: 0.25
```

This increases the amount but keeps the state requirement. For a headshot refund, clone the hit prerequisite and add a body-part condition while keeping the alternate-mode check. For an always-available refund, deliberately replace the AND prerequisite rather than accidentally attaching a different effector with no filters.

Refund percentage, magazine capacity and inventory ammunition are different values. Additional pellets can cause more qualifying hit callbacks; preserve/check per-shot conditions before using a shotgun-like donor.


## Distance and velocity reward different play styles

**Use for:** a sniper that rewards range, a close-range execution weapon, or a gun that rewards high movement speed.

OvertureDanteWeaponModAbility_inline0 and inline1 separately modify headshot crit and damage with distance (0..35). They have improveWithDistance=true. Changing only one leaves the other part of the original ramp unchanged.

```yaml
Effectors.MyRangeDamage:
  $base: Items.OvertureDanteWeaponModAbility_inline1
  minDistance: 5.0
  maxDistance: 45.0
  percentMult: 1.4
```

For the opposite range preference inspect/support the class's improveWithDistance flag instead of swapping min and max into an invalid interval. Keep a positive range span.

PowerOfThePackWeaponModAbility_inline6 uses ModifyDamageWithVelocity, unitThreshold=10 and percentMult=0.25. Its threshold refers to velocity, not distance to the victim. A higher DamagePerHit constant cannot reproduce the ramp or its moving/stationary distinction.


## Aiming improves handling while a combat event grants another buff

**Use for:** a weapon with both an ADS advantage and an opening-combat reward.

BorisWardenWeaponModAbility has independent paths. Inline0 applies Warden_Stealth_Multiplier_Helper when PlayerJustEnteredCombat is present. Inline2 applies a weapon CycleTimeBonus +0.5 group while aiming.

Clone only the path being changed. Replacing the whole ability with an ADS effector removes the combat-event reward; copying the helper status without its trigger can make an opening effect permanent. State-gated weapon groups generally use removeWithEffector=true, whereas an earned timed status may use false so it can finish its duration after the event ends.

Use multiple effectors when triggers differ. A single AND prerequisite would require aiming and the combat-entry condition simultaneously, changing when the player earns the event reward.


## Health-dependent damage versus a threshold-triggered emergency buff

**Use for:** damage that rises as health falls, or a one-time defensive/offensive reward below critical health.

Inspect NueBreeWeaponModAbility and RogueMasamuneWeaponModAbility for groups using Player Health alongside damage/crit/handling stats. A Combined/Curve modifier can continuously read health. A StatPrereq or Perks.IsPlayerInCritHealth instead gates a separate effect on a threshold; it does not create a continuous ramp by itself.

WitcherSwordWeaponModAbility_inline13 applies Witcher_Wounded_Buff under IsPlayerInCritHealth, with removeWithEffector=true. Its other prerequisites can use that status as an alternate route to the kill reward. If building a strict cooldown-based emergency ability, replace that continuous state lifetime with an earned timed status and a cooldown guard. Otherwise it can remain active for the whole low-health period or activate again whenever the condition is re-established.

