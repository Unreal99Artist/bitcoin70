VERSION=1.0.2.0
rm -rf ./release-linux
mkdir release-linux

cp ./src/btc69d ./release-linux/
cp ./src/btc69-cli ./release-linux/
cp ./src/qt/btc69-qt ./release-linux/
cp ./BTC69COIN_small.png ./release-linux/

cd ./release-linux/
strip btc69d
strip btc69-cli
strip btc69-qt

#==========================================================
# prepare for packaging deb file.

mkdir btc69coin-$VERSION
cd btc69coin-$VERSION
mkdir -p DEBIAN
echo 'Package: btc69coin
Version: '$VERSION'
Section: base 
Priority: optional 
Architecture: all 
Depends:
Maintainer: Bitcoin69
Description: Bitcoin69 coin wallet and service.
' > ./DEBIAN/control
mkdir -p ./usr/local/bin/
cp ../btc69d ./usr/local/bin/
cp ../btc69-cli ./usr/local/bin/
cp ../btc69-qt ./usr/local/bin/

# prepare for desktop shortcut
mkdir -p ./usr/share/icons/
cp ../BTC69COIN_small.png ./usr/share/icons/
mkdir -p ./usr/share/applications/
echo '
#!/usr/bin/env xdg-open

[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Exec=/usr/local/bin/btc69-qt
Name=btc69coin
Comment= btc69 coin wallet
Icon=/usr/share/icons/BTC69COIN_small.png
' > ./usr/share/applications/btc69coin.desktop

cd ../
# build deb file.
dpkg-deb --build btc69coin-$VERSION

#==========================================================
# build rpm package
rm -rf ~/rpmbuild/
mkdir -p ~/rpmbuild/{RPMS,SRPMS,BUILD,SOURCES,SPECS,tmp}

cat <<EOF >~/.rpmmacros
%_topdir   %(echo $HOME)/rpmbuild
%_tmppath  %{_topdir}/tmp
EOF

#prepare for build rpm package.
rm -rf btc69coin-$VERSION
mkdir btc69coin-$VERSION
cd btc69coin-$VERSION

mkdir -p ./usr/bin/
cp ../btc69d ./usr/bin/
cp ../btc69-cli ./usr/bin/
cp ../btc69-qt ./usr/bin/

# prepare for desktop shortcut
mkdir -p ./usr/share/icons/
cp ../BTC69COIN_small.png ./usr/share/icons/
mkdir -p ./usr/share/applications/
echo '
[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Exec=/usr/bin/btc69-qt
Name=btc69coin
Comment= btc69 coin wallet
Icon=/usr/share/icons/BTC69COIN_small.png
' > ./usr/share/applications/btc69coin.desktop
cd ../

# make tar ball to source folder.
tar -zcvf btc69coin-$VERSION.tar.gz ./btc69coin-$VERSION
cp btc69coin-$VERSION.tar.gz ~/rpmbuild/SOURCES/

# build rpm package.
cd ~/rpmbuild

cat <<EOF > SPECS/btc69coin.spec
# Don't try fancy stuff like debuginfo, which is useless on binary-only
# packages. Don't strip binary too
# Be sure buildpolicy set to do nothing

Summary: Bitcoin69 wallet rpm package
Name: btc69coin
Version: $VERSION
Release: 1
License: MIT
SOURCE0 : %{name}-%{version}.tar.gz
URL: https://www.btc69coin.net/

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
%{summary}

%prep
%setup -q

%build
# Empty section.

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}

# in builddir
cp -a * %{buildroot}


%clean
rm -rf %{buildroot}


%files
/usr/share/applications/btc69coin.desktop
/usr/share/icons/BTC69COIN_small.png
%defattr(-,root,root,-)
%{_bindir}/*

%changelog
* Tue Aug 24 2021  Bitcoin69 Project Team.
- First Build

EOF

rpmbuild -ba SPECS/btc69coin.spec



