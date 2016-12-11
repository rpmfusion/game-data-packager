# How to refresh
#
# 1) bump "Version:"
# 2) add changelog entry
# 3) 'spectool -g game-data-packager.spec'
# 4) rpmbuild -ba game-data-packager.spec
# 5) rfpkg commit
# 6) rfpkg push
# 7) rfpkg build

#define gitdate 20160112
# git log --oneline -1
%define gitversion 50f64b6

%if 0%{?gitdate}
%define gver .git%{gitdate}%{gitversion}
%endif

Name:          game-data-packager
Version:       48
Release:       1%{?gver}%{?dist}
Summary:       Installer for game data files
License:       GPLv2 and GPLv2+
Url:           https://wiki.debian.org/Games/GameDataPackager
%if 0%{?gitdate}
# git archive --prefix=game-data-packager-44/ --format tar.gz master > ../rpmbuild/SOURCES/game-data-packager-`date +%Y%m%d`.tar.gz
Source:        game-data-packager-%{gitdate}.tar.gz
%else
Source:        http://http.debian.net/debian/pool/contrib/g/game-data-packager/game-data-packager_%{version}.tar.xz
%endif
BuildArch:     noarch
BuildRequires: ImageMagick
BuildRequires: inkscape
BuildRequires: python3
BuildRequires: python3-PyYAML
BuildRequires: python3-pyflakes
BuildRequires: xcftools
BuildRequires: xmlstarlet
BuildRequires: zip
Requires: python3-PyYAML
# download
Recommends: lgogdownloader
Suggests: steam
# rip
Suggests: cdparanoia
Suggests: vorbis-tools
# extract
Suggests: arj
Suggests: cabextract
Recommends: innoextract
Suggests: lha
Suggests: p7zip-plugins
Suggests: xdelta
Suggests: unar
Suggests: unrar
Suggests: unshield
Suggests: unzip

%global __python %{__python3}

%description
Various games are divided into two logical parts: engine and data.
.
game-data-packager is a tool which builds .rpm files for game
data which cannot be distributed (such as commercial game data).

%package -n doom2-masterlevels
Summary: "Master Levels for Doom II" launcher
Requires: python3-gobject-base
Requires: gobject-introspection
Provides: game-data-packager-runtime = %{version}
%description -n doom2-masterlevels
This GUI let you select a WAD to play &
show it's description.

%prep
%autosetup
# id-shr-extract is not packaged
sed -i '/wolf3d/d' tests/integration.py
# Mock: "Error: No Package found for lha"
sed -i '/spear/d' tests/integration.py

%build
%configure
make %{?_smp_mflags}

%check
make check

%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT/usr/share/game-data-packager/game_data_packager -name '*.py' -exec chmod 755 {} \;
#E: python-bytecode-inconsistent-mtime
python3 -m compileall $RPM_BUILD_ROOT/usr/share/game-data-packager/game_data_packager/version.py
find $RPM_BUILD_ROOT/etc/game-data-packager -empty -exec sh -c "echo '# we need more mirrors' > {}" \;

# throw away src:quake stuff for now
rm -rvf $RPM_BUILD_ROOT/etc/apparmor.d
rm -v $RPM_BUILD_ROOT/usr/bin/etqw*
rm -v $RPM_BUILD_ROOT/usr/bin/quake*
# 'lib64' in local build, 'lib' on buildd
rm -vrf $RPM_BUILD_ROOT/usr/lib*
rm -v $RPM_BUILD_ROOT/usr/share/applications/etqw.desktop
rm -v $RPM_BUILD_ROOT/usr/share/applications/quake*.desktop
rm -rv $RPM_BUILD_ROOT/usr/share/game-data-packager-runtime/
rm -rv $RPM_BUILD_ROOT/usr/share/quake*
rm -rv $RPM_BUILD_ROOT/usr/share/icons
rm -v $RPM_BUILD_ROOT/usr/share/man/man6/etqw*.6
rm -v $RPM_BUILD_ROOT/usr/share/man/man6/quake*.6

%files
%doc doc/adding_a_game.mdwn
%{_mandir}/man6/game-data-packager.*
%{_mandir}/fr/man6/game-data-packager.*
%config(noreplace) %attr(644, root, root) /etc/game-data-packager.conf
%config(noreplace) %attr(644, root, root) /etc/game-data-packager/*
/usr/bin/game-data-packager
/usr/share/bash-completion/completions/game-data-packager
/usr/share/game-data-packager
%license COPYING

%files -n doom2-masterlevels
%{_mandir}/man6/doom2-masterlevels.*
/usr/bin/doom2-masterlevels
/usr/share/applications/doom2-masterlevels.desktop
/usr/share/pixmaps/doom2-masterlevels.png
%license COPYING

%changelog
* Sun Dec 11 2016 Alexandre Detiste <alexandre.detiste@gmail.com> - 48-1
- new upstream release

* Sun Nov 06 2016 Alexandre Detiste <alexandre.detiste@gmail.com> - 47-1
- new upstream release

* Tue Oct 18 2016 Alexandre Detiste <alexandre.detiste@gmail.com> - 46-1
- new experimental upstream release, don't push to F25/F24 etc...

* Sat Jul 23 2016 Alexandre Detiste <alexandre.detiste@gmail.com> - 45-2
- Inkscape is currently uninstallable, temporary strip out .svg from build

* Fri Jul 22 2016 Alexandre Detiste <alexandre.detiste@gmail.com> - 45-1
- Finally upload to RPMFusion, skip v44

* Sun Jan 24 2016 Alexandre Detiste <alexandre.detiste@gmail.com> - 44-1
- First cross-distribution release
- Add Cacodemon icon to doom2-masterlevels subpackage
- The (optional) licenses of generated .rpm goes now correctly to /usr/share/licenses
  instead of /usr/share/doc
- AppArmor support temporary disabled until figured out

* Thu Dec 31 2015 Alexandre Detiste <alexandre.detiste@gmail.com> - 44-0.2.git2015123150f64b6
- Git Snapshot
- Enable checks

* Tue Dec 29 2015 Alexandre Detiste <alexandre.detiste@gmail.com> - 44-0.1.git2015122906f1b80
- Git Snapshot
- Suggests xdelta

* Sun Nov 08 2015 Alexandre Detiste <alexandre.detiste@gmail.com> - 43-1
- Initial port to Fedora
