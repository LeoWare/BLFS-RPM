#	libva-1.8.3.tar.bz2
Summary:	The libva package contains a library which provides access to hardware accelerated video processing
Name:		libva
Version:	1.8.3
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Requires:	mesa >= 17.1.6,  wayland >= 1.14.0
Source0:	%{name}-%{version}.tar.bz2
%description
	The libva package contains a library which provides access to hardware accelerated video processing,
	using hardware to accelerate video processing in order to offload the central processing unit (CPU)
	to decode and encode compressed digital video. The VA API video decode/encode interface is platform
	and window system independent targeted at Direct Rendering Infrastructure (DRI) in the X Window System
	however it can potentially also be used with direct framebuffer and graphics sub-systems for video output.
	Accelerated processing includes support for video decoding, video encoding, subpicture blending, and rendering. 
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
*	Fri Feb 16 2018 baho-utot <baho-utot@columbus.rr.com> libva-1.8.3-1
-	Initial build.	First version