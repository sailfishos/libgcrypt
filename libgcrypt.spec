#specfile originally created for Fedora, modified for Moblin Linux
Name: libgcrypt
Version: 1.5.0
Release: 1
URL: http://www.gnu.org/software/libgcrypt/
Source0: ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2.sig
Source2: wk@g10code.com
Patch0: libgcrypt-adding-pc.patch
License: LGPLv2+
Summary: A general-purpose cryptography library
BuildRequires: gawk pkgconfig(libgpg-error) pkgconfig
Group: System/Libraries

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
PreReq: /sbin/install-info
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
%setup -q
%patch0 -p1
%build
autoreconf
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

# Relocate the shared libraries to /%{_lib}.
mkdir -p $RPM_BUILD_ROOT/%{_lib}
for shlib in $RPM_BUILD_ROOT/%{_libdir}/*.so* ; do
	if test -L "$shlib" ; then
		rm "$shlib"
	else
		mv "$shlib" $RPM_BUILD_ROOT/%{_lib}/
	fi
done

# Figure out where /%{_lib} is relative to %{_libdir}.
touch $RPM_BUILD_ROOT/root_marker
relroot=..
while ! test -f $RPM_BUILD_ROOT/%{_libdir}/$relroot/root_marker ; do
	relroot=$relroot/..
done

# Overwrite development symlinks.
pushd $RPM_BUILD_ROOT/%{_libdir}
for shlib in $relroot/%{_lib}/lib*.so.* ; do
	shlib=`echo "$shlib" | sed -e 's,//,/,g'`
	target=`basename "$shlib" | sed -e 's,\.so.*,,g'`.so
	ln -sf $shlib $target
done
popd

# Add soname symlink.
/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_lib}/
rm -f $RPM_BUILD_ROOT/root_marker

rm -f $RPM_BUILD_ROOT/usr/share/info/dir


%clean
rm -fr $RPM_BUILD_ROOT

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
/%{_lib}/*.so.*
#%{_libdir}/%{name}

%files devel
%defattr(-,root,root)
%{_bindir}/%{name}-config
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/aclocal/*
#%{_datadir}/%{name}

%{_infodir}/gcrypt.info*
%{_libdir}/pkgconfig/*.pc

