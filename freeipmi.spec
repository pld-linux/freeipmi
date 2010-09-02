# TODO
#  - split based on provided spec.in: devel, fish, utils ?
#    still not sure about how to split packages. move -libs to main
#    and programs to -utils? or leave as it is? (but package init.d
#    scripts separately?). -libs contains /var/lib/%{name} (because
#    that .so needs to read ipckey inode), so one vote for discarding
#    -libs?
#  - additional split by requires/services (watchdog)
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
Summary(pl.UTF-8):	GNU FreeIPMI - oprogramowanie do zarządzania systemem
Name:		freeipmi
Version:	0.8.9
Release:	0.1
License:	GPL v2+
Group:		Applications/System
Source0:	http://ftp.zresearch.com/pub/freeipmi/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5c729b91e229c3ed3cd1d568195a2d26
Patch0:		%{name}-install.patch
URL:		http://www.gnu.org/software/freeipmi/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.9
BuildRequires:	grep
BuildRequires:	guile-devel
BuildRequires:	libgcrypt-devel
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

%package bmc-watchdog
Summary:	FreeIPMI BMC watchdog
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	logrotate

%description bmc-watchdog
Provides a watchdog daemon for OS monitoring and recovery.

%package libs
Summary:	Shared libraries for FreeIPMI
Summary(pl.UTF-8):	Biblioteki współdzielone FreeIPMI
Group:		Libraries


%package ipmidetectd
Summary:	IPMI node detection monitoring daemon
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	logrotate

%description ipmidetectd
IPMI node detection daemon.


%description libs
Shared libraries for FreeIPMI.

%description libs -l pl.UTF-8
Biblioteki współdzielone FreeIPMI.

%package devel
Summary:	Development package for FreeIPMI
Summary(pl.UTF-8):	Pakiet programistyczny FreeIPMI
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development package for FreeIPMI. This package includes the FreeIPMI
header files.

%description devel -l pl.UTF-8
Pakiet programistyczny FreeIPMI. Zawiera pliki nagłówkowe.

%package static
Summary:	Static FreeIPMI library
Summary(pl.UTF-8):	Statyczna biblioteka FreeIPMI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FreeIPMI library.

%description static -l pl.UTF-8
Statyczna biblioteka FreeIPMI.

%prep
%setup -q
%patch0 -p1
#install %{_includedir}/limits.h ipmi-oem/src/
#cat %{_includedir}/linux/limits.h |grep ARG_MAX >> ipmi-oem/src/limits.h
#install ipmi-oem/src/limits.h ipmi-raw/src/limits.h

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
mv $RPM_BUILD_ROOT/etc/init.d/* $RPM_BUILD_ROOT/etc/rc.d/init.d
# TODO: patch Makefile.am instead
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/freeipmi

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog DISCLAIMER.* INSTALL NEWS README TODO doc/freeipmi-*.txt
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/freeipmi.conf
%attr(444,root,root) %config(noreplace) %{_sysconfdir}/ipmi_monitoring_sensors.conf
%attr(755,root,root) %{_sbindir}/bmc-config
%attr(755,root,root) %{_sbindir}/bmc-device
%attr(755,root,root) %{_sbindir}/bmc-info
%attr(755,root,root) %{_sbindir}/ipmi-chassis
%attr(755,root,root) %{_sbindir}/ipmi-chassis-config
%attr(755,root,root) %{_sbindir}/ipmi-dcmi
%attr(755,root,root) %{_sbindir}/ipmi-fru
%attr(755,root,root) %{_sbindir}/ipmi-locate
%attr(755,root,root) %{_sbindir}/ipmi-oem
%attr(755,root,root) %{_sbindir}/ipmi-pef-config
%attr(755,root,root) %{_sbindir}/ipmi-raw
%attr(755,root,root) %{_sbindir}/ipmi-sel
%attr(755,root,root) %{_sbindir}/ipmi-sensors
%attr(755,root,root) %{_sbindir}/ipmi-sensors-config
%attr(755,root,root) %{_sbindir}/ipmiconsole
%attr(755,root,root) %{_sbindir}/ipmidetect
%attr(755,root,root) %{_sbindir}/ipmimonitoring
%attr(755,root,root) %{_sbindir}/ipmiping
%attr(755,root,root) %{_sbindir}/ipmipower
%attr(755,root,root) %{_sbindir}/pef-config
%attr(755,root,root) %{_sbindir}/rmcpping
%{_mandir}/man5/bmc-config.conf.5*
%{_mandir}/man5/freeipmi.conf.5*
%{_mandir}/man5/ipmi_monitoring_sensors.conf.5*
%{_mandir}/man5/ipmiconsole.conf.5*
%{_mandir}/man5/ipmidetect.conf.5*
%{_mandir}/man5/ipmimonitoring.conf.5*
%{_mandir}/man5/ipmimonitoring_sensors.conf.5*
%{_mandir}/man5/ipmipower.conf.5*
%{_mandir}/man5/libipmimonitoring.conf.5*
%{_mandir}/man7/freeipmi.7*
%{_mandir}/man8/bmc-config.8*
%{_mandir}/man8/bmc-device.8*
%{_mandir}/man8/bmc-info.8*
%{_mandir}/man8/ipmi-chassis-config.8*
%{_mandir}/man8/ipmi-chassis.8*
%{_mandir}/man8/ipmi-dcmi.8*
%{_mandir}/man8/ipmi-fru.8*
%{_mandir}/man8/ipmi-locate.8*
%{_mandir}/man8/ipmi-oem.8*
%{_mandir}/man8/ipmi-pef-config.8*
%{_mandir}/man8/ipmi-raw.8*
%{_mandir}/man8/ipmi-sel.8*
%{_mandir}/man8/ipmi-sensors-config.8*
%{_mandir}/man8/ipmi-sensors.8*
%{_mandir}/man8/ipmiconsole.8*
%{_mandir}/man8/ipmidetect.8*
%{_mandir}/man8/ipmimonitoring.8*
%{_mandir}/man8/ipmiping.8*
%{_mandir}/man8/ipmipower.8*
%{_mandir}/man8/pef-config.8*
%{_mandir}/man8/rmcpping.8*
#%dir %{_localstatedir}/cache/ipmimonitoringsdrcache
%{_infodir}/freeipmi-faq.info*
%dir /var/log/freeipmi

%files bmc-watchdog
%defattr(644,root,root,755)
%config(noreplace) /etc/rc.d/init.d/bmc-watchdog
%config(noreplace) /etc/sysconfig/bmc-watchdog
%config(noreplace) /etc/logrotate.d/bmc-watchdog
%attr(755,root,root) %{_sbindir}/bmc-watchdog
%{_mandir}/man8/bmc-watchdog.8*
%dir /var/log/freeipmi

%files ipmidetectd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ipmidetectd
%attr(754,root,root) /etc/rc.d/init.d/ipmidetectd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipmidetectd.conf
%{_mandir}/man5/ipmidetectd.conf.5*
%{_mandir}/man8/ipmidetectd.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreeipmi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreeipmi.so.10
%attr(755,root,root) %{_libdir}/libipmiconsole.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libipmiconsole.so.2
%attr(755,root,root) %{_libdir}/libipmidetect.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libipmidetect.so.0
%attr(755,root,root) %{_libdir}/libipmimonitoring.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libipmimonitoring.so.4
%dir /var/lib/freeipmi
/var/lib/freeipmi/ipckey

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libipmiconsole.so
%attr(755,root,root) %{_libdir}/libfreeipmi.so
%attr(755,root,root) %{_libdir}/libipmidetect.so
%attr(755,root,root) %{_libdir}/libipmimonitoring.so
%{_libdir}/libfreeipmi.la
%{_libdir}/libipmiconsole.la
%{_libdir}/libipmidetect.la
%{_libdir}/libipmimonitoring.la
%{_includedir}/freeipmi
%{_includedir}/ipmi*.h
%{_mandir}/man3/libfreeipmi.3*
%{_mandir}/man3/libipmiconsole.3*
%{_mandir}/man3/libipmidetect.3*
%{_mandir}/man3/libipmimonitoring.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libfreeipmi.a
%{_libdir}/libipmiconsole.a
%{_libdir}/libipmidetect.a
%{_libdir}/libipmimonitoring.a
