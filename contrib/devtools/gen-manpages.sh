#!/bin/sh

TOPDIR=${TOPDIR:-$(git rev-parse --show-toplevel)}
SRCDIR=${SRCDIR:-$TOPDIR/src}
MANDIR=${MANDIR:-$TOPDIR/doc/man}

BTC69D=${BTC69D:-$SRCDIR/btc69d}
BTC69CLI=${BTC69CLI:-$SRCDIR/btc69-cli}
BTC69TX=${BTC69TX:-$SRCDIR/btc69-tx}
BTC69QT=${BTC69QT:-$SRCDIR/qt/btc69-qt}

[ ! -x $BTC69D ] && echo "$BTC69D not found or not executable." && exit 1

# The autodetected version git tag can screw up manpage output a little bit
btc69VER=($($BTC69CLI --version | head -n1 | awk -F'[ -]' '{ print $6, $7 }'))

# Create a footer file with copyright content.
# This gets autodetected fine for btc69d if --version-string is not set,
# but has different outcomes for btc69-qt and btc69-cli.
echo "[COPYRIGHT]" > footer.h2m
$BTC69D --version | sed -n '1!p' >> footer.h2m

for cmd in $BTC69D $BTC69CLI $BTC69TX $BTC69QT; do
  cmdname="${cmd##*/}"
  help2man -N --version-string=${btc69VER[0]} --include=footer.h2m -o ${MANDIR}/${cmdname}.1 ${cmd}
  sed -i "s/\\\-${btc69VER[1]}//g" ${MANDIR}/${cmdname}.1
done

rm -f footer.h2m
