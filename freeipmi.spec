# TODO
#  - split based on provided spec.in: devel, fish, utils ?
#    still not sure about how to split packages. move -libs to main
#    and programs to -utils? or leave as it is? (but package init.d
#    scripts separately?). -libs contains /var/lib/%{name} (because
#    that .so needs to read ipckey inode), so one vote for discarding
#    -libs?
#  - additional split by requires/services (watchdog)
#  - file /usr/share/man/man1/sensors.1.gz from install of freeipmi-0.1.3-0.5 conflicts with file from package lm_sensors-2.
#  - wtf is this?
# # bmc-config
#>>--:>  >>--:>  >>--:> >>--:>
#~ ~   Cat ate the fish!!  ~ ~
#>>--:>  >>--:>  >>--:> >>--:>
#Fish Exception (gh_standard_handler dump):
#tag        : 
#throw args : 
#data       : [/usr/share/fish/extensions/sensors.scm]
#misc-error(#f %s %S (no such module (srfi srfi-13)) #f)No backtrace
#available.
# dig: http://www.google.com/search?q=srfi&ie=UTF-8&oe=UTF-8
Summary:	GNU FreeIPMI - system management software
Summary(pl.UTF-8):   GNU FreeIPMI - oprogramowanie do zarządzania systemem
Name:		freeipmi
Version:	0.1.3
Release:	0.12
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.californiadigital.com/pub/freeipmi/download/0.1.3/%{name}-%{version}.tar.gz
# Source0-md5:	c4b088f806253971759c60263722e63d
Patch0:		%{name}-am.patch
Patch1:		%{name}-build.patch
URL:		http://www.gnu.org/software/freeipmi/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	guile-devel
BuildRequires:	libtool
BuildRequires:	readline-devel >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The GNU FreeIPMI system provides "Remote-Console" (out-of-band) and
"System Management Software" (in-band) based on IPMI v1.5/2.0
specification. This project includes:
- KCS, SMIC, SSIF, LAN Drivers and C Library (libfreeipmi)
- FreeIPMI SHell (fish)
- Watchdog Daemon (bmc-watchdog)
- Sensors (sensors)
- System Event Log (sel)
- BMC Info (bmc-info)
- BMC Config (bmc-config)
- IPMI Power (ipmipower)
- IPMI Ping (ipmiping)
- RMCP Ping (rmcpping)

%description -l pl.UTF-8
System GNU FreeIPMI dostarcza "zdalną konsolę" (Remote-Console) oraz
"oprogramowanie do zarządzania systemem" (System Management Software)
oparte na specyfikacji IPMI v1.5/2.0. Projekt zawiera:
- KCS, SMIC, SSIF, sterowniki LAN i bibliotekę C (libfreeipmi)
- powłokę FreeIPMI SHell (fish)
- demona watchdog (bmc-watchdog)
- czujniki (sensors)
- dziennik zdarzeń systemowych (sel - System Event Log)
- narzędzie informacyjne BMC (bmc-info)
- narzędzie konfiguracyjne BMC (bmc-config)
- narzędzie IPMI Power (ipmipower)
- ping dla IPMI (ipmiping)
- ping dla RMCP (rmcpping)

%package fish
Summary:	FreeIPMI Shell
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	scsh

%description fish
Fish provides Shell, Extension/Plug-in and scripting interface. As a
shell, User has access to both in-band and out-of-band access to the
host BMC through a rich set of IPMI commands.

%description fish -l pl.UTF-8
Fish dostarcza powłokę oraz interfejs rozszerzeń/wtyczek i skryptów.
Jako powłoka daje użytkownikowi dostęp do części in-band jak i
out-of-band systemowego BMC poprzez bogaty zestaw poleceń IPMI.

%package libs
Summary:	Shared libraries for FreeIPMI
Summary(pl.UTF-8):   Biblioteki współdzielone FreeIPMI
Group:		Libraries

%description libs
Shared libraries for FreeIPMI.

%description libs -l pl.UTF-8
Biblioteki współdzielone FreeIPMI.

%package devel
Summary:	Development package for FreeIPMI
Summary(pl.UTF-8):   Pakiet programistyczny FreeIPMI
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development package for FreeIPMI. This package includes the FreeIPMI
header files.

%description devel -l pl.UTF-8
Pakiet programistyczny FreeIPMI. Zawiera pliki nagłówkowe.

%package static
Summary:	Static FreeIPMI library
Summary(pl.UTF-8):   Statyczna biblioteka FreeIPMI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FreeIPMI library.

%description static -l pl.UTF-8
Statyczna biblioteka FreeIPMI.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

# TODO: patch Makefile.am instead
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/freeipmi
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post 	libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/BUGS NEWS TODO AUTHORS README ChangeLog
%doc doc/ipmi-over-ts2000.texi
%doc DISCLAIMER.*
%attr(754,root,root) /etc/rc.d/init.d/bmc-watchdog
%attr(755,root,root) %{_sbindir}/rmcpping
%attr(755,root,root) %{_sbindir}/ipmiping
%attr(755,root,root) %{_sbindir}/ipmipower
%attr(755,root,root) %{_sbindir}/bmc-watchdog
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_infodir}/freeipmi.info*
%dir /var/log/freeipmi

%files fish
%defattr(644,root,root,755)
%dir %{_sysconfdir}/fish
%config(noreplace) %{_sysconfdir}/fish/sensors-conf.scm
%config(noreplace) %{_sysconfdir}/fish/fish.scm
%attr(755,root,root) %{_sbindir}/fish
%attr(755,root,root) %{_sbindir}/bmc-config
%attr(755,root,root) %{_sbindir}/bmc-info
%attr(755,root,root) %{_sbindir}/sel
%attr(755,root,root) %{_sbindir}/sensors
%dir %{_datadir}/fish
%{_datadir}/fish/extensions
%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%dir /var/lib/freeipmi
/var/lib/freeipmi/ipckey
%{_libdir}/libfreeipmi.so.1.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/examples/
%doc doc/{ipmi-network-layout.fig,freeipmi-hackers-intro.sxi}
%attr(755,root,root) %{_libdir}/libfreeipmi.so
%{_libdir}/libfreeipmi.la
%{_includedir}/freeipmi

%files static
%defattr(644,root,root,755)
%{_libdir}/libfreeipmi.a
