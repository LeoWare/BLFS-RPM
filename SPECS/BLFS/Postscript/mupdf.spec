#		 http://www.mupdf.com/downloads/archive/mupdf-1.11-source.tar.gz
Summary:	MuPDF is a lightweight PDF and XPS viewer.
Name:		mupdf
Version:	1.11
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
#	Requires:		Xorg Libraries, REC:  HarfBuzz-1.4.8, libjpeg-turbo-1.5.2, OpenJPEG-2.2.0, and cURL-7.55.1 
Source0:	%{name}-%{version}-source.tar.gz
Patch0:		mupdf-1.11-shared_libs-1.patch
Patch1:		mupdf-1.11-openjpeg-2.patch
%description
	MuPDF is a lightweight PDF and XPS viewer.
%prep
%setup -q -c -n %{NAME}-%{VERSION}
mv %{NAME}-%{VERSION}-source/* .
%patch0 -p1
%patch1 -p1
	rm -rf thirdparty/curl
	rm -rf thirdparty/freetype
	rm -rf thirdparty/harfbuzz
	rm -rf thirdparty/jpeg
	rm -rf thirdparty/libjpeg
	rm -rf thirdparty/openjpeg
	rm -rf thirdparty/zlib 
%build
	make %{?_smp_mflags} build=release
%install
	make DESTDIR=%{buildroot} \
		prefix=/usr \
		build=release \
		docdir=/usr/share/doc/mupdf-1.11 \
		install
	install -vdm 755 %{buildroot}/usr/bin
	ln -sfv mupdf-x11-curl %{buildroot}/usr/bin/mupdf
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
	%{_bindir}/mujstest
	%{_bindir}/mupdf
	%{_bindir}/mupdf-gl
	%{_bindir}/mupdf-x11
	%{_bindir}/mupdf-x11-curl
	%{_bindir}/muraster
	%{_bindir}/mutool
	%{_includedir}/%{NAME}
	%{_libdir}/*.so
	%{_datarootdir}/doc/%{NAME}-%{VERSION}
	%{_mandir}/man1/*.gz
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 1.11-1
-	Initial build.	First version