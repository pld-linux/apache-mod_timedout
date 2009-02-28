#
%define		mod_name	timedout
%define 	apxs		%{_sbindir}/apxs
Summary:	Apache module: timedout
Summary(pl.UTF-8):	Moduł Apache'a: timedout
Name:		apache-mod_%{mod_name}
Version:	0.1
Release:	1
License:	GPL v2
Group:		Networking/Daemons/HTTP
Source0:	http://dl.sourceforge.net/modtimedout/mod_%{mod_name}-%{version}.tar.bz2
# Source0-md5:	11e8b08c40b29654abf01df29a22715c
Source1:	%{name}.conf
URL:		http://modtimedout.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_timedout is an Apache module for checking the Apache free server
count. When this is lower then defined in the configuration, it starts
searching for long-running Apache requests, and either killing them or
warning about plans to do it.

%description -l pl.UTF-8
mod_timedout to moduł apache sprawdzający liczbę dostępnych serwerów.
Gdy liczba ta jest poniżej wartości określonej w pliku
konfiguracyjnym, moduł ten zaczyna wyszukiwanie najdłużej
obsługiwanych żądań Apache i zabija je lub sygnalizuje takie zamiary.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-apache=/usr/include/apache \
	--with-apr=$(apr-1-config --includedir)

%build
%{__make} \
	CFLAGS="%{rpmcflags} $(apr-1-config --cflags --includes) $(apu-1-config --includes)"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install .libs/libmodtimedout.so.0.0.0 $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
