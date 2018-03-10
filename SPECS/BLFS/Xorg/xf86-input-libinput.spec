#	xf86-input-libinput-0.25.1.tar.bz2
Summary:	The X.Org Libinput Driver is a thin wrapper around libinput and allows for libinput to be used for input devices in X
Name:		xf86-input-libinput
Version:	0.25.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	libinput >= 1.8.1, xorg-server >= 1.19.3 
Source0:	%{name}-%{version}.tar.bz2
%description
	The X.Org Libinput Driver is a thin wrapper around libinput and allows for libinput to
	be used for input devices in X. This driver can be used as as drop-in replacement for
	evdev and synaptics.
%define		XORG_CONFIG	--prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --disable-static
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure %{XORG_CONFIG}
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
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> xf86-input-libinput-0.25.1-1
-	Initial build.	First version