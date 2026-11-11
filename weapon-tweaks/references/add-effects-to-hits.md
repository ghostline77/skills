# Make weapon hits do something extra

Use this guide for quickhack uploads, EMP/chain attacks, marks, bleeding, stun or execution effects. The weapon's custom mod attaches a GameplayLogicPackage through OnAttach; add custom effector IDs to that package's effectors array.

Choose the actual event first: a committed hit, a body-part hit, a kill or an attack attempt. HitPrereq contains callback/pipeline/conditions; each condition is a separate HitPrereqCondition. WeaponType, AttackType and AttackSubtype filter different things. Damage/Process and processMiss=false are appropriate for many hit-earned effects; kill rewards commonly use Damage/PostProcess instead.

Keep the target and the effect recipient separate. A condition can inspect the victim while the earned effect goes to Player or Weapon. ApplyStatusEffect, AddStatusEffectToAttack, ApplyQuickhack and TriggerAttackOnTarget are different payloads; copying a field such as applicationChance across them can change its required type.

## Attribute-dependent chain lightning

**Use for:** a headshot that arcs to nearby enemies and upgrades with a skill threshold.

`Items.GradScavWeaponModAbility` has two outer ApplyEffectorEffector branches. Inline1 checks Owner.TechnicalAbilitySkill <55; inline8 checks >=55. They select inline2 and inline9 respectively. Both inner effects require a ranged-weapon headshot, ignore civilians and choose two enemies at 0.3..10 metres, but use different attack records: ScavChainLightning versus ScavChainLightningTech55.

For a fixed three-target arc without the attribute split, attach a clone of the inner effect directly:

```yaml
Effectors.MyHeadshotArc:
  $base: Items.GradScavWeaponModAbility_inline2
  targetHowManyEnemies: 3
  targetMaxDistance: 12.0
  targetMinDistance: 0.3
```

For a skill-scaled variant keep both outer branches and point them to custom inner effects. Change both comparisons to the same threshold and retain Less / GreaterOrEqual so there is no gap or overlap. `TechnicalAbilitySkill` here is the exact stat read by the donor; it is not automatically the character-sheet attribute rank. Match the intended stat rather than reusing the threshold number without its meaning.

The primary hit and the secondary attack must remain distinct. Increasing target count changes total damage without changing the original bullet, and replacing the attackRecord is where the secondary damage payload is controlled.


## Quickhacks with different rules for normal enemies and bosses

**Use for:** Overheat, blindness or another quickhack proc without applying the ordinary version to every target.

Fenrir's three effectors separate Human nonboss, MainBossSE/non-Chimera and Chimera targets. Clone inline1, inline7 and inline13 from Items.SaratogaMaelstromWeaponModAbility. Keep their inherited prerequisites; change objectAction to QuickHack.OverheatHack, BossOverheatHack and ChimeraOverheatHack respectively.

The probability belongs to uploadChance; uploadTime sets the effector's upload delay. The payload ObjectAction also carries active-target checks, start/completion effects and immunity restrictions. Replacing the effect with BurningApplicationRate is not an equivalent Overheat implementation. Clone the three branches as follows:

```yaml
Effectors.MyOverheat:
  $base: Items.SaratogaMaelstromWeaponModAbility_inline1
  objectAction: QuickHack.OverheatHack
  uploadChance: 0.5
  uploadTime: 1.0
Effectors.MyBossOverheat:
  $base: Items.SaratogaMaelstromWeaponModAbility_inline7
  objectAction: QuickHack.BossOverheatHack
  uploadChance: 0.05
  uploadTime: 1.0
Effectors.MyChimeraOverheat:
  $base: Items.SaratogaMaelstromWeaponModAbility_inline13
  objectAction: QuickHack.ChimeraOverheatHack
  uploadChance: 0.05
  uploadTime: 1.0
```

For a custom boss balance, adjust the boss/Chimera upload chances independently. Combining all targets into one broad hit prerequisite loses the variant action selection. Two overlapping branches can attempt two uploads from one event; mutually exclusive target filters prevent that.


## A first effect marks the victim; another attack consumes the mark

**Use for:** one weapon primes a target and another detonates, drains or upgrades the debuff.

SaburoKatana and SaburoTanto separate ordinary Bleeding, Saburo_Hemorrhage and Saburo_Healing. Their AddStatusEffectToAttackEffectors and subsequent player-heal application are connected through status prerequisites, not a single application-rate stat.

Use private marker IDs, a target-status check and a separate consuming effect. Choose whether application on a target already carrying the marker refreshes it, adds stacks or is blocked. If the payoff removes the marker, retain the removal effector; otherwise every later hit can continue earning the payoff. Clone both weapons' record references if preserving a paired-weapon design; cloning only one side can leave it checking the vanilla marker.

Do not replace normal/strong/draw attack filters with a single Melee filter unless every melee attack should participate. Keep the target-debuff check distinct from a player buff/cooldown check: they refer to different objects.


## Status application, crowd control and dismemberment

**Use for:** stun-on-strong-attack, bleed-on-crit, an execution effect or special damage against marked enemies.

Start from SasquatchHammer/TinkerBell for AddStatusEffectToAttackEffector, or MetelKurtWeaponModAbility for ForceDismembermentEffector and status removal. Inspect the donor's attack subtype, target flags and immunity-bearing status packages before broadening its trigger.

An applicationChance array of modifiers is not a scalar proc probability. A ForceDismemberment effector is not equivalent to increasing HitDismembermentFactor: the latter is a modifier participating in ordinary hit processing, while the former is an explicit action with its own prerequisite. Keep status removal/consumption when it supplies the reset rule for the next use.

For a target that is already stunned/burning/bleeding, decide whether a second application refreshes duration, increases stacks, converts to a stronger status or does nothing. That choice belongs in target conditions and the status's stacking/package behavior, not merely its tooltip text.

