set -euo pipefail

aur_dir=$(mktemp -d)
trap 'rm -rf "$aur_dir"' EXIT
git clone "${AUR_REMOTE:-ssh://aur@aur.archlinux.org/senden-bin.git}" "$aur_dir"
git -C "$aur_dir" checkout -B master
install -m644 PKGBUILD .SRCINFO "$aur_dir/"
git -C "$aur_dir" add PKGBUILD .SRCINFO
if git -C "$aur_dir" diff --cached --quiet; then
    echo 'AUR is already up to date.'
    exit 0
fi
version=$(sed -n 's/^pkgver=//p' PKGBUILD)
git -C "$aur_dir" commit -m "chore: update senden to $version"
git -C "$aur_dir" push origin HEAD:master
