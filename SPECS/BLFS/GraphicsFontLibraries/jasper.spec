#		  http://www.ece.uvic.ca/~frodo/jasper/software/jasper-2.0.12.tar.gz
Summary:	The JasPer Project is an open-source initiative to provide a free software-based reference implementation of the JPEG-2000 codec
Name:		jasper
Version:	2.0.12
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
#	Requires:	CMake-3.9.1:	libjpeg-turbo-1.5.2
Source0:	%{name}-%{version}.tar.gz
%description
	The JasPer Project is an open-source initiative to provide a free software-based reference implementation of the JPEG-2000 codec
%prep
%setup -q -n %{NAME}-%{VERSION}
mkdir BUILD
%build
	cd    BUILD
	cmake -DCMAKE_INSTALL_PREFIX=/usr \
		-DCMAKE_BUILD_TYPE=Release \
		-DCMAKE_SKIP_INSTALL_RPATH=YES \
		-DCMAKE_INSTALL_DOCDIR=%{_datarootdir}/doc/%{NAME}-%{VERSION} \
		..
	make %{?_smp_mflags}
%install
	cd    BUILD
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}%{_datarootdir}/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
	%defattr(-,root,root)
	%{_bindir}/imgcmp
	%{_bindir}/imginfo
	%{_bindir}/jasper
	%{_includedir}/jasper
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/*.4
	%{_libdir}/pkgconfig/j*.pc
	%{_mandir}/man1/*.gz
#	%%{_datarootdir}/licenses/%%{name}/LICENSE

%{_datarootdir}/doc/%{NAME}-%{VERSION}
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 2.0.12-1
-	Initial build.	First version