#	pixman-0.34.0.tar.gz
Summary:	The Pixman package contains a library that provides low-level pixel manipulation features such as image compositing and trapezoid rasterization. 
Name:		pixman
Version:	0.34.0
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.gz
%description
	The Pixman package contains a library that provides low-level pixel manipulation features such as image compositing and trapezoid rasterization. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static
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
	for f in *;do; install-info $f dir; 2>/dev/null	done
	popd
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> pixman-0.34.0-1
-	Initial build.	First version