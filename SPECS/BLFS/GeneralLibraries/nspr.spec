#		https://archive.mozilla.org/pub/nspr/releases/v4.16/src/nspr-4.16.tar.gz
Summary:	Netscape Portable Runtime (NSPR) provides a platform-neutral API for system level and libc like functions
Name:		nspr
Version:	4.16
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}-%{version}.tar.gz
%description
	Netscape Portable Runtime (NSPR) provides a platform-neutral API for system level and libc like functions
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	cd nspr
	sed -ri 's#^(RELEASE_BINS =).*#\1#' pr/src/misc/Makefile.in
	sed -i 's#$(LIBRARY) ##'            config/rules.mk
	./configure \
		--prefix=%{_prefix} \
		--with-mozilla \
		--with-pthreads \
		$([ $(uname -m) = x86_64 ] && echo --enable-64bit)
#		--docdir=%{_datarootdir}/doc/%{NAME}-%{VERSION}
	make %{?_smp_mflags}
%install
	cd nspr
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
	%{_bindir}/nspr-config
	%{_includedir}/nspr
	%{_libdir}/*.so
	%{_libdir}/pkgconfig/nspr.pc
	%{_datarootdir}/aclocal/nspr.m4
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 4.16-1
-	Initial build.	First version