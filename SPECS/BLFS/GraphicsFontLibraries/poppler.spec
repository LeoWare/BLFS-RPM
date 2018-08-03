#		https://poppler.freedesktop.org/poppler-0.57.0.tar.xz
Summary:	The additional package consists of encoding files for use with Poppler
Name:		poppler
Version:	0.57.0
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
#	Requires:	Fontconfig-2.12.4,  Rec: Cairo-1.14.10, libjpeg-turbo-1.5.2, libpng-1.6.31, NSS-3.32, and OpenJPEG-1.5.2 
Source0:	%{name}-%{version}.tar.xz
Source1:	poppler-data-0.4.8.tar.gz
%description
	The additional package consists of encoding files for use with Poppler.
	The encoding files are optional and Poppler will automatically read them
	if they are present. When installed, they enable Poppler to render CJK
	and Cyrillic properly. 
%prep
#	install -vdm 755  %{_builddir}/%{name}-%{version}
%setup -q -n %{NAME}-%{VERSION}
%setup -q -T -D -a 1  -n %{name}-%{version}
%build
	./configure \
		--prefix=%{_prefix} \
		--sysconfdir=/etc \
		--disable-static \
		--enable-build-type=release \
		--enable-cmyk \
		--enable-xpdf-headers \
		--with-testdatadir=$PWD/testfiles
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	install -v -m755 -d 		%{buildroot}/usr/share/doc/poppler-0.57.0
	install -v -m644 README*	%{buildroot}/usr/share/doc/poppler-0.57.0
	cp -vr glib/reference/html	%{buildroot}/usr/share/doc/poppler-0.57.0
	cd poppler-data-0.4.8
	make prefix=/usr DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	install -D -m644 COPYING %{buildroot}%{_datarootdir}/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
	%defattr(-,root,root)
	%{_datarootdir}/licenses/%{name}/LICENSE
	%{_bindir}/pdfdetach
	%{_bindir}/pdffonts
	%{_bindir}/pdfimages
	%{_bindir}/pdfinfo
	%{_bindir}/pdfseparate
	%{_bindir}/pdfsig
	%{_bindir}/pdftocairo
	%{_bindir}/pdftohtml
	%{_bindir}/pdftoppm
	%{_bindir}/pdftops
	%{_bindir}/pdftotext
	%{_bindir}/pdfunite
	%{_includedir}/poppler
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/*.8
	%{_libdir}/*.68
	%{_libdir}/pkgconfig/*.pc
	%{_datarootdir}/doc/poppler-0.57.0
	%{_datarootdir}/gir-1.0/Poppler-0.18.gir
	%{_datarootdir}/gtk-doc/html/poppler
	%{_mandir}/man1/*.gz
	%{_datarootdir}/pkgconfig/poppler-data.pc
	%{_datarootdir}/poppler
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 0.57.0-1
-	Initial build.	First version