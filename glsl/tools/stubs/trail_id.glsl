uint TDIndex() { return gl_GlobalInvocationID.x; }
uint TDNumElements() { return 0u; }
layout(std430, binding = 0) buffer O0 { int TrailId[]; };
