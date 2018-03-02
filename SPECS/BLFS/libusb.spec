#		https://github.com/libusb/libusb/releases/download/v1.0.21/libusb-1.0.21.tar.bz2
Summary:	The libusb package contains a library used by some applications for USB device access
Name:		libusb
Version:	1.0.21
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.bz2
%description
	The libusb package contains a library used by some applications for USB device access
%prep
%setup -q -n %{NAME}-%{VERSION}
	sed -i "s/^PROJECT_LOGO/#&/" doc/doxygen.cfg.in
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static
	make -j1
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
	%defattr(-,root,root)
	%{_includedir}/libusb-1.0
	%{_libdir}/libusb-1.0.so
	%{_libdir}/libusb-1.0.so.0
	%{_libdir}/libusb-1.0.so.0.1.0
	%{_libdir}/pkgconfig/libusb-1.0.pc
%changelog
*	Thu Mar 01 2018 baho-utot <baho-utot@columbus.rr.com> 1.0.21-1
-	Initial build.	First version