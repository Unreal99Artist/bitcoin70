%define bdbv 4.8.30
%global selinux_variants mls strict targeted

%if 0%{?_no_gui:1}
%define _buildqt 0
%define buildargs --with-gui=no
%else
%define _buildqt 1
%if 0%{?_use_qt4}
%define buildargs --with-qrencode --with-gui=qt4
%else
%define buildargs --with-qrencode --with-gui=qt5
%endif
%endif

Name:		btc69
Version:	0.12.0
Release:	2%{?dist}
Summary:	Peer to Peer Cryptographic Currency

Group:		Applications/System
License:	MIT
URL:		https://btc69crypto.com
Source0:	https://btc69crypto.com/bin/btc69-core-%{version}/btc69-%{version}.tar.gz
Source1:	http://download.oracle.com/berkeley-db/db-%{bdbv}.NC.tar.gz

Source10:	https://raw.githubusercontent.com/btc69/btc69/v%{version}/contrib/debian/examples/btc69.conf

#man pages
Source20:	https://raw.githubusercontent.com/btc69/btc69/v%{version}/doc/man/btc69d.1
Source21:	https://raw.githubusercontent.com/btc69/btc69/v%{version}/doc/man/btc69-cli.1
Source22:	https://raw.githubusercontent.com/btc69/btc69/v%{version}/doc/man/btc69-qt.1

#selinux
Source30:	https://raw.githubusercontent.com/btc69/btc69/v%{version}/contrib/rpm/btc69.te
# Source31 - what about btc69-tx and bench_btc69 ???
Source31:	https://raw.githubusercontent.com/btc69/btc69/v%{version}/contrib/rpm/btc69.fc
Source32:	https://raw.githubusercontent.com/btc69/btc69/v%{version}/contrib/rpm/btc69.if

Source100:	https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin69.svg

%if 0%{?_use_libressl:1}
BuildRequires:	libressl-devel
%else
BuildRequires:	openssl-devel
%endif
BuildRequires:	boost-devel
BuildRequires:	miniupnpc-devel
BuildRequires:	autoconf automake libtool
BuildRequires:	libevent-devel


Patch0:		btc69-0.12.0-libressl.patch


%description
Bitcoin69 is a digital cryptographic currency that uses peer-to-peer technology to
operate with no central authority or banks; managing transactions and the
issuing of btc69 is carried out collectively by the network.

%if %{_buildqt}
%package core
Summary:	Peer to Peer Cryptographic Currency
Group:		Applications/System
Obsoletes:	%{name} < %{version}-%{release}
Provides:	%{name} = %{version}-%{release}
%if 0%{?_use_qt4}
BuildRequires:	qt-devel
%else
BuildRequires:	qt5-qtbase-devel
# for /usr/bin/lrelease-qt5
BuildRequires:	qt5-linguist
%endif
BuildRequires:	protobuf-devel
BuildRequires:	qrencode-devel
BuildRequires:	%{_bindir}/desktop-file-validate
# for icon generation from SVG
BuildRequires:	%{_bindir}/inkscape
BuildRequires:	%{_bindir}/convert

%description core
Bitcoin69 is a digital cryptographic currency that uses peer-to-peer technology to
operate with no central authority or banks; managing transactions and the
issuing of btc69 is carried out collectively by the network.

This package contains the Qt based graphical client and node. If you are looking
to run a Bitcoin69 wallet, this is probably the package you want.
%endif


%package libs
Summary:	Bitcoin69 shared libraries
Group:		System Environment/Libraries

%description libs
This package provides the btc69consensus shared libraries. These libraries
may be used by third party software to provide consensus verification
functionality.

Unless you know need this package, you probably do not.

%package devel
Summary:	Development files for btc69
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the header files and static library for the
btc69consensus shared library. If you are developing or compiling software
that wants to link against that library, then you need this package installed.

Most people do not need this package installed.

%package server
Summary:	The btc69 daemon
Group:		System Environment/Daemons
Requires:	btc69-utils = %{version}-%{release}
Requires:	selinux-policy policycoreutils-python
Requires(pre):	shadow-utils
Requires(post):	%{_sbindir}/semodule %{_sbindir}/restorecon %{_sbindir}/fixfiles %{_sbindir}/sestatus
Requires(postun):	%{_sbindir}/semodule %{_sbindir}/restorecon %{_sbindir}/fixfiles %{_sbindir}/sestatus
BuildRequires:	systemd
BuildRequires:	checkpolicy
BuildRequires:	%{_datadir}/selinux/devel/Makefile

%description server
This package provides a stand-alone btc69-core daemon. For most users, this
package is only needed if they need a full-node without the graphical client.

Some third party wallet software will want this package to provide the actual
btc69-core node they use to connect to the network.

If you use the graphical btc69-core client then you almost certainly do not
need this package.

%package utils
Summary:	Bitcoin69 utilities
Group:		Applications/System

%description utils
This package provides several command line utilities for interacting with a
btc69-core daemon.

The btc69-cli utility allows you to communicate and control a btc69 daemon
over RPC, the btc69-tx utility allows you to create a custom transaction, and
the bench_btc69 utility can be used to perform some benchmarks.

This package contains utilities needed by the btc69-server package.


%prep
%setup -q
%patch0 -p1 -b .libressl
cp -p %{SOURCE10} ./btc69.conf.example
tar -zxf %{SOURCE1}
cp -p db-%{bdbv}.NC/LICENSE ./db-%{bdbv}.NC-LICENSE
mkdir db4 SELinux
cp -p %{SOURCE30} %{SOURCE31} %{SOURCE32} SELinux/


%build
CWD=`pwd`
cd db-%{bdbv}.NC/build_unix/
../dist/configure --enable-cxx --disable-shared --with-pic --prefix=${CWD}/db4
make install
cd ../..

./autogen.sh
%configure LDFLAGS="-L${CWD}/db4/lib/" CPPFLAGS="-I${CWD}/db4/include/" --with-miniupnpc --enable-glibc-back-compat %{buildargs}
make %{?_smp_mflags}

pushd SELinux
for selinuxvariant in %{selinux_variants}; do
	make NAME=${selinuxvariant} -f %{_datadir}/selinux/devel/Makefile
	mv btc69.pp btc69.pp.${selinuxvariant}
	make NAME=${selinuxvariant} -f %{_datadir}/selinux/devel/Makefile clean
done
popd


%install
make install DESTDIR=%{buildroot}

mkdir -p -m755 %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/btc69d %{buildroot}%{_sbindir}/btc69d

# systemd stuff
mkdir -p %{buildroot}%{_tmpfilesdir}
cat <<EOF > %{buildroot}%{_tmpfilesdir}/btc69.conf
d /run/btc69d 0750 btc69 btc69 -
EOF
touch -a -m -t 201504280000 %{buildroot}%{_tmpfilesdir}/btc69.conf

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/btc69
# Provide options to the btc69 daemon here, for example
# OPTIONS="-testnet -disable-wallet"

OPTIONS=""

# System service defaults.
# Don't change these unless you know what you're doing.
CONFIG_FILE="%{_sysconfdir}/btc69/btc69.conf"
DATA_DIR="%{_localstatedir}/lib/btc69"
PID_FILE="/run/btc69d/btc69d.pid"
EOF
touch -a -m -t 201504280000 %{buildroot}%{_sysconfdir}/sysconfig/btc69

mkdir -p %{buildroot}%{_unitdir}
cat <<EOF > %{buildroot}%{_unitdir}/btc69.service
[Unit]
Description=Bitcoin69 daemon
After=syslog.target network.target

[Service]
Type=forking
ExecStart=%{_sbindir}/btc69d -daemon -conf=\${CONFIG_FILE} -datadir=\${DATA_DIR} -pid=\${PID_FILE} \$OPTIONS
EnvironmentFile=%{_sysconfdir}/sysconfig/btc69
User=btc69
Group=btc69

Restart=on-failure
PrivateTmp=true
TimeoutStopSec=120
TimeoutStartSec=60
StartLimitInterval=240
StartLimitBurst=5

[Install]
WantedBy=multi-user.target
EOF
touch -a -m -t 201504280000 %{buildroot}%{_unitdir}/btc69.service
#end systemd stuff

mkdir %{buildroot}%{_sysconfdir}/btc69
mkdir -p %{buildroot}%{_localstatedir}/lib/btc69

#SELinux
for selinuxvariant in %{selinux_variants}; do
	install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
	install -p -m 644 SELinux/btc69.pp.${selinuxvariant} %{buildroot}%{_datadir}/selinux/${selinuxvariant}/btc69.pp
done

%if %{_buildqt}
# qt icons
install -D -p share/pixmaps/btc69.ico %{buildroot}%{_datadir}/pixmaps/btc69.ico
install -p share/pixmaps/nsis-header.bmp %{buildroot}%{_datadir}/pixmaps/
install -p share/pixmaps/nsis-wizard.bmp %{buildroot}%{_datadir}/pixmaps/
install -p %{SOURCE100} %{buildroot}%{_datadir}/pixmaps/btc69.svg
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/btc6916.png -w16 -h16
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/btc6932.png -w32 -h32
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/btc6964.png -w64 -h64
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/btc69128.png -w128 -h128
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/btc69256.png -w256 -h256
%{_bindir}/convert -resize 16x16 %{buildroot}%{_datadir}/pixmaps/btc69256.png %{buildroot}%{_datadir}/pixmaps/btc6916.xpm
%{_bindir}/convert -resize 32x32 %{buildroot}%{_datadir}/pixmaps/btc69256.png %{buildroot}%{_datadir}/pixmaps/btc6932.xpm
%{_bindir}/convert -resize 64x64 %{buildroot}%{_datadir}/pixmaps/btc69256.png %{buildroot}%{_datadir}/pixmaps/btc6964.xpm
%{_bindir}/convert -resize 128x128 %{buildroot}%{_datadir}/pixmaps/btc69256.png %{buildroot}%{_datadir}/pixmaps/btc69128.xpm
%{_bindir}/convert %{buildroot}%{_datadir}/pixmaps/btc69256.png %{buildroot}%{_datadir}/pixmaps/btc69256.xpm
touch %{buildroot}%{_datadir}/pixmaps/*.png -r %{SOURCE100}
touch %{buildroot}%{_datadir}/pixmaps/*.xpm -r %{SOURCE100}

# Desktop File - change the touch timestamp if modifying
mkdir -p %{buildroot}%{_datadir}/applications
cat <<EOF > %{buildroot}%{_datadir}/applications/btc69-core.desktop
[Desktop Entry]
Encoding=UTF-8
Name=Bitcoin69
Comment=Bitcoin69 P2P Cryptocurrency
Comment[fr]=Bitcoin69, monnaie virtuelle cryptographique pair à pair
Comment[tr]=Bitcoin69, eşten eşe kriptografik sanal para birimi
Exec=btc69-qt %u
Terminal=false
Type=Application
Icon=btc69128
MimeType=x-scheme-handler/btc69;
Categories=Office;Finance;
EOF
# change touch date when modifying desktop
touch -a -m -t 201511100546 %{buildroot}%{_datadir}/applications/btc69-core.desktop
%{_bindir}/desktop-file-validate %{buildroot}%{_datadir}/applications/btc69-core.desktop

# KDE protocol - change the touch timestamp if modifying
mkdir -p %{buildroot}%{_datadir}/kde4/services
cat <<EOF > %{buildroot}%{_datadir}/kde4/services/btc69-core.protocol
[Protocol]
exec=btc69-qt '%u'
protocol=btc69
input=none
output=none
helper=true
listing=
reading=false
writing=false
makedir=false
deleting=false
EOF
# change touch date when modifying protocol
touch -a -m -t 201511100546 %{buildroot}%{_datadir}/kde4/services/btc69-core.protocol
%endif

# man pages
install -D -p %{SOURCE20} %{buildroot}%{_mandir}/man1/btc69d.1
install -p %{SOURCE21} %{buildroot}%{_mandir}/man1/btc69-cli.1
%if %{_buildqt}
install -p %{SOURCE22} %{buildroot}%{_mandir}/man1/btc69-qt.1
%endif

# nuke these, we do extensive testing of binaries in %%check before packaging
rm -f %{buildroot}%{_bindir}/test_*

%check
make check
srcdir=src test/btc69-util-test.py
test/functional/test_runner.py --extended

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%pre server
getent group btc69 >/dev/null || groupadd -r btc69
getent passwd btc69 >/dev/null ||
	useradd -r -g btc69 -d /var/lib/btc69 -s /sbin/nologin \
	-c "Bitcoin69 wallet server" btc69
exit 0

%post server
%systemd_post btc69.service
# SELinux
if [ `%{_sbindir}/sestatus |grep -c "disabled"` -eq 0 ]; then
for selinuxvariant in %{selinux_variants}; do
	%{_sbindir}/semodule -s ${selinuxvariant} -i %{_datadir}/selinux/${selinuxvariant}/btc69.pp &> /dev/null || :
done
%{_sbindir}/semanage port -a -t btc69_port_t -p tcp 8766
%{_sbindir}/semanage port -a -t btc69_port_t -p tcp 8767
%{_sbindir}/semanage port -a -t btc69_port_t -p tcp 18766
%{_sbindir}/semanage port -a -t btc69_port_t -p tcp 18767
%{_sbindir}/semanage port -a -t btc69_port_t -p tcp 18443
%{_sbindir}/semanage port -a -t btc69_port_t -p tcp 18444
%{_sbindir}/fixfiles -R btc69-server restore &> /dev/null || :
%{_sbindir}/restorecon -R %{_localstatedir}/lib/btc69 || :
fi

%posttrans server
%{_bindir}/systemd-tmpfiles --create

%preun server
%systemd_preun btc69.service

%postun server
%systemd_postun btc69.service
# SELinux
if [ $1 -eq 0 ]; then
	if [ `%{_sbindir}/sestatus |grep -c "disabled"` -eq 0 ]; then
	%{_sbindir}/semanage port -d -p tcp 8766
	%{_sbindir}/semanage port -d -p tcp 8767
	%{_sbindir}/semanage port -d -p tcp 18766
	%{_sbindir}/semanage port -d -p tcp 18767
	%{_sbindir}/semanage port -d -p tcp 18443
	%{_sbindir}/semanage port -d -p tcp 18444
	for selinuxvariant in %{selinux_variants}; do
		%{_sbindir}/semodule -s ${selinuxvariant} -r btc69 &> /dev/null || :
	done
	%{_sbindir}/fixfiles -R btc69-server restore &> /dev/null || :
	[ -d %{_localstatedir}/lib/btc69 ] && \
		%{_sbindir}/restorecon -R %{_localstatedir}/lib/btc69 &> /dev/null || :
	fi
fi

%clean
rm -rf %{buildroot}

%if %{_buildqt}
%files core
%defattr(-,root,root,-)
%license COPYING db-%{bdbv}.NC-LICENSE
%doc COPYING btc69.conf.example doc/README.md doc/bips.md doc/files.md doc/multiwallet-qt.md doc/reduce-traffic.md doc/release-notes.md doc/tor.md
%attr(0755,root,root) %{_bindir}/btc69-qt
%attr(0644,root,root) %{_datadir}/applications/btc69-core.desktop
%attr(0644,root,root) %{_datadir}/kde4/services/btc69-core.protocol
%attr(0644,root,root) %{_datadir}/pixmaps/*.ico
%attr(0644,root,root) %{_datadir}/pixmaps/*.bmp
%attr(0644,root,root) %{_datadir}/pixmaps/*.svg
%attr(0644,root,root) %{_datadir}/pixmaps/*.png
%attr(0644,root,root) %{_datadir}/pixmaps/*.xpm
%attr(0644,root,root) %{_mandir}/man1/btc69-qt.1*
%endif

%files libs
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/shared-libraries.md
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/developer-notes.md doc/shared-libraries.md
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files server
%defattr(-,root,root,-)
%license COPYING db-%{bdbv}.NC-LICENSE
%doc COPYING btc69.conf.example doc/README.md doc/REST-interface.md doc/bips.md doc/dnsseed-policy.md doc/files.md doc/reduce-traffic.md doc/release-notes.md doc/tor.md
%attr(0755,root,root) %{_sbindir}/btc69d
%attr(0644,root,root) %{_tmpfilesdir}/btc69.conf
%attr(0644,root,root) %{_unitdir}/btc69.service
%dir %attr(0750,btc69,btc69) %{_sysconfdir}/btc69
%dir %attr(0750,btc69,btc69) %{_localstatedir}/lib/btc69
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/sysconfig/btc69
%attr(0644,root,root) %{_datadir}/selinux/*/*.pp
%attr(0644,root,root) %{_mandir}/man1/btc69d.1*

%files utils
%defattr(-,root,root,-)
%license COPYING
%doc COPYING btc69.conf.example doc/README.md
%attr(0755,root,root) %{_bindir}/btc69-cli
%attr(0755,root,root) %{_bindir}/btc69-tx
%attr(0755,root,root) %{_bindir}/bench_btc69
%attr(0644,root,root) %{_mandir}/man1/btc69-cli.1*



%changelog
* Fri Feb 26 2016 Alice Wonder <buildmaster@librelamp.com> - 0.12.0-2
- Rename Qt package from btc69 to btc69-core
- Make building of the Qt package optional
- When building the Qt package, default to Qt5 but allow building
-  against Qt4
- Only run SELinux stuff in post scripts if it is not set to disabled

* Wed Feb 24 2016 Alice Wonder <buildmaster@librelamp.com> - 0.12.0-1
- Initial spec file for 0.12.0 release

# This spec file is written from scratch but a lot of the packaging decisions are directly
# based upon the 0.11.2 package spec file from https://www.ringingliberty.com/btc69/
