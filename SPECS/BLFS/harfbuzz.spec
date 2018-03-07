#		https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-1.4.8.tar.bz2
Summary:	The HarfBuzz package contains an OpenType text shaping engine
Name:		harfbuzz
Version:	1.4.8
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
#Requires:	GLib-2.52.3 (required for Pango), ICU-59.1 and FreeType-2.8 (after HarfBuzz-1.4.8 is installed, reinstall FreeType-2.8) 
Source0:	%{name}-%{version}.tar.bz2
%description
	The HarfBuzz package contains an OpenType text shaping engine
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--with-gobject
#		--docdir=%{_datarootdir}/doc/%{NAME}-%{VERSION}
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
	%{_bindir}/hb-ot-shape-closure
	%{_bindir}/hb-shape
	%{_bindir}/hb-view
	%{_includedir}/harfbuzz
	%{_libdir}/girepository-1.0/HarfBuzz-0.0.typelib
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/*.8
	%{_libdir}/pkgconfig/*.pc
	%{_datarootdir}/gir-1.0/HarfBuzz-0.0.gir
	%{_datarootdir}/gtk-doc/html/harfbuzz
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 1.4.8-1
-	Initial build.	First version