#		 https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs921/ghostscript-9.21.tar.gz
Summary:	Ghostscript is a versatile processor for PostScript data with the ability to render PostScript to different targets
Name:		ghostscript
Version:	9.21
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
#	FreeType-2.8, libjpeg-turbo-1.5.2, libpng-1.6.31, LibTIFF-4.0.8, and Little CMS-2.8 
Source0:	%{name}-%{version}.tar.gz
Source1:	https://downloads.sourceforge.net/gs-fonts/ghostscript-fonts-std-8.11.tar.gz
Source2:	https://downloads.sourceforge.net/gs-fonts/gnu-gs-fonts-other-6.0.tar.gz
%description
	Ghostscript is a versatile processor for PostScript data with the ability to render
	PostScript to different targets. It is a mandatory part of the cups printing stack. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%setup -q -T -D -a 1  -n %{name}-%{version}
%setup -q -T -D -a 2  -n %{name}-%{version}
%build
	rm -rf freetype lcms2 jpeg libpng
	./configure \
		--prefix=%{_prefix} \
		--disable-compile-inits \
		--enable-dynamic \
		--with-system-libtiff 
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	install -vdm 755 %{buildroot}%{_datarootdir}/doc
	ln -sfvn ../%{name}/%{version}/doc %{buildroot}%{_datarootdir}/doc/%{name}-%{version}
	install -vdm 755 %{buildroot}%{_datarootdir}/%{name}
	mv fonts %{buildroot}%{_datarootdir}/%{name}
	#	Copy license/copying file 
	install -D -m644 LICENSE %{buildroot}%{_datarootdir}/licenses/%{name}/LICENSE
	rm -rf %{buildroot}%{_mandir}/de
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%post
	/sbin/ldconfig
	fc-cache -v /usr/share/ghostscript/fonts/
%postun
	/sbin/ldconfig
%files
	%defattr(-,root,root)
	%{_datarootdir}/licenses/%{name}/LICENSE
	%{_bindir}/dvipdf
	%{_bindir}/eps2eps
   	%{_bindir}/font2c
   	%{_bindir}/gs
	%{_bindir}/gsbj
   	%{_bindir}/gsdj
   	%{_bindir}/gsdj500
   	%{_bindir}/gslj
   	%{_bindir}/gslp
   	%{_bindir}/gsnd
   	%{_bindir}/lprsetup.sh
   	%{_bindir}/pdf2dsc
   	%{_bindir}/pdf2ps
   	%{_bindir}/pf2afm
   	%{_bindir}/pfbtopfa
   	%{_bindir}/pphs
   	%{_bindir}/printafm
   	%{_bindir}/ps2ascii
   	%{_bindir}/ps2epsi
   	%{_bindir}/ps2pdf
   	%{_bindir}/ps2pdf12
   	%{_bindir}/ps2pdf13
   	%{_bindir}/ps2pdf14
   	%{_bindir}/ps2pdfwr
   	%{_bindir}/ps2ps
   	%{_bindir}/ps2ps2
   	%{_bindir}/unix-lpr.sh
   	%{_bindir}/wftopfa
	%{_libdir}/%{name}/%{version}
	%{_datarootdir}/doc/%{name}-%{version}
	%{_datarootdir}/%{name}/%{version}
	%{_datarootdir}/%{NAME}/fonts
	%{_mandir}/man1/*.gz
%changelog
*	Fri Feb 16 2018 baho-utot <baho-utot@columbus.rr.com> 9.21-1
-	Initial build.	First version