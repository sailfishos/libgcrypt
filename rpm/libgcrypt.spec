Name: libgcrypt
Version: 1.5.0
Release: 4
URL: http://www.gnu.org/software/libgcrypt/
Source0: %{name}-%{version}.tar.gz
Source1: wk@g10code.com
Patch0: libgcrypt-adding-pc.patch
Patch1: libgcrypt-flush-reload.patch
Patch2: add_gcry_divide_by_zero.patch
Patch3: CVE-2014-5270.patch
Patch4: CVE-2014-3591.patch
Patch5: CVE-2015-0837-1.patch
Patch6: CVE-2015-0837-2.patch
Patch7: CVE-2015-0837-3.patch
Patch8: 0001-Disable-document-building.patch
License: LGPLv2+
Summary: A general-purpose cryptography library
BuildRequires: gawk pkgconfig(libgpg-error)
Group: System/Libraries

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: pkgconfig(libgpg-error)
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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
echo -n %{version} | cut -d'+' -f1 > VERSION
autoreconf -vfi
%configure --disable-static --enable-noexecstack 
make

%check
make check

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

%post devel
/sbin/install-info %{_infodir}/gcrypt.info.gz %{_infodir}/dir
exit 0

%preun devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gcrypt.info.gz %{_infodir}/dir
fi
exit 0

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/%{name}-config
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/aclocal/*

%{_libdir}/pkgconfig/*.pc

