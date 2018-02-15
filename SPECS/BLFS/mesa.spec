#	mesa-17.1.6.tar.xz
Summary:	Mesa is an OpenGL compatible 3D graphics library.
Name:		mesa
Version:	17.1.6
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	xorg-protocol-headers, Xorg Libraries
Requires:	libdrm >= 2.4.82, Mako >= 1.0.4, Python2 >= 2.7.13 
Requires:	libvdpau >= 1.1.1, llvm >= 4.0.1, libgcrypt >= 1.8.0, nettle >= 3.3, wayland >= 1.14.0
Source0:	%{name}-%{version}.tar.bz2
Patch0:		mesa-17.1.6-add_xdemos-1.patch
%description
	Mesa is an OpenGL compatible 3D graphics library.
%define		XORG_CONFIG	--prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --disable-static
%define		GLL_DRV		r300,r600,radeonsi,svga,swrast
%prep
%setup -q -n %{NAME}-%{VERSION}
patch0% -p1
sed -i "/pthread_stubs_possible=/s/yes/no/" configure.ac
%build
	./autogen.sh CFLAGS='-O2' CXXFLAGS='-O2' \
		--prefix=%{XORG_PREFIX} \
		--sysconfdir=/etc \
		--enable-texture-float \
		--enable-osmesa \
		--enable-xa \
		--enable-glx-tls \
		--with-platforms="drm,x11" \
		--with-gallium-drivers=$GLL_DRV
		#		Archlinux
		#		--with-gallium-drivers=r300,r600,radeonsi,nouveau,svga,swrast,virgl,swr \
		#		--with-dri-drivers=i915,i965,r200,radeon,nouveau,swrast \
		#		--with-platforms=x11,drm,wayland \
		#		--with-vulkan-drivers=intel,radeon \
		#		--enable-gles1 \
		#		--enable-gles2 \
		#		--enable-dri
	make %{?_smp_mflags}
	make %{?_smp_mflags} -C xdemos DEMOS_PREFIX=%{XORG_PREFIX}
%install
	make DESTDIR=%{buildroot} install
	make DESTDIR=%{buildroot} -C xdemos DEMOS_PREFIX=%{XORG_PREFIX} install
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
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> mesa-17.1.6-1
-	Initial build.	First version