uint TDIndex() { return gl_GlobalInvocationID.x; }
uint TDNumElements() { return 0u; }
vec3 TDIn_P() { return vec3(0.0); }
vec3 TDIn_Min(uint inputIndex, uint id) { return vec3(0.0); }
vec3 TDIn_Max(uint inputIndex, uint id) { return vec3(0.0); }
layout(std430, binding = 0) buffer O0 { vec2 PegUV[]; };
uniform int uFit;
uniform int uAspect;
uniform vec2 uScale;
uniform vec2 uOffset;
uniform vec2 uImageRes;
