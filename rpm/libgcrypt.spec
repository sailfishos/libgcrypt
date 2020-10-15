Name:    libgcrypt
Summary: A general-purpose cryptography library
Version: 1.8.6
Release: 1
License: LGPLv2+
URL:     http://www.gnu.org/software/libgcrypt/
Source0: %{name}-%{version}.tar.gz
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: gawk
BuildRequires: pkgconfig(libgpg-error)

%description
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard. This is a development version.

%package devel
Summary: Development files for the %{name} package
Requires: pkgconfig(libgpg-error)
Requires: %{name} = %{version}-%{release}

%description devel
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard. This package contains files needed to develop
applications using libgcrypt.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
echo -n %{version} | cut -d'+' -f1 > VERSION
%reconfigure --disable-static \
             --disable-doc \
             --enable-noexecstack
%make_build

%check
make check

%install
%make_install

# Change /usr/lib64 back to /usr/lib.  This saves us from having to patch the
# script to "know" that -L/usr/lib64 should be suppressed, and also removes
# a file conflict between 32- and 64-bit versions of this package.
sed -i -e 's,^libdir="/usr/lib.*"$,libdir="/usr/lib",g' %{buildroot}/%{_bindir}/libgcrypt-config

/sbin/ldconfig -n %{buildroot}/%{_libdir}

rm -f %{buildroot}/usr/share/info/dir

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING.LIB
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/%{name}-config
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_bindir}/mpicalc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libgcrypt.pc
%{_datadir}/aclocal/*
