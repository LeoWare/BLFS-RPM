#	xinit-1.3.4.tar.bz2
Summary:	The xinit package contains a usable script to start the xserver
Name:		xinit
Version:	1.3.4
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	xorg-libs
Source0:	%{name}-%{version}.tar.bz2
%description
	The xinit package contains a usable script to start the xserver
	This package is not a part of the Xorg katamari and is provided
	only as a dependency to other packages or for testing the
	completed Xorg installation
%define		XORG_CONFIG	--prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --disable-static
%prep
%setup -q -n %{NAME}-%{VERSION}
sed -e '/$serverargs $vtarg/ s/serverargs/: #&/' -i startx.cpp
%build
	./configure %{XORG_CONFIG} \
		--with-xinitdir=/etc/X11/app-defaults
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
%postun
	/sbin/ldconfig
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Fri Feb 16 2018 baho-utot <baho-utot@columbus.rr.com> xinit-1.3.4-1
-	Initial build.	First version