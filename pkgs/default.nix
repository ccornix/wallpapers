{ pkgs ? import <nixpkgs> { }, ... }:

let
  inherit (pkgs) lib;
  mkPkg = name: pkgs.callPackage ./wallpaper.nix { inherit name; };
in
lib.genAttrs [
  "hexagons"
  "gosperflakes2"
  "kochflakes3"
]
  mkPkg
