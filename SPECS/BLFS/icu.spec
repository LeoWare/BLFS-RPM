#		http://download.icu-project.org/files/icu4c/59.1/icu4c-59_1-src.tgz
Summary:	The International Components for Unicode (ICU) package is a mature, widely used set of C/C++ libraries
Name:		icu
Version:	59.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}4c-59_1-src.tgz
%description
	The International Components for Unicode (ICU) package is a mature, widely used set
	of C/C++ libraries providing Unicode and Globalization support for software applications.
	ICU is widely portable and gives applications the same results on all platforms. 
%prep
#install -vdm 755 %{_builddir}/%{NAME}-%{VERSION}
%setup -q -c -n %{NAME}-%{VERSION}
%build
	cd icu/source
	sed -i 's/xlocale/locale/' i18n/digitlst.cpp
	./configure \
		--prefix=%{_prefix}
#		--docdir=%{_datarootdir}/doc/%{NAME}-%{VERSION}
	make %{?_smp_mflags}
%install
	cd icu/source
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
	%{_bindir}/derb
	%{_bindir}/genbrk
	%{_bindir}/gencfu
	%{_bindir}/gencnval
	%{_bindir}/gendict
	%{_bindir}/genrb
	%{_bindir}/icu-config
	%{_bindir}/icuinfo
	%{_bindir}/makeconv
	%{_bindir}/pkgdata
	%{_bindir}/uconv
	%{_includedir}/unicode/*.h
	%{_libdir}/%{NAME}
	%{_libdir}/*.so
	%{_libdir}/*.1
	%{_libdir}/*.59
	%{_libdir}/pkgconfig/*.pc
	%{_sbindir}/escapesrc
	%{_sbindir}/genccode
	%{_sbindir}/gencmn
	%{_sbindir}/gennorm2
	%{_sbindir}/gensprep
	%{_sbindir}/icupkg
	%{_datarootdir}/%{NAME}/%{VERSION}
	%{_mandir}/man1/*.gz
	%{_mandir}/man8/*.gz
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 59_1-1
-	Initial build.	First version