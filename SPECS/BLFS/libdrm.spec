#	libdrm-2.4.82.tar.bz2
Summary:	libdrm provides a user space library for accessing the DRM, direct rendering manager
Name:		libdrm
Version:	2.4.82
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.bz2
%description
	libdrm provides a user space library for accessing the DRM, direct rendering manager,
	on operating systems that support the ioctl interface. libdrm is a low-level library,
	typically used by graphics drivers such as the Mesa DRI drivers, the X drivers, libva
	and similar projects.

%prep
	install -vdm 755  %{_builddir}/%{name}-%{version}
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		 --enable-udev
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
	for f in *
		do install-info $f dir 2>/dev/null
	done
	popd
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Tue Jan 09 2018 baho-utot <baho-utot@columbus.rr.com> libdrm-2.4.82-1
-	Initial build.	First version