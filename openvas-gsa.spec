%define Werror_cflags -Wformat

Name:           openvas-gsa
Version:        2.0.2
Release:        2
License:        GPLv2+
Group:          System/Configuration/Networking
Url:            http://www.openvas.org
Source0:        http://wald.intevation.org/frs/download.php/1157/greenbone-security-assistant-%{version}.tar.gz
Source1:        gsad.logrotate
Source2:        debian.greenbone-security-assistant.default
Source3:        gsad.init.suse
Source4:        gsad.init.fedora
Source5:        gsad.init.mandriva
source6:				.abf.yml
Patch0:		greenbone-security-assistant-2.0.1-werror.diff

BuildRequires:  pinentry-gtk2
BuildRequires:  xsltproc

BuildRequires:  cmake >= 2.6.0
BuildRequires:  doxygen
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libmicrohttpd) >= 0.4.2
BuildRequires:  openvas-devel >= 3.98
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig
Requires:       logrotate
Summary:        The Greenbone Security Assistant

%description
The Greenbone Security Assistant is a web application that
connects to the OpenVAS Manager and OpenVAS Administrator
to provide for a full-featured user interface for
vulnerability management.


%prep
%setup -q -n greenbone-security-assistant-%{version}
%patch0 -p0 -b .werror

%build
export LDFLAGS="-lopenvas_base -lopenvas_misc"
%serverbuild

%cmake -DCMAKE_VERBOSE_MAKEFILE=ON \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DSYSCONFDIR=%{_sysconfdir} \
        -DLOCALSTATEDIR=%{_localstatedir} \
        -DCMAKE_BUILD_TYPE=release \
	-DUSE_LIBXSLT=0
%{__mkdir_p} src/html
cp -r ../src/html/* src/html
%make  VERBOSE=1

%install
pushd build
%__make install DESTDIR=%{buildroot}
popd
%__install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/greenbone-security-assistant
%__install -D -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/greenbone-security-assistant
%__install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/greenbone-security-assistant

%__mkdir_p %{buildroot}%{_localstatedir}/log/openvas
touch %{buildroot}%{_localstatedir}/log/openvas/gsad.log

%post
%_post_service greenbone-security-assistant

%preun
%_preun_service greenbone-security-assistant


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/logrotate.d/greenbone-security-assistant
%dir %{_sysconfdir}/openvas
%config(noreplace) %{_sysconfdir}/openvas/gsad_log.conf
%{_initrddir}/greenbone-security-assistant
%{_sbindir}/gsad
%{_mandir}/man8/gsad.8*
%dir %{_datadir}/openvas
%{_datadir}/openvas/gsa
%dir %{_localstatedir}/log/openvas
%ghost %{_localstatedir}/log/openvas/gsad.log
%config(noreplace) %{_sysconfdir}/sysconfig/greenbone-security-assistant



%changelog
* Thu Sep 08 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 2.0.1-2mdv2011.0
+ Revision: 699059
- bump release
- BR fixed
- Group fixed
- lets wellcme from Suse
  P1 to let install and compile
  multiple SPEC fixes
- import openvas-gsa

