uint TDInputNumPoints(uint inputIndex) { return 0u; }
vec2 TDIn_PegUV(uint inputIndex, uint id) { return vec2(0.0); }
layout(std430, binding = 0) buffer O0 { float R[]; };
layout(std430, binding = 1) buffer O1 { int Path[]; };
layout(std430, binding = 2) buffer O2 { float Score[]; };
layout(std430, binding = 3) buffer O3 { int Counters[]; };
uniform int uK;
uniform int uLineCount;
uniform int uTrails;
uniform int uHistory;
uniform int uSeed;
uniform int uW;
uniform int uH;
uniform float uOpacity;
uniform float uMinDist;
