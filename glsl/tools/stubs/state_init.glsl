uint TDIndex() { return gl_GlobalInvocationID.x; }
uint TDNumElements() { return 0u; }
uint TDInputNumPoints(uint inputIndex) { return 0u; }
vec4 TDIn_Color() { return vec4(0.0); }
layout(std430, binding = 0) buffer O0 { float R[]; };
layout(std430, binding = 1) buffer O1 { int Path[]; };
layout(std430, binding = 2) buffer O2 { float Score[]; };
layout(std430, binding = 3) buffer O3 { int Counters[]; };
uniform int uInvert;
uniform int uLineCount;
uniform int uTrails;
uniform int uSeed;
uniform int uDebugRandom;
