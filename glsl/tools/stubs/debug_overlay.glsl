uniform sampler2D sTD2DInputs[1];
in vec3 vUV;
struct TDOutInfo { vec4 res; };
uniform TDOutInfo uTDOutputInfo;
vec4 TDOutputSwizzle(vec4 c) { return c; }
uint TDBufferLength_PegUV() { return 0u; }
vec2 TDBuffer_PegUV(uint i) { return vec2(0.0); }
