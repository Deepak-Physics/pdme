{
  description = "Application packaged using poetry2nix";

  inputs.flake-utils.url = "github:numtide/flake-utils?rev=0f8662f1319ad6abf89b3380dd2722369fc51ade";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs?rev=e194871435cad8ffb1d64b64fb7df3b2b8a10088";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix?rev=99c79568352799af09edaeefc858d337e6d9c56f";

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
          shellHook = ''
            export DO_NIX_CUSTOM=1
          '';
          packages = [ pkgs.nodejs-16_x ];
        };

      }));
}
