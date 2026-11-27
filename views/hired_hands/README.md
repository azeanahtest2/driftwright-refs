# Hired hands: concepts (27 Nov 2026)

For the Anvilhawk's hired hands (Fleet Voyages `docs/handoff/2026-11-26-hired-hands-for-art-design.md`; Aaron, 26 Nov 12:39: "artwork can be lower quality but animations should be comparable"). Step 5 of WP-A2 in the crew animation plan; Aaron, 27 Nov 16:15: "proceed. approved".

- `concept_A.png`, `concept_B.png`: GPT Image 2, image2image, low, 2K (OpenArt E6tmgMfZmRfNf8EDqW87: A ZtCdERDYv36Lnecvjntd, B alciMO1urqdA7BM5SO1k), from the approved round 162 crew concepts (the Bartender TlMwyUBNyxnmPpWUNact, the Boilermaker xxESIiOXgYuwxkzzXyaY) and their A-pose reference. Left to right: the maintenance hand (rust-orange overalls, tool pack), the nurse (off-white smock, red band, kit bag), the security hand (dark plate over a padded coat, blaster at the hip). Plainer than the named crew, one family look.
- Both drew a red cross on the nurse's bag, which wasn't asked for and is a protected emblem: to be replaced with a plain red band or patch in the model sheet.

Made for: the Anvilhawk's twelve spare berths (Fleet Voyages `scripts/hands.gd`). Awaiting Aaron's pick.

Aaron picked **A**. Model sheets (GPT Image 2, low, 2K; OpenArt maintenance dGlOi5qYqpLFrVLqsKDQ / TRLZWFus7NUp7CAaUQNH, nurse dRQtsWVgQFejnkfjqc5D / sFqVWPH89f7jQ1RUc3xi with the cross replaced by a plain red band, security FDIsY96nwsdw8CZL93TU / zRtrQ2staNE3UWZsNbiQ), from concept A and the crew's A-pose reference: `views/hand_maintenance/`, `views/hand_nurse/`, `views/hand_security/` (sheet, front, back, concept). Front and back go to Tripo with the round 162 crew's settings.

## Direction changed (Aaron, 27 Nov 16:21), before any Tripo spend

Aaron: "It should be noted to use the leather under-model and various suits should be crafted and applied for each. We already have security armor in the game with game pieces. The others need to follow suit. we can add mechanics for what they start with and upgrade paths with the armor and equipment settings that we have started"

So the hands are not separate whole-body builds: each is body D (`base_body`, Mixamo-rigged, idle and walk) in the Leather set (round 59, `leather5_whole` split into cap, jerkin, gloves, breeches, boots), with a department suit on top, split into the same slots through `ArmourFit`. The security hand wears the Security set as it is. The maintenance and nurse suits are new sets to draw on body D (the looks in concept A and the model sheets here are their starting point). No rigs needed: body D already animates. The `hand_*` model sheets are kept as look references only; nothing was sent to Tripo.

Aaron, 16:24 picks: start kit "Leather plus a department piece"; new suits "Maintenance and Medic".

- `suit_maintenance.png`, `suit_medic.png`: Nano Banana 2, image2image, 1K, on body D (`views/base_body/front.png`) over the Leather set (`views/leather7_whole/`), looks from concept A (OpenArt maintenance YQmxy58kcHdDv4EYJuEy then fix IRW16XI2SoKHjGPmbkw5 = jghU8GSNUjIAZmeVXfry; medic pLs42qswFEcKiGGWo5tG then fix iYdxx0xtBdXetUwsfygu = NwfSkHS6b3c1O8SEBR5i: the cross, the cap and a backpack removed from the back view). Pieces: chest (overalls bib or smock, with shoulder plates), arm plates, belt, leg pieces with knee pads, back module (tool pack) or kit bag. Open: the medic's back view shows the Leather breeches and boots, the front iron knee pads and boots. Awaiting Aaron.
