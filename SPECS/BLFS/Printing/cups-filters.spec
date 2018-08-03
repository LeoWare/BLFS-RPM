#		https://www.openprinting.org/download/cups-filters/cups-filters-1.17.2.tar.xz
Summary:	The CUPS Filters package contains backends, filters and other software
Name:		cups-filters
Version:	1.17.2
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
#	Requires:	 Cups-2.2.4, GLib-2.52.3, ghostscript-9.21, IJS-0.35, Little CMS-2.8, mupdf-1.11 (mutool), Poppler-0.57.0, and Qpdf-6.0.0 
Source0:	%{name}-%{version}.tar.xz
%description
	The CUPS Filters package contains backends, filters and other software that was once 
	part of the core CUPS distribution but is no longer maintained by Apple Inc
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--sysconfdir=%{_sysconfdir} \
		--localstatedir=%{_localstatedir} \
		--without-rcdir \
		--disable-static \
		--disable-avahi \
		--docdir=%{_datarootdir}/doc/%{NAME}-%{VERSION}
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
	%defattr(-,root,root,-)
	%{_sysconfdir}/cups/cups-browsed.conf
	%{_sysconfdir}/fonts/conf.d/99pdftoopvp.conf
	%{_bindir}/driverless
	%{_bindir}/foomatic-rip
	%{_bindir}/ttfread
	%{_includedir}/cupsfilters/*.h
	%{_includedir}/fontembed/*.h
	%{_libdir}/cups/backend
	%{_libdir}/cups/driver/driverless
	%{_libdir}/cups/filter
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/*.1
	%{_libdir}/pkgconfig/*.pc
	%{_sbindir}/cups-browsed
	%{_datarootdir}/cups/banners
	%{_datarootdir}/cups/braille
	%{_datarootdir}/cups/charsets
	%{_datarootdir}/cups/data
	%{_datarootdir}/cups/drv
	%{_datarootdir}/cups/mime
	%{_datarootdir}/cups/ppdc
	%{_datarootdir}/doc/%{NAME}-%{VERSION}
	%{_datarootdir}/ppd/cupsfilters
	%{_mandir}/man1/*.gz
	%{_mandir}/man5/*.gz
	%{_mandir}/man8/*.gz
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 1.17.2-1
-	Initial build.	First version