# senden-bin

AUR packaging for the [Senden](https://senden.chat) desktop client. Packages the
upstream Electron Linux zips for `x86_64` and `aarch64` into `/opt/senden`, with
`senden-electron` and `senden` launchers, a desktop entry and icon.

## Build and install

```sh
makepkg -si
```

Install `libpipewire` and `libpulse` for screen share audio capture, and
`libappindicator-gtk3` for the tray icon.

## Automatic updates

The GitHub Actions workflow runs hourly, on manual dispatch, and when packaging
or automation files change on the default branch. It reads `version` from
[latest-linux.yml](https://senden-releases.objects.eplg.cloud/desktop/latest-linux.yml).
When the version is newer than `pkgver`, it downloads both zips, updates
`pkgver`, resets `pkgrel` and refreshes the SHA-256 sums, then regenerates
`.SRCINFO` with Arch's `makepkg` and pushes the result to AUR. Downgrades and
missing zips fail without changing the package.

To enable publishing:

1. Push this directory to a GitHub repository and enable GitHub Actions.
2. Add an SSH public key to your AUR account and save its private key as the
   repository Actions secret `AUR_SSH_PRIVATE_KEY`.
3. Run **aur-auto-update** from the Actions tab. An empty AUR repository is
   supported for the first submission.

Only `PKGBUILD` and `.SRCINFO` are published to AUR.

Local metadata update:

```sh
python3 .github/scripts/update.py
makepkg --printsrcinfo > .SRCINFO
```
