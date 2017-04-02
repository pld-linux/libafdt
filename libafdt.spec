#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
%bcond_without	tests		# skip tests

Summary:	LIBrary for Asynchronous File Descriptor Transfer
Name:		libafdt
Version:	0.1.0
Release:	4
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libafdt/%{name}-%{version}.tar.gz
# Source0-md5:	8051b4e88c5804ce34e221cb62c5e672
URL:		http://facebook.github.io/libafdt/
Patch0:		%{name}-link.patch
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libevent-devel >= 1.4.5
BuildRequires:	libtool
%{?with_tests:BuildRequires:	python}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libafdt is a library for "a"synchronous "f"ile "d"escriptor
"t"ransfers. It provides a simple interface that allows libevent-based
programs to set up a Unix domain socket to accept connections and
transfer file descriptors to clients, or to be a client and request a
file descriptor from a libafdt server. Low-level and synchronous
interfaces are also provided for programs that do not use libevent.

%package devel
Summary:	Header files for libafdt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libafdt
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libafdt library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libafdt.

%package static
Summary:	Static libafdt library
Summary(pl.UTF-8):	Statyczna biblioteka libafdt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libafdt library.

%description static -l pl.UTF-8
Statyczna biblioteka libafdt.

%package apidocs
Summary:	libafdt API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libafdt
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API and internal documentation for libafdt library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libafdt.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--enable-shared \
	%{!?with_static_libs:--disable-static}

%{__make}

%{?with_tests:%{__make} check}

%{?with_apidocs:doxygen}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libafdt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libafdt.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libafdt.so
%{_libdir}/libafdt.la
%{_includedir}/afdt.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libafdt.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doxygen-out/html/*
%endif
