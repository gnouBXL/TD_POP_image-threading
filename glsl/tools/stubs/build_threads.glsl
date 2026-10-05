uint TDIndex() { return gl_GlobalInvocationID.x; }
uint TDNumElements() { return 0u; }
int TDInPoint_Counters(uint inputIndex, uint id) { return 0; }
int TDInPoint_Path(uint inputIndex, uint id) { return 0; }
float TDInPoint_Score(uint inputIndex, uint id) { return 0.0; }
vec3 TDInPoint_P(uint inputIndex, uint id) { return vec3(0.0); }
layout(std430, binding = 0) buffer O0 { vec3 oTDPoint_P[]; };
layout(std430, binding = 1) buffer O1 { vec4 oTDPoint_Color[]; };
layout(std430, binding = 2) buffer O2 { float oTDPoint_Score[]; };
layout(std430, binding = 3) buffer O3 { int oTDPoint_PegIndex[]; };
layout(std430, binding = 4) buffer O4 { int oTDPoint_Step[]; };
layout(std430, binding = 5) buffer O5 { float oTDPoint_StepNorm[]; };
layout(std430, binding = 6) buffer O6 { int oTDPoint_LineStripIndex[]; };
uniform int uTrails;
uniform int uTrailLen;
uniform vec4 uColor;
