%define Werror_cflags -Wformat

Name:           openvas-gsa
Version:        2.0.1
Release:        %mkrel 1
License:        GPLv2+
Group:          System/Configuration/Networking
Url:            http://www.openvas.org
Source0:        greenbone-security-assistant-%{version}.tar.gz
Source1:        gsad.logrotate
Source2:        debian.greenbone-security-assistant.default
Source3:        gsad.init.suse
Source4:        gsad.init.fedora
Source5:        gsad.init.mandriva
Patch0:		greenbone-security-assistant-2.0.1-werror.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildRequires:  pinentry-gtk2
BuildRequires:  xsltproc

BuildRequires:  cmake >= 2.6.0
BuildRequires:  doxygen
BuildRequires:  glib2-devel
BuildRequires:  libmicrohttpd-devel >= 0.4.2
BuildRequires:  libopenvas-devel >= 3.98
BuildRequires:  libxslt-devel
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
%serverbuild
#export CFLAGS="%{optflags}"

%cmake -DCMAKE_VERBOSE_MAKEFILE=ON \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DSYSCONFDIR=%{_sysconfdir} \
        -DLOCALSTATEDIR=%{_localstatedir} \
        -DCMAKE_BUILD_TYPE=release \
	-DUSE_LIBXSLT=0
%{__mkdir_p} src/html
%{__cp} -r ../src/html/* src/html
%make  VERBOSE=1

%install
pushd build
%__make install DESTDIR=%{buildroot}
popd
%__install -D -m 644 %{_sourcedir}/gsad.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/greenbone-security-assistant

%__install -D -m 755 %{_sourcedir}/gsad.init.mandriva %{buildroot}%{_initrddir}/greenbone-security-assistant
%__install -D -m 644 %{_sourcedir}/debian.greenbone-security-assistant.default %{buildroot}%{_sysconfdir}/sysconfig/greenbone-security-assistant

%__mkdir_p %{buildroot}%{_localstatedir}/log/openvas
touch %{buildroot}%{_localstatedir}/log/openvas/gsad.log

%clean
test "%{buildroot}" != "/" && %__rm -rf %{buildroot}

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

