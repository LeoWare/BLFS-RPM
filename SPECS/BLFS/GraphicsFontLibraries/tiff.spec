#		http://download.osgeo.org/libtiff/tiff-4.0.8.tar.gz
Summary:	The LibTIFF package contains the TIFF libraries and associated utilities
Name:		tiff
Version:	4.0.8
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
#	Requires:	libjpeg-turbo-1.5.2 
Source0:	%{name}-%{version}.tar.gz
%description
	The LibTIFF package contains the TIFF libraries and associated utilities.
	The libraries are used by many programs for reading and writing TIFF files
	and the utilities are used for general work with TIFF files.
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
		install -D -m644 COPYRIGHT %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
	%defattr(-,root,root)
	%{_bindir}/fax2ps
	%{_bindir}/fax2tiff
	%{_bindir}/pal2rgb
	%{_bindir}/ppm2tiff
	%{_bindir}/raw2tiff
	%{_bindir}/tiff2bw
	%{_bindir}/tiff2pdf
	%{_bindir}/tiff2ps
	%{_bindir}/tiff2rgba
	%{_bindir}/tiffcmp
	%{_bindir}/tiffcp
	%{_bindir}/tiffcrop
	%{_bindir}/tiffdither
	%{_bindir}/tiffdump
	%{_bindir}/tiffinfo
	%{_bindir}/tiffmedian
	%{_bindir}/tiffset
	%{_bindir}/tiffsplit
	%{_includedir}/*.h
	%{_includedir}/tiffio.hxx
	%{_libdir}/libtiff.so
	%{_libdir}/libtiff.so.5
	%{_libdir}/libtiff.so.5.2.6
	%{_libdir}/libtiffxx.so
	%{_libdir}/libtiffxx.so.5
	%{_libdir}/libtiffxx.so.5.2.6
	%{_libdir}/pkgconfig/libtiff-4.pc
	%{_datarootdir}/doc/%{NAME}-%{VERSION}
	%{_mandir}/man1/*.gz
	%{_mandir}/man3/*.gz
	/usr/share/licenses/tiff/LICENSE
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 4.0.8-1
-	Initial build.	First version