#	libinput-1.8.1.tar.xz
Summary:	libinput is a library that handles input devices for display servers and other applications that need to directly deal with input devices. 
Name:		libinput
Version:	1.8.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	libevdev >= 1.5.7, mtdev >= 1.1.5 
Source0:	%{name}-%{version}.tar.xz
%description
	libinput is a library that handles input devices for display servers and other applications that need to directly deal with input devices. 
%define		XORG_CONFIG	--prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --disable-static
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure %{XORG_CONFIG} \
		--disable-libwacom \
		--disable-debug-gui \
		--disable-tests \
		--disable-documentation \
		--with-udev-dir=/lib/udev
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
	/sbin/ldconfig
	pushd /usr/share/info
		rm -v dir
		for f in *;do install-info $f dir 2>/dev/null;done
	popd
%postun
	/sbin/ldconfig
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Fri Feb 16 2018 baho-utot <baho-utot@columbus.rr.com> libinput-1.8.1-1
-	Initial build.	First version