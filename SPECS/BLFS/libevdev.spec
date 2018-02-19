#	libevdev-1.5.7.tar.xz
Summary:	The libevdev package contains common functions for Xorg input drivers. 
Name:		libevdev
Version:	1.5.7
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}-%{version}.tar.xz
%description
	The libevdev package contains common functions for Xorg input drivers. 
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
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> libevdev-1.5.7-1
-	Initial build.	First version