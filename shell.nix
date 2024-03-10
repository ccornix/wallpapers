{ pkgs ? import <nixpkgs> { }, ... }:

let
  myPython = pkgs.python3.withPackages (python-pkgs: [
    python-pkgs.black
    python-pkgs.flake8
    python-pkgs.ipython
    python-pkgs.mypy
    python-pkgs.pytest
    python-pkgs.sympy
  ]);
in
pkgs.mkShell {
  src = ./.;
  packages = [ myPython pkgs.gitlint ];
  shellHook = ''
    export PYTHONPATH="${myPython}/${myPython.sitePackages}:$src/scripts"
    alias mypy="mypy --config-file $src/pyproject.toml"
  '';
}
