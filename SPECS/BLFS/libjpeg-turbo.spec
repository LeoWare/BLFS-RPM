#		https://downloads.sourceforge.net/libjpeg-turbo/libjpeg-turbo-1.5.2.tar.gz
Summary:	libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to accelerate baseline JPEG compression and decompression
Name:		libjpeg-turbo
Version:	1.5.2
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
#	Requires:	 NASM-2.13.01 or yasm-1.3.0 
Source0:	%{name}-%{version}.tar.gz
%description
	libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to accelerate baseline
	JPEG compression and decompression. libjpeg is a library that implements JPEG image encoding,
	decoding and transcoding.
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--mandir=/usr/share/man \
		--with-jpeg8 \
		--disable-static \
		--docdir=/usr/share/doc/libjpeg-turbo-1.5.2
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
	%defattr(-,root,root)
	%{_bindir}/cjpeg
	%{_bindir}/djpeg
	%{_bindir}/jpegtran
	%{_bindir}/rdjpgcom
	%{_bindir}/tjbench
	%{_bindir}/wrjpgcom
	%{_includedir}/*.h
	%{_libdir}/libjpeg.so
	%{_libdir}/libjpeg.so.8
	%{_libdir}/libjpeg.so.8.1.2
	%{_libdir}/libturbojpeg.so
	%{_libdir}/libturbojpeg.so.0
	%{_libdir}/libturbojpeg.so.0.1.0
	%{_libdir}/pkgconfig/libjpeg.pc
	%{_libdir}/pkgconfig/libturbojpeg.pc
	%{_datarootdir}/doc/%{name}-%{version}
	%{_mandir}/man1/*.gz
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 1.5.2-1
-	Initial build.	First version