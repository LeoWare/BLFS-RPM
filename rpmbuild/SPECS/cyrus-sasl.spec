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
Source1:	http://www.linuxfromscratch.org/blfs/downloads/svn/blfs-bootscripts-20130512.tar.bz2
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
tar xf %{SOURCE1}
%build
autoreconf -fi
pushd saslauthd
autoreconf -fi
popd
./configure \
	CFLAGS="%{optflags} -fPIC" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--sysconfdir=/etc \
	--with-dblib=berkeley \
	--with-dbpath=/var/lib/sasl/sasldb2 \
	--with-saslauthd=/var/run/saslauthd \
	--with-plugindir=%{_libdir}/sasl2 \
	--enable-anon\
	--enable-login \
	--enable-plain \
	--enable-cram \
	--enable-digest \
	--enable-ntlm \
	--enable-auth-sasldb \
	--disable-java \
	--disable-krb4 \
	--disable-otp
 
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete
install -D -m644 COPYING %{buildroot}/usr/share/licenses/%{name}/LICENSE
#	daemonize
pushd blfs-bootscripts-20130512
make DESTDIR=%{buildroot} install-saslauthd
popd
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/etc/rc.d/init.d/saslauthd
/etc/rc.d/rc0.d/K49saslauthd
/etc/rc.d/rc1.d/K49saslauthd
/etc/rc.d/rc2.d/S24saslauthd
/etc/rc.d/rc3.d/S24saslauthd
/etc/rc.d/rc4.d/S24saslauthd
/etc/rc.d/rc5.d/S24saslauthd
/etc/rc.d/rc6.d/K49saslauthd
/etc/sysconfig/saslauthd
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
