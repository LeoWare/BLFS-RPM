#		 https://downloads.sourceforge.net/pcre/pcre2-10.30.tar.bz2 
Summary:	The PCRE2 package contains a new generation of the Perl Compatible Regular Expression libraries
Name:		pcre2
Version:	10.30
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}-%{version}.tar.bz2
%description
	The PCRE2 package contains a new generation of the Perl Compatible Regular Expression libraries.
	These are useful for implementing regular expression pattern matching using the same syntax and
	semantics as Perl. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--docdir=%{_datarootdir}/doc/%{NAME}-%{VERSION} \
		--enable-unicode \
		--enable-pcre2-16 \
		--enable-pcre2-32 \
		--enable-pcre2grep-libz \
		--enable-pcre2grep-libbz2 \
		--enable-pcre2test-libreadline \
		--disable-static                 
	make %{?_smp_mflags}
%install
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
#	%%{buildroot}%%{_datarootdir}/licenses/%%{name}/LICENSE
	%{_bindir}/pcre2-config
	%{_bindir}/pcre2grep
	%{_bindir}/pcre2test
	%{_includedir}/*.h
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/*.2
	%{_libdir}/pkgconfig/*.pc
	%{_datarootdir}/doc/%{NAME}-%{VERSION}
	%{_mandir}/man1/*.gz
	%{_mandir}/man3/*.gz
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 10.30-1
-	Initial build.	First version