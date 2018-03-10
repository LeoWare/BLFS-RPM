#		https://github.com/uclouvain/openjpeg/archive/v2.2.0/openjpeg-2.2.0.tar.gz
Summary:	OpenJPEG is an open-source implementation of the JPEG-2000 standard.
Name:		openjpeg2
Version:	2.2.0
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Requires:	CMake-3.9.1:	Little CMS-2.8, libpng-1.6.31, LibTIFF-4.0.8
Source0:	openjpeg-%{version}.tar.gz
%description
	OpenJPEG is an open-source implementation of the JPEG-2000 standard.
	OpenJPEG fully respects the JPEG-2000 specifications and can
	compress/decompress lossless 16-bit images. 
%prep
%setup -q -c -n openjpeg-%{VERSION}
	cd openjpeg-%{VERSION};	mv * ../; cd -
	mkdir -v build
%build
	cd build
	cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr ..
%install
	cd build
	make DESTDIR=%{buildroot} install
	pushd ../doc
	for man in man/man?/* ; do
		install -v -D -m 644 $man %{buildroot}/usr/share/$man
	done
	popd
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
	%{_bindir}/opj_compress
	%{_bindir}/opj_decompress
	%{_bindir}/opj_dump
	%{_includedir}/openjpeg-2.2
	%{_libdir}/*.a
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/*.7
	%{_libdir}/openjpeg-2.2
	%{_libdir}/pkgconfig/libopenjp2.pc
	%{_mandir}/man1/*.gz
	%{_mandir}/man3/*.gz
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 2.2.0-1
-	Initial build.	First version