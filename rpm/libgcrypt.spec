Name: libgcrypt
Version: 1.8.1
Release: 2
URL: http://www.gnu.org/software/libgcrypt/
Source0: %{name}-%{version}.tar.gz
Patch0: 0001-Adding-package-config-support.patch
License: LGPLv2+
Summary: A general-purpose cryptography library
BuildRequires: gawk pkgconfig(libgpg-error)
Group: System/Libraries

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: pkgconfig(libgpg-error) >= 1.25
Requires: %{name} = %{version}-%{release}

%description
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This is a development version.

%description devel
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This package contains files needed to develop
applications using libgcrypt.

%prep
%setup -q -n %{name}-%{version}/%{name}
%patch0 -p1

%build
echo -n %{version} | cut -d'+' -f1 > VERSION
autoreconf -vfi
%configure --disable-static --enable-noexecstack --disable-doc
make

%check
%if ! 0%{?qemu_user_space_build}
make check
%endif

%install
rm -fr $RPM_BUILD_ROOT
%make_install

# Change /usr/lib64 back to /usr/lib.  This saves us from having to patch the
# script to "know" that -L/usr/lib64 should be suppressed, and also removes
# a file conflict between 32- and 64-bit versions of this package.
sed -i -e 's,^libdir="/usr/lib.*"$,libdir="/usr/lib",g' $RPM_BUILD_ROOT/%{_bindir}/libgcrypt-config

/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_libdir}

rm -f $RPM_BUILD_ROOT/usr/share/info/dir

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/%{name}-config
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_bindir}/mpicalc
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/aclocal/*

%{_libdir}/pkgconfig/*.pc

