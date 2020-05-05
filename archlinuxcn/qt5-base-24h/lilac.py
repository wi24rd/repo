# Trimmed lilac.py
#!/usr/bin/env python3

from types import SimpleNamespace

from lilaclib import *

g = SimpleNamespace()

#build_prefix = 'extra-x86_64'

def pre_build():
  g.files = download_official_pkgbuild('qt5-base')

  prepare = False
  checks = ''
  for line in edit_file('PKGBUILD'):
    if line.startswith('pkgbase='):
      line = 'pkgbase=qt5-base-24h' + '\n' + '_origpkgname=qt5-base'
      checks = checks + '0'
    elif line.startswith('pkgname='):
      line = 'pkgname=(qt5-base)'
      checks = checks + '1'
    elif line.startswith('pkgdesc='):
      line = "pkgdesc='A cross-platform application and UI framework. This package uses 24-hour notation in all locales.'"
      checks = checks + 'b'
    elif line.startswith('makedepends=('):
      line = line.replace('(', "('python2' ")
      checks = checks + '2'
    elif line.startswith('conflicts=('):
      line.replace('(', '("qt5-base" ')
      checks = checks + '3'
    elif line.startswith('groups=('):
      line = '''
provides=("qt5-base=$pkgver")
''' + line
      checks = checks + '4'
    elif line.startswith('_pkgfqn='):
      line = line.replace('${pkgbase/5-/}', '${_origpkgname/5-/}')
      checks = checks + '5'
    elif line.startswith('source=('):
      line = line.replace('=(', '''=(
      oldherl-24h.patch
      'ftp://unicode.org/Public/cldr/36/core.zip'
      ''')
      checks = checks + '6'
    elif line.startswith('sha256sums=('):
      line = line.replace('=(', '''=(
      '8265146554cea16ef94df3f21e4597a1e9c0a9b52b278348a98de14dd7611606'
      '07279e56c1f4266d140b907ef3ec379dce0a99542303a9628562ac5fe460ba43'
      ''')
      checks = checks + '7'
    elif line.startswith('prepare('):
      prepare = True
      checks = checks + '8'
    elif prepare and line.startswith('}'):
      line = '''
  patch -p1 -i ../oldherl-24h.patch
  cd util/locale_database
  echo "This is slow. It takes about 4 minutes on my desktop."
  ./cldr2qlocalexml.py ../../../common/main > ./24h.xml
  ./qlocalexml2cpp.py ./24h.xml ../..
      ''' + line
      prepare = False
      checks = checks + '9'
    elif line.startswith('package_qt5-base('):
      line.replace('qt5-base', 'qt5-base-24h')
      checks = checks + 'a'
    print(line)
  if len(checks) != 12:
    raise ValueError('PKGBUILD editing not completed. checks=' + checks)

def post_build():
  git_add_files(g.files)
  git_commit()

#if __name__ == '__main__':
#  single_main()