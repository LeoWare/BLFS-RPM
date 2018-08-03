#	 https://ftp.gnu.org/gnu/libtasn1/libtasn1-4.12.tar.gz
Summary:	highly portable C library that encodes and decodes DER/BER data following an ASN.1 schema
Name:		libtasn1
Version:	4.12
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Multimedia
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.gz
%description
	highly portable C library that encodes and decodes DER/BER data following an ASN.1 schema
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	make -C doc/reference DESTDIR=%{buildroot} install-data-local
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post	-p /sbin/ldconfig
	pushd /usr/share/info
	rm -v dir
	for f in *
		do install-info $f dir 2>/dev/null
	done
	popd
%postun	-p /sbin/ldconfig
	pushd /usr/share/info
	rm -v dir
	for f in *
		do install-info $f dir 2>/dev/null
	done
	popd
%files
	%defattr(-,root,root)
	%{_bindir}/asn1Coding
	%{_bindir}/asn1Decoding
	%{_bindir}/asn1Parser
	%{_includedir}/libtasn1.h
	%{_libdir}/libtasn1.so
	%{_libdir}/libtasn1.so.6
	%{_libdir}/libtasn1.so.6.5.4
	%{_libdir}/pkgconfig/libtasn1.pc
	%{_infodir}/libtasn1.info.gz
	%{_mandir}/man1/*.gz
	%{_mandir}/man3/*.gz
%changelog
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> 4.12-1
-	Initial build.	First version