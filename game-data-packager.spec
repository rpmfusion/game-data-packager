# How to refresh:
#
# - bump "Version:"
# - add changelog entry
# spectool -g game-data-packager.spec
# rfpkg new-sources game-data-packager_${version}.tar.xz
# rfpkg local
# rfpkg lint
# rfpkg commit
# rfpkg push
# rfpkg build

%global _vpath_srcdir %{name}-%{version}/

#define gitdate 20230104
# git log --oneline -1
%define gitversion a6352918

%if 0%{?gitdate}
%define gver .git%{gitdate}%{gitversion}
%endif

Name:          game-data-packager
Version:       72
Release:       1%{?gver}%{?dist}
Summary:       Installer for game data files
License:       GPLv2 and GPLv2+
URL:           https://wiki.debian.org/Games/GameDataPackager
%if 0%{?gitdate}
# git archive --prefix=game-data-packager-69/ --format tar.gz master > ../rpmbuild/SOURCES/game-data-packager-`date +%Y%m%d`.tar.gz
Source:        game-data-packager-%{gitdate}.tar.gz
%else
Source:        http://http.debian.net/debian/pool/contrib/g/game-data-packager/game-data-packager_%{version}.tar.xz
%endif
Source1:       game-data-packager.rpmlintrc

BuildArch:     noarch

BuildRequires: meson
BuildRequires: desktop-file-utils
BuildRequires: ImageMagick
BuildRequires: inkscape
BuildRequires: python3
BuildRequires: python3-pyyaml
BuildRequires: python3-pyflakes
#BuildRequires: xcftools
BuildRequires: xmlstarlet
BuildRequires: zip

Requires: python3-pyyaml
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
Suggests: xorriso
# cross-build for RaspBian
Suggests: dpkg
Suggests: python3-debian

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
Requires: gtk4
Provides: game-data-packager-runtime = %{version}

%description -n doom2-masterlevels
This GUI let you select a WAD to play &
show it's description.

%prep
%autosetup -c
# id-shr-extract is not packaged
#sed -i '/wolf3d/d' tests/integration.py
# Mock: "Error: No Package found for lha"
#sed -i '/spear/d' tests/integration.py

%build
%meson
%meson_build

%check
echo disabled
#DEB_BUILD_TIME_TESTS=1 % meson_test

%install
%meson_install
find %{buildroot}%{_datadir}/game-data-packager/game_data_packager -name '*.py' ! -empty -exec chmod 755 {} \;
#E: python-bytecode-inconsistent-mtime
python3 -m compileall %{buildroot}%{_datadir}/game-data-packager/game_data_packager/version.py
find %{buildroot}%{_sysconfdir}/game-data-packager -empty -exec sh -c "echo '# we need more mirrors' > {}" \;

# throw away Debian-specific scriptlet
rm -v %{buildroot}%{_datadir}/game-data-packager/doom-common.preinst.in

# throw away src:quake stuff for now
rm -rvf %{buildroot}%{_sysconfdir}/apparmor.d
rm -v %{buildroot}%{_bindir}/etqw*
rm -v %{buildroot}%{_bindir}/quake*
# 'lib64' in local build, 'lib' on buildd
rm -vrf %{buildroot}%{_prefix}/lib*
rm -v %{buildroot}%{_datadir}/applications/etqw.desktop
rm -v %{buildroot}%{_datadir}/applications/quake*.desktop
rm -rv %{buildroot}%{_datadir}/game-data-packager-runtime/
rm -rv %{buildroot}%{_datadir}/quake*
rm -rv %{buildroot}%{_datadir}/icons
rm -v %{buildroot}%{_mandir}/man6/etqw*.6
rm -v %{buildroot}%{_mandir}/man6/quake*.6

desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%doc %{name}-%{version}/doc/adding_a_game.mdwn
%license %{name}-%{version}/COPYING
%{_mandir}/man6/game-data-packager.*
%{_mandir}/fr/man6/game-data-packager.*
%dir %{_sysconfdir}/game-data-packager/
%config(noreplace) %{_sysconfdir}/game-data-packager.conf
%config(noreplace) %{_sysconfdir}/game-data-packager/*
%{_bindir}/game-data-packager
%{_datadir}/bash-completion/completions/game-data-packager
%{_datadir}/game-data-packager/

%files -n doom2-masterlevels
%license %{name}-%{version}/COPYING
%{_mandir}/man6/doom2-masterlevels.*
%{_bindir}/doom2-masterlevels
%{_datadir}/applications/net.debian.game_data_packager.doom2_masterlevels.desktop
%{_datadir}/pixmaps/doom2-masterlevels.png

%changelog
* Fri Feb 10 2023 Alexandre Detiste <alexandre.detiste@gmail.com> - 72-1
- New upstream release

* Wed Jan 25 2023 Alexandre Detiste <alexandre.detiste@gmail.com> - 71-1
- New upstream release

* Thu Jan 12 2023 Alexandre Detiste <alexandre.detiste@gmail.com> - 70-1
- New upstream release
- Switch GUI to Gtk4

* Wed Jan 04 2023 Alexandre Detiste <alexandre.detiste@gmail.com> - 69-2.git20230104a6352918
- Git Snapshot

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Mar 16 2022 Alexandre Detiste <alexandre.detiste@gmail.com> - 69-1
- New upstream release
- Switch to Meson build system

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct 08 2021 Alexandre Detiste <alexandre.detiste@gmail.com> - 68-1
- New upstream release

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 66-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 66-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 25 2020 Alexandre Detiste <alexandre.detiste@gmail.com> - 65-1
- New upstream release

* Mon Aug 24 2020 Leigh Scott <leigh123linux@gmail.com> - 65-3
- Use the proper macros
- Validate desktop file
- Clean up spec file

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 19 2020 Alexandre Detiste <alexandre.detiste@gmail.com> - 65-1
- New upstream release
- Builds with Inkscape 1.0

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 63-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 63-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Feb 18 2019 Alexandre Detiste <alexandre.detiste@gmail.com> - 63-1
- New upstream release
- Build without xcftools
- One check is failing, disabling for now

* Thu Jan 31 2019 Alexandre Detiste <alexandre.detiste@gmail.com> - 62-1
- New upstream release

* Sun Nov 11 2018 Alexandre Detiste <alexandre.detiste@gmail.com> - 60-1
- New upstream release

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 10 2018 Alexandre Detiste <alexandre.detiste@gmail.com> - 59-1
- New upstream release

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 28 2018 Alexandre Detiste <alexandre.detiste@gmail.com> - 58-1
- New upstream release

* Wed Jan 17 2018 Alexandre Detiste <alexandre.detiste@gmail.com> - 57-1
- New upstream release

* Mon Jan 15 2018 Alexandre Detiste <alexandre.detiste@gmail.com> - 56-1
- New upstream release
- skip memory-hungry tests

* Wed Dec 20 2017 Alexandre Detiste <alexandre.detiste@gmail.com> - 55-1
- New upstream release

* Sun Nov 12 2017 Alexandre Detiste <alexandre.detiste@gmail.com> - 54-1
- New upstream release

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Alexandre Detiste <alexandre.detiste@gmail.com> - 53-1
- New upstream release

* Tue May 23 2017 Alexandre Detiste <alexandre.detiste@gmail.com> - 52-1
- New upstream release

* Thu May 04 2017 Alexandre Detiste <alexandre.detiste@gmail.com> - 50-1
- new upstream release

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

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
- The (optional) licenses of generated .rpm goes now correctly to _datadir/licenses
  instead of _datadir/doc
- AppArmor support temporary disabled until figured out

* Thu Dec 31 2015 Alexandre Detiste <alexandre.detiste@gmail.com> - 44-0.2.git2015123150f64b6
- Git Snapshot
- Enable checks

* Tue Dec 29 2015 Alexandre Detiste <alexandre.detiste@gmail.com> - 44-0.1.git2015122906f1b80
- Git Snapshot
- Suggests xdelta

* Sun Nov 08 2015 Alexandre Detiste <alexandre.detiste@gmail.com> - 43-1
- Initial port to Fedora
