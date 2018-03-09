#		https://downloads.xiph.org/releases/theora/libtheora-1.1.1.tar.xz 
Summary:	libtheora is a reference implementation of the Theora video compression format being developed by the Xiph.Org Foundation
Name:		libtheora
Version:	1.1.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Requires:	libogg, libvorbis
Source0:	%{name}-%{version}.tar.xz
%description
	libtheora is a reference implementation of the Theora video compression format being developed by the Xiph.Org Foundation
%prep
%setup -q -n %{NAME}-%{VERSION}
sed -i 's/png_\(sizeof\)/\1/g' examples/png2theora.c
%build
	./configure \
		--prefix=%{_prefix} \
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
	%{_includedir}/theora
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/*.1
	%{_libdir}/*.2
	%{_libdir}/*.4
	%{_libdir}/*.10
	%{_libdir}/pkgconfig/*.pc
	%{_datarootdir}/doc/%{NAME}-%{VERSION}
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 1.1.1-1
-	Initial build.	First version