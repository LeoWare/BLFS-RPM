#		 https://www.openprinting.org/download/ijs/download/ijs-0.35.tar.bz2
Summary:	The IJS package contains a library which implements a protocol for transmission of raster page images
Name:		ijs
Version:	0.35
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}-%{version}.tar.bz2
%description
	The IJS package contains a library which implements a protocol for transmission of raster page images
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--mandir=/usr/share/man \
		--enable-shared \
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
	%{_bindir}/ijs-config
	%{_bindir}/ijs_client_example
	%{_bindir}/ijs_server_example
	%{_includedir}/ijs
	%{_libdir}/libijs-0.35.so
	%{_libdir}/libijs.so
	%{_libdir}/pkgconfig/ijs.pc
	%{_mandir}/man1/ijs-config.1.gz

%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 0.35-1
-	Initial build.	First version