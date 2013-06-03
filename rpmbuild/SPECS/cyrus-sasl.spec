Summary:	Cyrus Simple Authentication Service Layer (SASL) library
Name:		cyrus-sasl
Version:	2.1.26
Release:	1
License:	Custom
URL:		http://cyrusimap.web.cmu.edu/
Group:		BLFS/Security
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	ftp://ftp.cyrusimap.org/cyrus-sasl/%{name}-%{version}.tar.gz
Patch0:		http://www.linuxfromscratch.org/patches/blfs/svn/cyrus-sasl-2.1.26-fixes-1.patch
%description
The Cyrus SASL package contains a Simple Authentication and Security 
Layer, a method for adding authentication support to 
connection-based protocols. To use SASL, a protocol includes a command
for identifying and authenticating a user to a server and for 
optionally negotiating protection of subsequent protocol interactions.
If its use is negotiated, a security layer is inserted between the 
protocol and the connection.
%prep
%setup -q
%patch0 -p1
%build
autoreconf -fi
pushd saslauthd
autoreconf -fi
popd
./configure \
	CFLAGS="%{optflags} -fPIC" \
	CXXFLAGS="%{optflags}" \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--sysconfdir=/etc \
	--with-dbpath=/var/lib/sasl/sasldb2 \
	--with-saslauthd=/var/run/saslauthd
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete
install -D -m644 COPYING %{buildroot}/usr/share/licenses/%{name}/LICENSE
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so*
%{_libdir}/pkgconfig/*
%{_libdir}/sasl2/*
%{_sbindir}/*
%{_mandir}/man3/*
%{_mandir}/man8/*
%{_datadir}/licenses/%{name}/LICENSE
%changelog
*	Mon Jun 03 2013 baho-utot <baho-utot@columbus.rr.com> 2.1.26-1
-	Initial build.	First version