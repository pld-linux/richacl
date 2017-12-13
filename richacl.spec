#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library and utilities for Rich Access Control Lists
Summary(pl.UTF-8):	Biblioteka i narzędzia do Rich ACL ("bogatych" list kontroli dostępu)
Name:		richacl
Version:	1.12
Release:	1
License:	LGPL v2.1+ (library), GPL v2+ (utilities)
Group:		Libraries
#Source0Download: https://github.com/andreas-gruenbacher/richacl/releases
Source0:	https://github.com/andreas-gruenbacher/richacl/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7ddae319af3c92ead2949b0643d4325a
URL:		https://github.com/andreas-gruenbacher/richacl
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	libtool >= 2:2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library and utilities for Rich Access Control Lists.

Rich Access Control Lists (RichACLs) are an extension of the
traditional POSIX file permission model to support NFSv4 Access
Control Lists (<https://tools.ietf.org/rfc/rfc5661.txt>) on local and
remote-mounted filesystems.

%description -l pl.UTF-8
Biblioteka i narzędzia do Rich ACL ("bogatych" list kontroli dostępu).

RichACLs (Rich Access Control Lists) to rozszerzenie tradycyjnego
POSIX-owego modelu uprawnień do obsługi list kontroli dostępu NFSv4
(NFSv4 ACLs, <https://tools.ietf.org/rfc/rfc5661.txt>) na lokalnie i
zdalnie zamontowanych systemach plików.

%package devel
Summary:	Header files for richacl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki richacl
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for richacl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki richacl.

%package static
Summary:	Static richacl library
Summary(pl.UTF-8):	Statyczna biblioteka richacl
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static richacl library.

%description static -l pl.UTF-8
Statyczna biblioteka richacl.

%prep
%setup -q

echo %{version} > .tarball-version

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/librichacl.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README TODO doc/COPYING
%attr(755,root,root) %{_bindir}/getrichacl
%attr(755,root,root) %{_bindir}/setrichacl
%attr(755,root,root) %{_libdir}/librichacl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librichacl.so.1
%{_mandir}/man1/getrichacl.1*
%{_mandir}/man1/setrichacl.1*
%{_mandir}/man7/richacl.7*
%{_mandir}/man7/richaclex.7*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librichacl.so
%{_includedir}/sys/richacl.h
%{_pkgconfigdir}/librichacl.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/librichacl.a
%endif
