#	xf86-input-synaptics-1.9.0.tar.bz2
Summary:	The Xorg Synaptics Driver package contains the X.Org Input Driver
Name:		xf86-input-synaptics
Version:	1.9.0
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	libevdev >= 1.5.7, xorg-server >= 1.19.3 
Source0:	%{name}-%{version}.tar.bz2
%description
	The Xorg Synaptics Driver package contains the X.Org Input Driver, support programs and
	SDK for Synaptics touchpads. Even though the evdev driver can handle touchpads very well,
	this driver is required if you want to use advanced features like multi tapping, scrolling
	with touchpad, turning the touchpad off while typing, etc. 
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
*	Fri Feb 16 2018 baho-utot <baho-utot@columbus.rr.com> xf86-input-synaptics-1.9.0-1
-	Initial build.	First version