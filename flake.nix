{
  description = "Procedurally generated seamless wallpapers";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, ... } @ inputs:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = import ./shell.nix { inherit pkgs; };
      packages.${system} = import ./pkgs { inherit pkgs; };
      checks.${system} = {
        pychecks = pkgs.runCommand "pychecks"
          {
            buildInputs = [
              (pkgs.python3.withPackages (python-pkgs: [
                python-pkgs.black
                python-pkgs.flake8
                python-pkgs.flake8-docstrings
                python-pkgs.mypy
                python-pkgs.pytest
                python-pkgs.sympy
              ]))
            ];
            src = self;
          }
          ''
            # FIXME: occasionally, Nix fails with
            # error: boost::bad_format_string: format-string is ill-formed
            # The root cause has not yet been identified.
            # Possible related bugs:
            # https://github.com/NixOS/nix/issues/8761
            # https://github.com/NixOS/nix/issues/9204

            export PYTHONPATH="$PYTHONPATH:$src/scripts"
            mkdir "$out"
            mypy --config-file "$src/pyproject.toml" \
              "$src/scripts"/*.py "$src/tests"/*.py
            pytest "$src/tests"
            flake8 "$src/scripts" "$src/tests"
            black --check "$src/scripts" "$src/tests"
          '';
      };
      formatter.${system} = pkgs.nixpkgs-fmt;
    };
}
