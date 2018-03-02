#		https://www.gnupg.org/ftp/gcrypt/gnutls/v3.5/gnutls-3.5.14.tar.xz
Summary:	The GnuTLS package contains libraries and userspace tools which provide a secure layer over a reliable transport layer
Name:		gnutls
Version:	3.5.14
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.xz
%description
	The GnuTLS package contains libraries and userspace tools which provide a secure layer over
	a reliable transport layer. Currently the GnuTLS library implements the proposed standards
	by the IETF's TLS working group. Quoting from the TLS protocol specification:

	"The TLS protocol provides communications privacy over the Internet. The protocol allows client/server
	applications to communicate in a way that is designed to prevent eavesdropping, tampering, or message forgery."

	GnuTLS provides support for TLS 1.2, TLS 1.1, TLS 1.0, and SSL 3.0 protocols, TLS extensions,
	including server name and max record size. Additionally, the library supports authentication
	using the SRP protocol, X.509 certificates and OpenPGP keys, along with support for the
	TLS Pre-Shared-Keys (PSK) extension, the Inner Application (TLS/IA) extension and X.509 and
	OpenPGP certificate handling. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--with-default-trust-store-pkcs11="pkcs11:"
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	make -C doc/reference DESTDIR=%{buildroot} install-data-local
	%find_lang %{name}
	#	Copy license/copying file 
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f %{name}.lang
	%defattr(-,root,root)
	%{_bindir}/certtool
	%{_bindir}/gnutls-cli
	%{_bindir}/gnutls-cli-debug
	%{_bindir}/gnutls-serv
	%{_bindir}/ocsptool
	%{_bindir}/p11tool
	%{_bindir}/psktool
	%{_bindir}/srptool
	%{_includedir}/gnutls
	%{_libdir}/libgnutls.so
	%{_libdir}/libgnutls.so.30
	%{_libdir}/libgnutls.so.30.14.6
	%{_libdir}/libgnutlsxx.so
	%{_libdir}/libgnutlsxx.so.28
	%{_libdir}/libgnutlsxx.so.28.1.0
	%{_libdir}/pkgconfig/gnutls.pc
	%{_datarootdir}/doc/gnutls
	%{_datarootdir}/gtk-doc/html/gnutls
	%{_infodir}/*.gz
	%{_mandir}/man1/*.gz
	%{_mandir}/man3/*.gz
%changelog
*	Thu Mar 01 2018 baho-utot <baho-utot@columbus.rr.com> 3.5.14-1
-	Initial build.	First version