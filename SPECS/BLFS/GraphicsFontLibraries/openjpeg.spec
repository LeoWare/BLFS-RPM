#		https://downloads.sourceforge.net/openjpeg.mirror/openjpeg-1.5.2.tar.gz
Summary:	OpenJPEG is an open-source implementation of the JPEG-2000 standard
Name:		openjpeg
Version:	1.5.2
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
#	Requires:	Little CMS-2.8, libpng-1.6.31, LibTIFF-4.0.8
Source0:	%{name}-%{version}.tar.gz
%description
	OpenJPEG is an open-source implementation of the JPEG-2000 standard.
	OpenJPEG fully respects the JPEG-2000 specifications and can
	compress/decompress lossless 16-bit images. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	autoreconf -f -i
	./configure \
		--prefix=%{_prefix} \
		 --disable-static
#		--docdir=%{_datarootdir}/doc/%{NAME}-%{VERSION}
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
		install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
	%defattr(-,root,root)
	%{_bindir}/image_to_j2k
	%{_bindir}/j2k_dump
	%{_bindir}/j2k_to_image
	%{_includedir}/openjpeg-1.5
	%{_libdir}/libopenjpeg.so
	%{_libdir}/libopenjpeg.so.1
	%{_libdir}/libopenjpeg.so.1.5.2
	%{_libdir}/pkgconfig/libopenjpeg.pc
	%{_libdir}/pkgconfig/libopenjpeg1.pc
	%{_datarootdir}/doc/openjpeg-1.5/LICENSE
	%{_datarootdir}/licenses/%{name}/LICENSE
	%{_mandir}/man1/*.gz
	%{_mandir}/man3/*.gz
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 1.5.2-1
-	Initial build.	First version