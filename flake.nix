{
  description = "Application packaged using poetry2nix";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    {
      # Nixpkgs overlay providing the application
      overlay = nixpkgs.lib.composeManyExtensions [
        poetry2nix.overlay
        (final: prev: {
          # The application
          pdme = prev.poetry2nix.mkPoetryApplication {
            overrides = [
              prev.poetry2nix.defaultPoetryOverrides
            ];
            projectDir = ./.;
          };
          pdmeEnv = prev.poetry2nix.mkPoetryEnv {
            overrides = [
              prev.poetry2nix.defaultPoetryOverrides
            ];
            projectDir = ./.;
          };
        })
      ];
    } // (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlay ];
        };
      in
      {
        apps = {
          pdme = pkgs.pdme;
        };

        defaultApp = pkgs.pdme;
        devShell = pkgs.mkShell {
          buildInputs = [
            pkgs.poetry
            pkgs.pdmeEnv
            pkgs.pdme
          ];
        };

      }));
}
