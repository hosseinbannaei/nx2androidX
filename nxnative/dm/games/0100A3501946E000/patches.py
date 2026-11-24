# OCTOPATH TRAVELER II 1.1.1: build-keyed allocator replacement for the host's Unreal heap.
# Reference: seedds/nxnative 16f4889192dd9bc6363a77b5d8b9654fe65441a2, dm/games/0100A3501946E000/patches.py
# (brought here through shirai91/nx2android PR #484). These original bytes are asserted by the rewriter.
# GCreateMalloc creates a 0x1c38-byte object and calls FMallocBinned3's constructor, which carves its pools
# out of the engine's address region: with the region capped at 2 GB (game.tsv game_args) the original
# allocator cannot work. Skip that constructor call; OBS_UE_MALLOC then installs the host allocator's vtable
# in the object through x19 before anything calls it (hle_uemalloc.c, layout UE4_27 from ue_malloc.tsv).
# The rewriter refuses the file unless the original bytes below match this main build exactly.
CUTS = {
    '0d9649011312f62e93f6a5673a09d7e9': [
        (0xbecc08, 'dc820194', '1f2003d5', 'GCreateMalloc: bl 0xc4d778 (FMallocBinned3 constructor) -> nop; the gate right after it installs the host allocator'),
    ],
}
OBS = {
    '0d9649011312f62e93f6a5673a09d7e9': [
        (0xbecc0c, 21, 'aa1303e0', 'GCreateMalloc: OBS_UE_MALLOC takes the new allocator object from x19; original mov x0, x19'),
    ],
}
