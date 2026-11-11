# Create a weapon or change how it shoots

Use this guide for standalone/iconic weapon creation, damage, recoil, reload, capacity, elemental damage, pellets, penetration, smart projectiles and prices. Use [hit effects](add-effects-to-hits.md) for extra events caused by a hit and [state-dependent behavior](change-behavior-with-player-state.md) for bonuses that only exist while a condition holds.


## Create a standalone weapon
Clone an `Items.Preset_*` matching the weapon family. Changing a vanilla ID instead changes that weapon globally. Keep the inherited `slotPartList`, `slotPartListPreset`, placement slots, attacks and appearance unless changing them is part of the design.

For an iconic, add the appropriate iconic blueprint, IconicWeapon tag, Quality.IconicItem modifier and iconic quality randomization. Attach the custom weapon mod through a SlotItemPartPreset; the iconic tag alone does not install an ability. See [hit effects](add-effects-to-hits.md) for the ability attachment pattern.

Weapon preset -> parts / statModifierGroups -> statModifiers is the route for static behavior. Many iconic differences live here even if WeaponModAbility.effectors is empty.

## Modifier operations and units
Inspect the exact stat and consumer. Constant, Combined and Curve modifiers have different fields. Combined modifiers can scale from Player or Weapon stats; a constant replacement loses that scaling. Additive, AdditiveMultiplier and Multiplier are distinct operations.

Do not apply one percentage convention to every stat. In vanilla examples:
- ModifyAttackCritChanceEffector uses an additive CritChance modifier of 1 for guaranteed qualifying-attack crit.
- ApplyQuickhackEffector.uploadChance is a scalar 0..1 probability.
- NashWeaponMod adds PoisonedApplicationRate 10; this is not the same schema as a 0..1 effector chance.
- NekomataBreakthroughWeaponMod adds CanWeaponIgnoreArmor 0.5.
- A duration group uses BaseStats.MaxDuration in seconds.

## Damage and elemental behavior
DamagePerHit, FirePower, elemental damage groups, charge multipliers and target-specific attack modifiers are different control points. Compare source and donor groups before appending another elemental group. Thermal damage, Burning and the Overheat quickhack are separate mechanics.

For body-part bonuses, use an attack effector with the appropriate hit prerequisite rather than changing global DamagePerHit. PulsarBuzzsawWeaponModAbility_inline1 multiplies limb-hit damage by 1.4. OvertureDanteWeaponModAbility uses head-hit prerequisites with distance-based effects.

## Handling and timing
CycleTime/CycleTimeBonus affect firing cadence; ReloadTimeBonus affects reload; charge timing has its own stats. Inspect groups on the receiver/barrel and weapon preset because parts can supply the effective values.

NashWeaponMod combines ChargeMultiplier +0.08, ChargeTime AdditiveMultiplier +0.2, recoil multipliers 0.6 and poison application. Copying its ability alone misses these changes.

## Quality
Quality modifiers, iconic flags and randomization groups affect generation. Existing saved items may retain generated parts/stats; use a fresh item when comparing record changes. Upgrading an iconic, assigning its spawn tier and adding an iconic ability are separate operations.

## Buy and sell prices
Replace each modifier array independently for fixed base prices:

```yaml
Items.MyWeapon.buyPrice:
  - $type: ConstantStatModifier
    statType: BaseStats.Price
    modifierType: Additive
    value: 70000.0
Items.MyWeapon.sellPrice:
  - $type: ConstantStatModifier
    statType: BaseStats.Price
    modifierType: Additive
    value: 7000.0
```

Replacement removes the old quality/discount/sell-multiplier chain from those arrays. Append instead when the design should preserve the existing pricing formula. Price changes do not add the item to a vendor.

## Permanent extra projectiles with intentional damage trade-offs

**Use for:** turning a revolver into a spread weapon or increasing projectile count without adding an on-hit explosion.

DoomDoomWeaponMod changes ProjectilesPerShotBonus +2 alongside DamagePerHit *2, recoil, dismemberment, headshot modifier and RicochetCount *0. Its distinctive behavior is not found by inspecting its empty ability effectors list.

```yaml
Items.MyWeapon.statModifiers:
  - !append
    $base: Items.DoomDoomWeaponMod_inline1
    value: 1.0
```

This copies only the extra-projectile control. Choose damage compensation and spread independently; copying all DoomDoom modifiers also disables ricochet and changes headshot/recoil behavior. For an aiming-only version put these modifiers in an ADS-gated weapon group instead of appending them permanently.


## Penetration, armor ignore and ricochet are separate axes

**Use for:** a shot that passes cover, a weapon that ignores armor, or predictable ricochet chains.

NekomataBreakthroughWeaponMod contains TechPierceChargeLevel *0, CanWeaponIgnoreArmor +0.5, RicochetChance +1, RicochetCount +3 and angle/search controls. The tech attack/evolution still supplies the compatible firing behavior.

Copy the specific modifiers into a private group; do not assume an armor-ignore modifier enables wall penetration. RicochetCount and chance do not define the allowed angle or target search cone. For a straight penetrating sniper, omit ricochet additions; for a bouncing weapon, preserve compatible projectile behavior rather than forcing a tech template into a power preset without its other dependencies.


## Cyberware-dependent target count and explosive smart rounds

**Use for:** extra ADS locks only with Smart Link, or a smart weapon with a different projectile payload.

PrototypeShingenWeaponMod_inline0 is a CombinedStatModifier adding `2 * Player.HasSmartLink` to SmartGunAdsMaxLockedTargets. Lowering value changes the per-link contribution; replacing it with a constant removes the cyberware gate.

```yaml
Items.MyWeapon.statModifiers:
  - !append
    $base: Items.PrototypeShingenWeaponMod_inline0
    value: 1.0
```

The preset independently selects Attacks.SmartBulletHighExplosivePackage, whose defaultFire and chargeFire reference SmartBulletHighExplosiveFire. Copying the mod's target-count modifier does not make bullets explosive. Clone the ranged package/attack to change only one fire path; assigning a shared replacement to both defaultFire and chargeFire intentionally changes both.

