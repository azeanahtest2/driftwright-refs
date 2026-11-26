# The Wagon with Brokkr's bridge and maw (2026-11-26)

Aaron (14:55): "I also want to take the bridge+maw from the brokkr's wake and reduce it all the way down to this extended wagon's concept. I want there to be an upper bridge with a series of claws from the beard that get pulled into the maw, which has an industrial ore catcher and a debris conveyer belt that travel to the rear bay area. the living quarters should be a deck above in the front and have an airlock separation from the bay area"

Source art: Brokkr's Rest 2K views (`views/brokkrs_rest_2k/`, approved round 156): the brow band of windows (bridge), the stone moustache over the maw, five claws on the beard below it. The horns and guns are not carried over.

`map_maw_wagon.png` (from `make_map_maw_wagon.py`), true scale, proposal:
- Hull 23.0 m x 5.5 m x 7.8 m (the 1.18x Wagon of map B, bay trimmed to the hull width), the Explorer docked aft as the tail gun, nose 2 m out.
- Lower deck (floor 1.0 m): the maw (3.6 x 2.6 m), the ore catcher (grate and crusher jaws), a 1.6 m debris conveyor with a service walkway running aft to an ore hopper under the dock deck; engines aft.
- Upper deck (floor 4.0 m): the bridge behind the brow windows, then Joe's rooms in his order (equipment with the side hatches, galley and head, bunks), then an airlock into the rear bay. The dock deck is at 3.5 m, a short step down.
- Five beard claws under the chin, folded when landed, pulled into the maw to feed the catcher.

Aaron (15:04): "I'm amenable to the design. it's loosely what I asked for. / instead of the belt, drive, rollers, bins, etc on the side, put a fabricator, long boiler (like in hammerhead), and other service-level stations that don't belong in the bridge. / Then begin designing"

- Map updated: the conveyor runs along the starboard wall, the walkway down the middle; to port the claw post and hold control post (facing the catcher; FV `brokkr_maw/fv_brokkr_claw_post`, `fv_hold_control_post`), the long boiler (the Hammerhead's forge-pit boiler, `fv_boiler_forge_pit`, 4.5 m lying lengthwise), the fabricator (`fv_fabricator`), parts and tool racks.
- `render_guide_maw.png` (from `make_render_guide_maw.py`, which reads `_render_guide_b_base.py`): true-scale paint-over guide, port side and front, the Brokkr head cut from her 2K left and front views, horns and guns left off.
