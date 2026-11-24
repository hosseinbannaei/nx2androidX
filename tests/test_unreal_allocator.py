"""The Unreal allocator's size rule (nxnative/dm/host/hle_uemalloc.c): a block below 16 bytes must not reach the host allocator, whose smallest class is 8-byte aligned.

The engine reads such a block as 16-byte aligned (PhysX), so a block that lands in the tiny class is a SIGSEGV in a long play (upstream PR #484).
"""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import csrc   # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests/unreal_allocator.c'


@unittest.skipUnless(shutil.which('cc'), 'a C compiler is required')
class UnrealAllocatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temp = tempfile.TemporaryDirectory(prefix='nx2a-unreal-alloc-')
        cls.addClassCleanup(temp.cleanup)
        work = Path(temp.name)
        src = csrc.read('nxnative/dm/host/hle_uemalloc.c')
        body = csrc.between(src, 'static _Atomic int64_t g_used', 'static void *m_Malloc')   # the allocator's own functions
        (work / 'unreal_allocator.c').write_text(FIXTURE.read_text(encoding='utf-8').replace('/* CUT */', body), encoding='utf-8')
        cls.binary = work / 'unreal_allocator'
        subprocess.run(['cc', '-std=gnu11', '-Wall', '-Wextra', '-Werror', str(work / 'unreal_allocator.c'), '-o', str(cls.binary)], check=True, timeout=60)

    def sizes(self):
        out = subprocess.run([str(self.binary)], capture_output=True, text=True, timeout=10)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        return {k: int(v) for k, v in (l.split() for l in out.stdout.splitlines())}

    def test_a_block_below_16_bytes_never_reaches_the_host_allocator(self):
        s = self.sizes()
        self.assertGreaterEqual(s['alloc8'], 16)
        self.assertGreaterEqual(s['alloc0'], 16)
        self.assertGreaterEqual(s['alloc8align32'], 16)
        self.assertGreaterEqual(s['realloc4'], 16)

    def test_a_size_of_its_own_is_untouched(self):
        s = self.sizes()
        self.assertEqual(s['alloc100'], 100)

    def test_the_alignment_the_engine_asks_for_is_untouched(self):
        s = self.sizes()
        self.assertEqual(s['align32'], 32)   # the alignment is the engine's own, the size is the one the host gets


if __name__ == '__main__':
    unittest.main()
