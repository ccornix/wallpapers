# A collection of procedurally generated seamless geometric wallpapers

The SVG wallpapers in the `wallpapers` directory have been generated using Python code contained in the `scripts` directory. [Nix](https://nixos.org/) packages contained in this [flake](https://nixos.wiki/wiki/Flakes) render PNGs from the pre-generated SVGs, optionally re-colored using a customized palette to match the color scheme of the user's desktop theme.

## Gallery

### Tilings of the plane using randomly colored islands

#### `hexagons`

<a href="https://codeberg.org/ccornix/wallpapers/src/branch/main/wallpapers/hexagons.svg">
  <img src="wallpapers/hexagons.svg" width="960">
</a>

#### `gosperflakes2`

[Gosper islands (snowflakes)](https://mathworld.wolfram.com/GosperIsland.html) (2 iterations)

<a href="https://codeberg.org/ccornix/wallpapers/src/branch/main/wallpapers/gosperflakes2.svg">
  <img src="wallpapers/gosperflakes2.svg" width="960">
</a>

#### `kochflakes3`

[Koch islands (snowflakes)](https://mathworld.wolfram.com/KochSnowflake.html) (3 iterations)

<a href="https://codeberg.org/ccornix/wallpapers/src/branch/main/wallpapers/kochflakes3.svg">
  <img src="wallpapers/kochflakes3.svg" width="960">
</a>

## SVG generation and rendering

Clone this repo using `git`, and enter the repo directory.

Wallpapers with the default palette can be built as follows. Using stable Nix as

```sh
nix-build -E '(import ./pkgs { }).hexagons'
```

while using Flakes-enabled Nix as

```sh
nix build .#hexagons
```

The generated SVG and PNG files are contained within the `result` subdirectory.

The palette can be customized when building, using stable Nix as

```sh
nix-build -E '
(import ./pkgs { }).hexagons.override {
  palette = ["#000000" "#3f1f0f" "#7f3f1f" "#ff7f3f"];
}'
```

while using Flakes-enabled Nix as

```sh
nix build --impure --expr '
(import ./pkgs { }).hexagons.override {
  palette = ["#000000" "#3f1f0f" "#7f3f1f" "#ff7f3f"];
}'
```

## Python development

Clone this repo using `git` and open a development shell inside the repo directory. The latter can be accomplished using stable Nix as

```sh
nix-shell
```

while using Flakes-enabled Nix as

```sh
nix develop
```

## References

The randomly colored hexagonal grid pattern was inspired by paepaestockphoto's artwork at

https://www.vecteezy.com/vector-art/6941002-small-hexagon-shape-with-light-white-and-grey-color-seamless-pattern-background
