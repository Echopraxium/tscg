# HandOver — 2026-09-29 — Ship Builder (modular 3D ship editor)

**Author**: Echopraxium with the collaboration of Claude AI
**Purpose**: resume the Ship Builder design in a fresh session.
**Where to put this**: `instances/_01_Worksite/<date>/` (crafting-side HandOvers), or
Project Knowledge until the instance folder exists.

---

## 1. Load first — by name

- **`head-over-memory`** — for any TSCG fact touched (M0 instance, types, facets, domains).
- **`tscg-instance-pipeline`** — only when the Ship Builder M0 instance is modeled
  (after the check-M3 / Application chantier has landed; see §6).

## 2. Authority for this project

- **Design authority = the specification doc**, not this HandOver:
  "Ship Builder — Specification v0" — https://claude.ai/code/artifact/ce45932f-525a-4506-b1df-42c1a9b30058
  Read it first; this file only records context, locked decisions and next steps.
- TSCG facts (types, facets, domains) come from HEAD, never from this file.

## 3. Context

- **Users**: the developers of a dogfight space game (a team disappointed by Star Citizen).
- **Inspiration**: the No Man's Sky Corvette workshop (modular exterior + interior).
- **Intent**: a standalone tool, eventually its own GitHub repository; prototyped from
  the TSCG repository first.

## 4. Locked decisions (Michel, 2026-09-29) — do NOT relitigate

**Architecture**
- Front-end in **Godot 4** (the game team's engine): same renderer as the game.
- **One app, four editors on one shared assembly engine**:
  Equipment Editor · Structure Editor · Module Editor · Ship Editor.
  **Equipment + Structures = Module; Module + Module or Structure = Ship.**
- **Blender** models geometry; **glTF 2.0** is the pivot format; the **Module Editor
  owns gameplay metadata** (socket types, stats, axes). Sockets may be placed as named
  Empties in Blender as a starting point.
- The **assembly JSON** is the ship's source of truth; a merged `.glb` is only an export.
- Blender integration beyond authoring (rig, render) comes later via an add-on.

**Connection modes**
- Point **sockets** (cockpit, engines, weapons, gear…) or a shared **grid** along
  1, 2 or 3 axes; **habitats combine in length, width and height**. Grid faces are typed
  (open / wall / door / hatch); exterior grid faces expose sockets.

**Catalog**
- Habitat equipment: bunk, stairs, door, container, refiner, decor, **cooler**.
  Weapon equipment: mount, loader, sight.
- Structures: bulkhead, floor, ceiling, window, wing, walkway, duct/linkage, fairings,
  domes/antennas/nacelles. **Wings are cosmetic — no lift.** Cosmetics count toward the
  part budget; `traversable` flag feeds interior circulation.

**Engines and heat**
- Engine types trade thrust / mass / fuel burn / spool time / heat;
  stacking with `maxStack` and a diminishing `stackFactor`.
- **One engine type per ship** (no mixing).
- **Shared ship-wide heat pool**, capacity and cooling from **coolers**
  (a single "cooler" equipment — no radiator / heat-sink split).
- **The builder only provides characteristics; gameplay use (overheat, fuel, drone AI)
  is the game's responsibility.**

**Drones**
- A drone is a **mobile weapon, expendable like a missile**, assembled like a module;
  fired from a **launcher** (weapon module whose loader holds drones).
  Ship Editor shows stats fully loaded and after all drones are launched.

**TSCG placement** (depends on the check-M3 chantier — see its own HandOver)
- Instance type **`m3:Application`** (not TscgTool: the tool is not reflexive).
- Facets **Maturity = Prototype**, **Purpose = Editor**; `m1:domain` = **VideoGame**.
- Genre / Setting / PlayerScale (VideoGame instance facets) describe **the game**, not the builder.

## 5. Open questions (listed in the spec's last section)

For the game team: Godot 4 version and standalone app vs editor plugin; flight model and
formulas to mirror; polygon/texture budgets; single vs two-seat cockpits; root part
(landing gear vs hull); part budget and **grid cell size**; existing assets vs fresh
Blender parts; licence.
For Michel: instance folder for Application instances.

Suggestion made, not decided: put the assembly engine in `addons/ship_builder/` so the
same code ships as a standalone app and as a plugin in the game project.

## 6. Next steps

1. Share the spec with the game team; collect answers to §5.
2. **Gate "Conventions locked"**: one Blender test export into Godot to fix units, axes
   (front −Y in Blender → +Z glTF) and socket Empties conventions.
3. Prototype the assembly engine core (catalog schema, sockets, grid, rules, stats) with a
   few test parts and JSON save.
4. After the check-M3 / Application chantier: model `M0_ShipBuilder.jsonld` through the
   instance pipeline.
