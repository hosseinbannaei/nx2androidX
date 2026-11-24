// The Unreal allocator's own size rule: a block below 16 bytes must not reach the host allocator, whose smallest class is 8-byte aligned.
// The host allocator is stubbed here, so the harness sees the size the allocator asks for.
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define LOG(...) ((void)0)

typedef struct fake_zone { int unused; } malloc_zone_t;
static malloc_zone_t g_zone_storage;
static malloc_zone_t *g_zone;
static size_t g_slab_size;                      // what the host allocator would report for the block it holds
static size_t g_malloc_n, g_memalign_n, g_memalign_a, g_realloc_n;
static unsigned char g_slab[8192];

static void *malloc_zone_malloc(malloc_zone_t *z, size_t n) { (void)z; g_malloc_n = n; g_slab_size = n; return g_slab; }
static void *malloc_zone_memalign(malloc_zone_t *z, size_t a, size_t n) { (void)z; g_memalign_n = n; g_memalign_a = a; g_slab_size = n; return g_slab; }
static void *malloc_zone_realloc(malloc_zone_t *z, void *p, size_t n) { (void)z; (void)p; g_realloc_n = n; g_slab_size = n; return g_slab; }
static void malloc_zone_free(malloc_zone_t *z, void *p) { (void)z; (void)p; }
static size_t malloc_size(void *p) { (void)p; return g_slab_size; }

/* CUT */

int main(void) {
    g_zone = &g_zone_storage;
    alloc(8, 0);
    printf("alloc8 %zu\n", g_malloc_n);
    alloc(0, 0);
    printf("alloc0 %zu\n", g_malloc_n);
    alloc(100, 0);
    printf("alloc100 %zu\n", g_malloc_n);
    alloc(8, 32);
    printf("alloc8align32 %zu\n", g_memalign_n);
    printf("align32 %zu\n", g_memalign_a);
    g_slab_size = 8;              // a live block in the tiny class
    realloc_aligned(g_slab, 4, 0);
    printf("realloc4 %zu\n", g_realloc_n);
    return 0;
}
