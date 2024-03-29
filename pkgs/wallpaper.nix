{ lib
, librsvg
, python3
, stdenvNoCC
  # wallpaper name
, name
  # new palette colors as a list (HTML hex color codes without the leading hash
  # mark)
, palette ? [ ]
  # width of the generated PNG
, width ? 1920
}:

let
  paletteArgs = builtins.concatStringsSep " " (map lib.escapeShellArg palette);

  targetDir = "share/backgrounds/ccornix";

  pkg = stdenvNoCC.mkDerivation {
    inherit name;
    src = ../.;
    dontUnpack = true;

    nativeBuildInputs = [ python3 ];
    buildInputs = [ librsvg ];
    buildPhase = ''
      python3 "$src/scripts/recolor.py" "$src/wallpapers/${name}.svg" \
        ${paletteArgs} > ${name}.svg
      rsvg-convert -a -w ${toString width} ${name}.svg -o ${name}.png
    '';

    passthru = {
      filePath = "${pkg}/${targetDir}/${name}.png";
    };

    installPhase = ''
      mkdir -p "$out/${targetDir}"
      install -Dm0644 ${name}.svg "$out/${targetDir}/${name}.svg"
      install -Dm0644 ${name}.png "$out/${targetDir}/${name}.png"
    '';
  };
in pkg
