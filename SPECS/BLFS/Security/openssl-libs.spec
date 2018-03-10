#		 https://openssl.org/source/openssl-1.0.2l.tar.gz
Summary:	The OpenSSL-1.0.2l package contains libraries relating to cryptography.
Name:		openssl-libs
Version:	1.0.2l
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	openssl-%{version}.tar.gz
Patch0:		openssl-1.0.2l-compat_versioned_symbols-1.patch
%description
	The OpenSSL-1.0.2l package contains libraries relating to cryptography.
	These are useful for providing cryptographic functions to other packages,
	such as email applications and web browsers (for accessing HTTPS sites).
	This package provides only the libraries and headers for packages that
	have not yet been ported to OpenSSL-1.1.0f
%prep
%setup -q -n openssl-%{VERSION}
%patch0 -p1
%build
	./config \
		--prefix=%{_prefix} \
		--openssldir=%{_sysconfdir}/ssl \
		--libdir=lib/openssl-1.0 \
		shared \
		zlib-dynamic       
	make depend
	make -j1
%install
	make INSTALL_PREFIX=$PWD/Dest install_sw
	install -vdm755 %{buildroot}/usr/lib/openssl-1.0
	cp -Rv Dest/usr/lib/openssl-1.0/* %{buildroot}/usr/lib/openssl-1.0
	#
	mv -v  %{buildroot}/usr/lib/openssl-1.0/lib{crypto,ssl}.so.1.0.0 %{buildroot}/usr/lib
	ln -sv ../libssl.so.1.0.0 %{buildroot}/usr/lib/openssl-1.0
	ln -sv ../libcrypto.so.1.0.0 %{buildroot}/usr/lib/openssl-1.0
	#
	install -vdm755 %{buildroot}/usr/include/openssl-1.0
	cp -Rv Dest/usr/include/openssl   %{buildroot}/usr/include/openssl-1.0
	sed 's@/include$@/include/openssl-1.0@' -i %{buildroot}/usr/lib/openssl-1.0/pkgconfig/*.pc
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}%{_datarootdir}/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
	%defattr(-,root,root)
#	%%{buildroot}%%{_datarootdir}/licenses/%%{name}/LICENSE
	%{_includedir}/openssl-1.0
	%{_libdir}/libcrypto.so.1.0.0
	%{_libdir}/libssl.so.1.0.0
	%{_libdir}/openssl-1.0

%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 1.0.2l-1
-	Initial build.	First version