#		https://downloads.sourceforge.net/lcms/lcms2-2.8.tar.gz
Summary:	The Little Color Management System is a small-footprint color management engine
Name:		lcms2
Version:	2.8
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
#	Requires:	 libjpeg-turbo-1.5.2 and LibTIFF-4.0.8 
Source0:	%{name}-%{version}.tar.gz
%description
	The Little Color Management System is a small-footprint color management engine,
	with special focus on accuracy and performance. It uses the
	International Color Consortium standard (ICC), which is the modern standard for
	color management. 
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
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
	%defattr(-,root,root)
	%{_bindir}/jpgicc
	%{_bindir}/linkicc
	%{_bindir}/psicc
	%{_bindir}/tificc
	%{_bindir}/transicc
	%{_includedir}/*.h
	%{_libdir}/liblcms2.so
	%{_libdir}/liblcms2.so.2
	%{_libdir}/liblcms2.so.2.0.8
	%{_libdir}/pkgconfig/lcms2.pc
	%{_mandir}/man1/*.gz
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 2.8-1
-	Initial build.	First version