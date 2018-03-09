#		https://downloads.xiph.org/releases/ogg/libogg-1.3.2.tar.xz 
Summary:	The libogg package contains the Ogg file structure
Name:		libogg
Version:	1.3.2
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}-%{version}.tar.xz
%description
	The libogg package contains the Ogg file structure.
	This is useful for creating (encoding) or playing
	(decoding) a single physical bit stream
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static \
		--docdir=%{_datarootdir}/doc/%{NAME}-%{VERSION}
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
	%{_includedir}/ogg
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/*.2
	%{_libdir}/pkgconfig/*.pc
	%{_datarootdir}/aclocal/ogg.m4
	%{_datarootdir}/doc/%{NAME}-%{VERSION}
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 1.3.2-1
-	Initial build.	First version