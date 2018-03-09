#		https://downloads.sourceforge.net/libmng/libmng-2.0.3.tar.xz 
Summary:	The libmng libraries are used by programs wanting to read and write Multiple-image Network Graphics (MNG) files which are the animation equivalents to PNG files
Name:		libmng
Version:	2.0.3
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
#	Requires:	 libjpeg-turbo-1.5.2 and Little CMS-2.8 
Source0:	%{name}-%{version}.tar.xz
%description
	The libmng libraries are used by programs wanting to read and write
	Multiple-image Network Graphics (MNG) files which are the animation
	equivalents to PNG files
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	install -v -m755 -d %{buildroot}%{_datarootdir}/doc/%{name}-%{version}
	install -v -m644 doc/*.txt %{buildroot}%{_datarootdir}/doc/%{name}-%{version}
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
	%{_includedir}/*.h
	%{_libdir}/*.so
	%{_libdir}/*.2
	%{_libdir}/pkgconfig/libmng.pc
	%{_mandir}/man3/*.gz
	%{_mandir}/man5/*.gz
	%{_datarootdir}/doc/%{name}-%{version}
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 2.0.3-1
-	Initial build.	First version