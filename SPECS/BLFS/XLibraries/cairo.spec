#		 https://www.cairographics.org/releases/cairo-1.14.10.tar.xz
Summary:	Cairo is a 2D graphics library with support for multiple output devices
Name:		cairo
Version:	1.14.10
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
#	Requires:	 libpng-1.6.31 and Pixman-0.34.0  Fontconfig-2.12.4, GLib-2.52.3 (required for most GUIs) and Xorg Libraries 
Source0:	%{name}-%{version}.tar.xz
%description
	Cairo is a 2D graphics library with support for multiple output devices.
	Currently supported output targets include the X Window System, win32,
	image buffers, PostScript, PDF and SVG. Experimental backends include OpenGL,
	Quartz and XCB file output. Cairo is designed to produce consistent output on
	all output media while taking advantage of display hardware acceleration when
	available (e.g., through the X Render Extension). The Cairo API provides
	operations similar to the drawing operators of PostScript and PDF. Operations
	in Cairo include stroking and filling cubic Bézier splines, transforming and
	compositing translucent images, and antialiased text rendering. All drawing
	operations can be transformed by any affine transformation (scale, rotation,
	shear, etc.). 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static \
		--enable-tee
#		--docdir=%{_datarootdir}/doc/%{NAME}-%{VERSION}
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
	%defattr(-,root,root)
	%{_bindir}/cairo-sphinx
	%{_bindir}/cairo-trace
	%{_includedir}/cairo
	%{_libdir}/cairo
	%{_libdir}/*.so
	%{_libdir}/*.2
	%{_libdir}/*.10
	%{_libdir}/pkgconfig/*.pc
	%{_datarootdir}/gtk-doc/html/cairo
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 1.14.10-1
-	Initial build.	First version