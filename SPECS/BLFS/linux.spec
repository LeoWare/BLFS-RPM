Summary:	The Linux package contains the Linux kernel. 
Name:		linux
Version:	4.12.7
Release:	2
License:	Any
URL:		Any
Group:		LFS/Base
Vendor:		Octothorpe
Distribution:	LFS-8.1
ExclusiveArch:	x86_64
Requires:	filesystem
Source0:	https://www.kernel.org/pub/linux/kernel/v4.x/%{name}-%{version}.tar.xz
Patch0:		config-4.12.7.sound.patch
Patch1:		config-4.12.7.graphics.patch
Patch2:		config-4.12.7.powersave.patch
Patch3:		config-4.12.7.network.patch
%description
	The Linux package contains the Linux kernel. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	make mrproper
	make defconfig
	#	patch -p0 -i %{_sourcedir}/config-4.12.7.powersave.patch
	patch -p0 -i %{_sourcedir}/config-4.12.7.network.patch
	patch -p0 -i %{_sourcedir}/config-4.12.7.sound.patch
	patch -p0 -i %{_sourcedir}/config-4.12.7.graphics.patch
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} INSTALL_MOD_PATH=%{buildroot} modules_install
	install -vdm 755 %{buildroot}/boot
	cp -v arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{version}
	cp -v System.map %{buildroot}/boot/System.map-%{version}
	cp -v .config %{buildroot}/boot/config-%{version}
	install -d %{buildroot}/usr/share/doc/%{NAME}-%{VERSION}
	cp -r Documentation/* %{buildroot}/usr/share/doc/%{NAME}-%{version}
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	#	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Sun Feb 25 2018 baho-utot <baho-utot@columbus.rr.com> 4.12.7-2
-	Added patches for graphics and sound
*	Tue Jan 09 2018 baho-utot <baho-utot@columbus.rr.com> 4.12.7-1
-	Initial build.	First version