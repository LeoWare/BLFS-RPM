#	  http://ftp.gnome.org/pub/gnome/sources/glib/2.52/glib-2.52.3.tar.xz
Summary:	The GLib package contains low-level libraries useful for providing data structure handling for C
Name:		glib
Version:	2.52.3
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}-%{version}.tar.xz
%description
	The GLib package contains low-level libraries useful for providing data structure
	handling for C, portability wrappers and interfaces for such runtime functionality
	as an event loop, threads, dynamic loading and an object system.
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--with-pcre=system
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
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> glib-2.52.3-1
-	Initial build.	First version