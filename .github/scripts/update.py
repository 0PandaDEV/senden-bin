#!/usr/bin/env python3

import hashlib
from pathlib import Path
import re
import urllib.request


BASE = 'https://senden-releases.objects.eplg.cloud/desktop'
LATEST = f'{BASE}/latest-linux.yml'
ARCHES = {'x86_64': 'senden-electron-{v}.zip', 'aarch64': 'senden-electron-{v}-arm64.zip'}
HEADERS = {'User-Agent': 'senden-aur-updater'}


def open_url(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=300)


def latest_version():
    with open_url(LATEST) as response:
        text = response.read().decode()
    match = re.search(r'^version:\s*[\'"]?(\d+\.\d+\.\d+)[\'"]?\s*$', text, re.MULTILINE)
    if not match:
        raise ValueError('No stable version found in latest-linux.yml')
    return match.group(1)


def checksum(url):
    digest = hashlib.sha256()
    with open_url(url) as response:
        for chunk in iter(lambda: response.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def field(text, name):
    matches = re.findall(rf'^{re.escape(name)}=(.+)$', text, re.MULTILINE)
    if len(matches) != 1:
        raise ValueError(f'Expected exactly one {name} assignment')
    return matches[0]


def parse(version):
    return tuple(map(int, version.split('.')))


def update(text, version):
    current = field(text, 'pkgver')
    if version == current:
        return text
    if parse(version) < parse(current):
        raise ValueError(f'Refusing to downgrade {current} to {version}')

    replacements = {'pkgver': version, 'pkgrel': '1'}
    for arch, name in ARCHES.items():
        replacements[f'sha256sums_{arch}'] = f"('{checksum(f'{BASE}/{name.format(v=version)}')}')"
    for name, value in replacements.items():
        field(text, name)
        text = re.sub(rf'^{re.escape(name)}=.+$', lambda _: f'{name}={value}', text, flags=re.MULTILINE)
    return text


def main():
    path = Path('PKGBUILD')
    current = path.read_text()
    updated = update(current, latest_version())
    if updated == current:
        print('Already up to date.')
    else:
        path.write_text(updated)
        print(f'Updated to {field(updated, "pkgver")}-{field(updated, "pkgrel")}')


if __name__ == '__main__':
    main()
