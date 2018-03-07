#		https://archive.mozilla.org/pub/security/nss/releases/NSS_3_32_RTM/src/nss-3.32.tar.gz
#		http://www.linuxfromscratch.org/patches/blfs/8.1/nss-3.32-standalone-1.patch
Summary:	The Network Security Services (NSS) package is a set of libraries designed to support cross-platform development of security-enabled client and server applications
Name:		nss
Version:	3.32
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
#	Requires:	NSPR-4.16 Rec:	SQLite-3.20.0 and p11-kit-0.23.8 (runtime) 
Source0:	%{name}-%{version}.tar.gz
Patch0:		nss-3.32-standalone-1.patch
%description
	The Network Security Services (NSS) package is a set of libraries designed to support
	cross-platform development of security-enabled client and server applications.
	Applications built with NSS can support SSL v2 and v3, TLS, PKCS #5, PKCS #7, PKCS #11,
	PKCS #12, S/MIME, X.509 v3 certificates, and other security standards. This is useful
	for implementing SSL and S/MIME or other Internet security standards into an application. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%patch0 -p1
%build
	cd nss
	make \
		-j1 BUILD_OPT=1 \
		NSPR_INCLUDE_DIR=/usr/include/nspr  \
		USE_SYSTEM_ZLIB=1 \
		ZLIB_LIBS=-lz \
		NSS_ENABLE_WERROR=0 \
		$([ $(uname -m) = x86_64 ] && echo USE_64=1) \
		$([ -f /usr/include/sqlite3.h ] && echo NSS_USE_SYSTEM_SQLITE=1)
%install
#	cd nss
#	make DESTDIR=%{buildroot} install
	cd nss
	cd ../dist
	install -vdm 755 %{buildroot}%{_bindir}
	install -vdm 755 %{buildroot}%{_includedir}/nss
	install -vdm 755 %{buildroot}%{_libdir}
	install -v -m755 Linux*/lib/*.so %{buildroot}%{_libdir}
	install -v -m644 Linux*/lib/{*.chk,libcrmf.a} %{buildroot}%{_libdir}
	#	file /usr/lib/libnssckbi.so from install of nss-3.32-1.x86_64 conflicts with file from package p11-kit-0.23.8-1.x86_64
	rm %{buildroot}/usr/lib/libnssckbi.so
	#
	cp -v -RL {public,private}/nss/* %{buildroot}%{_includedir}/nss
	chmod 644 %{buildroot}%{_includedir}/nss/*
	install -v -m755 Linux*/bin/{certutil,nss-config,pk12util} %{buildroot}%{_bindir}
	install -vdm 755 %{buildroot}%{_libdir}/pkgconfig
	install -vm 644 Linux*/lib/pkgconfig/nss.pc %{buildroot}%{_libdir}/pkgconfig
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
	%defattr(-,root,root)
	%{_bindir}/certutil
	%{_bindir}/nss-config
	%{_bindir}/pk12util
	%{_includedir}/nss
	%{_libdir}/*.a
	%{_libdir}/*.chk
	%{_libdir}/*.so
	%{_libdir}/pkgconfig/nss.pc
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 3.32-1
-	Initial build.	First version