#		https://github.com/p11-glue/p11-kit/releases/download/0.23.8/p11-kit-0.23.8.tar.gz
Summary:	The p11-kit package provides a way to load and enumerate PKCS #11 (a Cryptographic Token Interface Standard) modules
Name:		p11-kit
Version:	0.23.8
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.gz
%description
	The p11-kit package provides a way to load and enumerate PKCS #11 (a Cryptographic Token Interface Standard) modules
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--sysconfdir=/etc \
		--with-trust-paths=/etc/pki/anchors
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	ln -sfv ./pkcs11/p11-kit-trust.so %{buildroot}/usr/lib/libnssckbi.so
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
	%defattr(-,root,root)
	%{_sysconfdir}//pkcs11
	%{_bindir}/%{NAME}
	%{_bindir}/trust
	%{_includedir}/p11-kit-1
	%{_libdir}/libnssckbi.so
	%{_libdir}/libp11-kit.so
	%{_libdir}/libp11-kit.so.0
	%{_libdir}/libp11-kit.so.0.3.0
	%{_libdir}/p11-kit-proxy.so
	%{_libdir}/pkcs11/p11-kit-client.so
	%{_libdir}/pkcs11/p11-kit-trust.so
	%{_libdir}/pkgconfig/p11-kit-1.pc
	%{_libexecdir}/%{NAME}
	%{_datarootdir}/gtk-doc/html/%{NAME}
	%{_datarootdir}/%{NAME}
%changelog
*	Thu Mar 01 2018 baho-utot <baho-utot@columbus.rr.com> 0.23.8-1
-	Initial build.	First version