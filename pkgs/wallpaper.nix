{ lib
, librsvg
, python3
, stdenvNoCC
, name
, # wallpaper name
  palette ? [ ]
, # new palette colors as a list
  width ? 1920
, # width of the generated PNG
}:

let
  paletteArgs = builtins.concatStringsSep " " (
    map lib.escapeShellArg palette
  );
in
stdenvNoCC.mkDerivation {
  inherit name;
  src = ../.;
  dontUnpack = true;

  nativeBuildInputs = [ python3 ];
  buildInputs = [ librsvg ];
  buildPhase = ''
    python3 "$src/scripts/recolor.py" "$src/wallpapers/${name}.svg" \
      ${paletteArgs} > wallpaper.svg
    rsvg-convert -a -w ${toString width} wallpaper.svg -o wallpaper.png
    # Fallback solution for conversion:
    # inkscape \
    #   --export-type=png \
    #   --export-width=${toString width} \
    #   --export-filename=wallpaper.png \
    #   wallpaper.svg
  '';

  installPhase = ''
    mkdir -p "$out"
    install -Dm0644 wallpaper.svg "$out/wallpaper.svg"
    install -Dm0644 wallpaper.png "$out/wallpaper.png"
  '';
}
