# TODO
#  - split based on provided spec.in: devel, fish, utils ?
#  - additional split by requires/services (watchdog)
Summary:	GNU FreeIPMI
Name:		freeipmi
Version:	0.1.3
Release:	0.5
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.californiadigital.com/pub/freeipmi/download/0.1.3/%{name}-%{version}.tar.gz
# Source0-md5:	c4b088f806253971759c60263722e63d
URL:		http://www.gnu.org/software/freeipmi/
BuildRequires:	guile-devel
#BuildRequires:	autoconf >= 2.50
#BuildRequires:	automake
#BuildRequires:	libltdl-devel
#BuildRequires:	libtool
#Obsoletes:	ipmitool-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# XXX don't translate before subpackages are done
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

#%package fish
#Summary:	FreeIPMI Shell
#Group:		Applications/System
#Requires:	%{name} = %{version}-%{release}
#
#%description fish
#Fish provides Shell, Extension/Plug-in and scripting interface. As a
#shell, User has access to both in-band and out-of-band access to the
#host BMC through a rich set of IPMI commands.

%package devel
Summary:	Development package for FreeIPMI
Group:		Development/Libraries

%description devel
Development package for FreeIPMI. This package includes the FreeIPMI
header files and static libraries.

%package static
Summary:	Static FreeIPMI library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FreeIPMI library.

%prep
%setup -q

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

# TODO: patch Makefile.am instead
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/freeipmi
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post 	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/BUGS NEWS TODO AUTHORS README ChangeLog
%doc doc/ipmi-over-ts2000.texi
%doc DISCLAIMER.*
%{_sysconfdir}/init.d/bmc-watchdog
%dir /var/lib/freeipmi
/var/lib/freeipmi/ipckey
%dir /var/log/freeipmi
%{_libdir}/libfreeipmi.so.1.0.0
%{_libdir}/libfreeipmi.so.1
%attr(755,root,root) %{_sbindir}/rmcpping
%attr(755,root,root) %{_sbindir}/ipmiping
%attr(755,root,root) %{_sbindir}/ipmipower
%attr(755,root,root) %{_sbindir}/bmc-watchdog
%{_datadir}/fish/extensions
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_datadir}/info/freeipmi.info.*

#%files fish
#%defattr(644,root,root,755)
%dir %{_sysconfdir}/fish
%config(noreplace) %{_sysconfdir}/fish/sensors-conf.scm
%config(noreplace) %{_sysconfdir}/fish/fish.scm
%attr(755,root,root) %{_sbindir}/fish
%attr(755,root,root) %{_sbindir}/bmc-config
%attr(755,root,root) %{_sbindir}/bmc-info
%attr(755,root,root) %{_sbindir}/sel
%attr(755,root,root) %{_sbindir}/sensors
%dir %{_datadir}/fish
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc doc/examples/
%doc doc/{ipmi-network-layout.fig,freeipmi-hackers-intro.sxi}
%{_includedir}/freeipmi
%{_libdir}/libfreeipmi.la
%{_libdir}/libfreeipmi.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libfreeipmi.a
