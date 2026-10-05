// ImageThreading POP — debug view (phase 1): pegs drawn in UV over the image.
//
// Host: GLSL TOP "debug_overlay", pixel shader, input 0 = the image.
//   Buffers page: POP = pegs_uv, class Point, attribute PegUV, name PegUV
//   uniforms: uRadius (float, pixels), uDotColor (vec4)

uniform float uRadius;      // GLSL TOP: uniforms are declared by the shader
uniform vec4 uDotColor;

layout(location = 0) out vec4 fragColor;

void main()
{
    vec4 color = texture(sTD2DInputs[0], vUV.st);
    vec2 res = uTDOutputInfo.res.zw;
    vec2 px = vUV.st * res;

    float d = 1e9;
    uint n = TDBufferLength_PegUV();
    for (uint i = 0u; i < n; i++)
        d = min(d, distance(px, TDBuffer_PegUV(i) * res));

    float a = 1.0 - smoothstep(uRadius - 1.0, uRadius, d);
    fragColor = TDOutputSwizzle(mix(color, vec4(uDotColor.rgb, 1.0), a * uDotColor.a));
}
