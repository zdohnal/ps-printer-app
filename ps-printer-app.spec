# the original SPEC file was created by Brandon Nielsen in his COPR repo and this comment
# is to honor his great contribution - thank you for all you work, Brandon!
#
# Brandon changes are present in Changelog as well to let people know he worked on this SPEC file.

%global forgeurl https://github.com/OpenPrinting/ps-printer-app

%global commit 5dbdece4aa51d9eba85c05151b5dd4de2161d777

%forgemeta

Name: ps-printer-app
Version: 0
Release: 2%{?dist}
# the CUPS exception text is the same as LLVM exception, so using that name with
# agreement from legal team
# https://lists.fedoraproject.org/archives/list/legal@lists.fedoraproject.org/message/A7GFSD6M3GYGSI32L2FC5KB22DUAEQI3/
License: Apache-2.0 WITH LLVM-exception
Summary: PAPPL-based Printer Application for PostScript printers.
URL: %{forgeurl}
Source0: %{forgesource}
Source1: ps-printer-app.sysusers
Source2: ps-printer-app.conf

# Services which run as root cannot create listener sockets
Patch0: ps-printer-app_service-user.patch

# uses make
BuildRequires: make
# written in C
BuildRequires: gcc
# macros in scriptlets
BuildRequires: systemd-rpm-macros
# using pkgconfig in SPEC file
BuildRequires: pkgconf-pkg-config
# CUPS API
BuildRequires: pkgconfig(cups) >= 2.2
# filters API
BuildRequires: pkgconfig(libcupsfilters) >= 2.0b1
# common PAPPL related functions API
BuildRequires: pkgconfig(libpappl-retrofit) >= 1.0b1
# IPP <-> PPD convertor API
BuildRequires: pkgconfig(libppd) >= 2.0b2
# PAPPL API for web ui, commands, IPP system
BuildRequires: pkgconfig(pappl) >= 1.2.1
# perl magic related magic in Makefile for getting version numbers
BuildRequires: perl

%description
ps-printer-app is a printer application for PostScript printers that uses PAPPL
to support IPP printing from multiple operating systems. In addition, it uses
the resources of cups-filters 2.x (filter functions in libcupsfilters, libppd)
and pappl-retrofit (encapsulating classic CUPS drivers in Printer Applications).
This work (or now the code of pappl-retrofit) is derived from the hp-printer-app.

%prep
%forgesetup
%autopatch -p1

%build
%make_build

%install
%make_install libdir=%{buildroot}%{_libdir} serverbin=%{buildroot}%{_libdir}/ps-printer-app

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/ps-printer-app.conf
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/ps-printer-app.conf

%pre
%sysusers_create_compat %{SOURCE1}

%post
%systemd_post ps-printer-app.service

%preun
%systemd_preun ps-printer-app.service

%postun
%systemd_postun_with_restart ps-printer-app.service

%files
%license
%{_bindir}/ps-printer-app
%{_libdir}/ps-printer-app
%{_unitdir}/ps-printer-app.service
%{_mandir}/man1/ps-printer-app.1.gz
%{_datadir}/ppd/generic-ps-printer.ppd
%dir %{_datadir}/ps-printer-app
%{_datadir}/ps-printer-app/testpage.ps
%attr(-, ps-printer-app, ps-printer-app) %dir %{_sharedstatedir}/ps-printer-app
%config(noreplace) %{_sysconfdir}/ps-printer-app.conf
%{_sysusersdir}/ps-printer-app.conf

%changelog
* Tue Aug 06 2024 Zdenek Dohnal <zdohnal@redhat.com> - 0-2.20230918git5dbdece
- initial import (bz#)

* Mon Sep 18 2023 Brandon Nielsen <nielsenb@jetfuse.net> 0-1.20230918git5dbdece
- Update to 5dbdece git snapshot
- Change to SPDX license identifier

* Thu Feb 2 2023 Brandon Nielsen <nielsenb@jetfuse.net> 0-1.20230202git4a54b0f
- Update to 4a54b0f git snapshot
- Remove unit install workaround since it seems to work on rawhide

* Thu Aug 25 2022 Brandon Nielsen <nielsenb@jetfuse.net> 0-1.20220825git73bafe8
- Update to 73bafe8 git snapshot

* Sun Feb 27 2022 Brandon Nielsen <nielsenb@jetfuse.net> 0-1.20220227git81d6d64
- Update to 81d6d64 git snapshot

* Tue Nov 16 2021 Brandon Nielsen <nielsenb@jetfuse.net> 0-1.20211116gitf2480e8
- Update to latest git snapshot

* Sun Sep 26 2021 Brandon Nielsen <nielsenb@jetfuse.net> 0-4.20210916git65b53e2
- Run service as user ps-printer-app

* Thu Sep 23 2021 Brandon Nielsen <nielsenb@jetfuse.net> 0-3.20210916git65b53e2
- Correct some path definitions

* Thu Sep 23 2021 Brandon Nielsen <nielsenb@jetfuse.net> 0-2.20210916git65b53e2
- Add shared state folder

* Wed Sep 15 2021 Brandon Nielsen <nielsenb@jetfuse.net> 0-1.20210916git65b53e2
- Initial specfile
