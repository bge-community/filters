uniform sampler2D bgl_RenderedTexture;

uniform float fade;
uniform vec4 color;

void main()
{
    vec4 imageColor = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);
    gl_FragColor = mix(imageColor, color, fade);
}
