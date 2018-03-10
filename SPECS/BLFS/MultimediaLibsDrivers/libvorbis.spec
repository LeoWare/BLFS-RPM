#		  https://downloads.xiph.org/releases/vorbis/libvorbis-1.3.5.tar.xz
Summary:	The libvorbis package contains a general purpose audio and music encoding format
Name:		libvorbis
Version:	1.3.5
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Requires:	libogg
Source0:	%{name}-%{version}.tar.xz
%description
	The libvorbis package contains a general purpose audio and music encoding format.
	This is useful for creating (encoding) and playing (decoding) sound in an
	open (patent free) format. 
%prep
%setup -q -n %{NAME}-%{VERSION}
sed -i '/components.png \\/{n;d}' doc/Makefile.in
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static
#		--docdir=%{_datarootdir}/doc/%{NAME}-%{VERSION}
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	install -vdm 755 %{buildroot}%{_datarootdir}/doc/%{NAME}-%{VERSION}
	install -v -m644 doc/Vorbis* %{buildroot}%{_datarootdir}/doc/%{NAME}-%{VERSION}
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
	%{_includedir}/vorbis
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/*.2
	%{_libdir}/*.3
	%{_libdir}/*.7
	%{_libdir}/*.8
	%{_libdir}/*.11
	%{_libdir}/pkgconfig/*.pc
	%{_datarootdir}/aclocal/vorbis.m4
	%{_datarootdir}/doc/%{NAME}-%{VERSION}
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 1.3.5-1
-	Initial build.	First version