#	libxcb-1.12.tar.bz2
Summary:	The libxcb package provides an interface to the X Window System protocol
Name:		libxcb	
Version:	1.12
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.bz2
Patch0:		libxcb-1.12-python3-1.patch
%description
	The libxcb package provides an interface to the X Window System protocol, which replaces the current
	Xlib interface. Xlib can also use XCB as a transport layer, allowing software to make requests and
	receive responses with both. 

%define		XORG_CONFIG	--prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --disable-static
%prep
%setup -q -n %{NAME}-%{VERSION}
%patch0 -p1
	sed -i "s/pthread-stubs//" configure
%build
	./configure %{XORG_CONFIG} \
		--enable-xinput \
		--without-doxygen \
		--docdir='${datadir}'/doc/libxcb-1.12
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post
	pushd /usr/share/info
	rm -v dir
	for f in *;do install-info $f dir 2>/dev/null;done
	popd
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Mon Feb 11 2018 baho-utot <baho-utot@columbus.rr.com> -1
-	Initial build.	First version