// ImageThreading POP — helpers shared by the shaders.
// Loaded in the Text DAT "shader_common"; shaders use #include "shader_common".

// Wang hash, bit-identical to wang_hash() in python/reference.py.
uint wangHash(uint x)
{
    x = (x ^ 61u) ^ (x >> 16);
    x *= 9u;
    x = x ^ (x >> 4);
    x *= 0x27D4EB2Du;
    x = x ^ (x >> 15);
    return x;
}

// Tie-break key of candidate `c` at `iteration` (reference.py tie_hash()).
uint tieHash(uint seed, uint iteration, uint c)
{
    return wangHash(wangHash(seed ^ wangHash(iteration)) ^ c);
}

// Path layout (SPEC 5.3): trail t owns path entries [t * M, (t + 1) * M).
int trailLen(int lineCount, int trails)            // M
{
    return (lineCount + trails - 1) / trails + 1;
}

// Segments given to trail t when lineCount segments go round-robin (SPEC 4.6).
int trailSegments(int lineCount, int trails, int t)
{
    return lineCount / trails + (t < lineCount % trails ? 1 : 0);
}

// Counters layout: [0] segments done, [1] iteration, [2 + t] vertex count of
// trail t, [2 + trails + t] trail t is stuck (1) or not (0).
const int cCounterSegments = 0;
const int cCounterIteration = 1;
const int cCounterTrailVerts = 2;
