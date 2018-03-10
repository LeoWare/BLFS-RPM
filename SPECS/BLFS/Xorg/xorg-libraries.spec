Summary:	The Xorg libraries provide library routines that are used within all X Window applications. 
Name:		xorg-libraries
Version:	7
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	xorg-protocol-headers
Source0:	xtrans-1.3.5.tar.bz2
Source1:	libX11-1.6.5.tar.bz2
Source2:	libXext-1.3.3.tar.bz2
Source3:	libFS-1.0.7.tar.bz2
Source4:	libICE-1.0.9.tar.bz2
Source5:	libSM-1.2.2.tar.bz2
Source6:	libXScrnSaver-1.2.2.tar.bz2
Source7:	libXt-1.1.5.tar.bz2
Source8:	libXmu-1.1.2.tar.bz2
Source9:	libXpm-3.5.12.tar.bz2
Source10:	libXaw-1.0.13.tar.bz2
Source11:	libXfixes-5.0.3.tar.bz2
Source12:	libXcomposite-0.4.4.tar.bz2
Source13:	libXrender-0.9.10.tar.bz2
Source14:	libXcursor-1.1.14.tar.bz2
Source15:	libXdamage-1.1.4.tar.bz2
Source16:	libfontenc-1.1.3.tar.bz2
Source17:	libXfont2-2.0.1.tar.bz2
Source18:	libXft-2.3.2.tar.bz2
Source19:	libXi-1.7.9.tar.bz2
Source20:	libXinerama-1.1.3.tar.bz2
Source21:	libXrandr-1.5.1.tar.bz2
Source22:	libXres-1.0.7.tar.bz2
Source23:	libXtst-1.2.3.tar.bz2
Source24:	libXv-1.0.11.tar.bz2
Source25:	libXvMC-1.0.10.tar.bz2
Source26:	libXxf86dga-1.1.4.tar.bz2
Source27:	libXxf86vm-1.1.4.tar.bz2
Source28:	libdmx-1.1.3.tar.bz2
Source29:	libpciaccess-0.13.5.tar.bz2
Source30:	libxkbfile-1.0.9.tar.bz2
Source31:	libxshmfence-1.2.tar.bz2

%description
	The Xorg libraries provide library routines that are used within all X Window applications. 

%define		XORG_CONFIG	--prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --disable-static
%prep
install -vdm 755  %{_builddir}/%{name}-%{version}
%setup -q -T -D -a 0  -n %{name}-%{version}
%setup -q -T -D -a 1  -n %{name}-%{version}
%setup -q -T -D -a 2  -n %{name}-%{version}
%setup -q -T -D -a 3  -n %{name}-%{version}
%setup -q -T -D -a 4  -n %{name}-%{version}
%setup -q -T -D -a 5  -n %{name}-%{version}
%setup -q -T -D -a 6  -n %{name}-%{version}
%setup -q -T -D -a 7  -n %{name}-%{version}
%setup -q -T -D -a 8  -n %{name}-%{version}
%setup -q -T -D -a 9  -n %{name}-%{version}
%setup -q -T -D -a 10 -n %{name}-%{version}
%setup -q -T -D -a 11 -n %{name}-%{version}
%setup -q -T -D -a 12 -n %{name}-%{version}
%setup -q -T -D -a 13 -n %{name}-%{version}
%setup -q -T -D -a 14 -n %{name}-%{version}
%setup -q -T -D -a 15 -n %{name}-%{version}
%setup -q -T -D -a 16 -n %{name}-%{version}
%setup -q -T -D -a 17 -n %{name}-%{version}
%setup -q -T -D -a 18 -n %{name}-%{version}
%setup -q -T -D -a 19 -n %{name}-%{version}
%setup -q -T -D -a 20 -n %{name}-%{version}
%setup -q -T -D -a 21 -n %{name}-%{version}
%setup -q -T -D -a 22 -n %{name}-%{version}
%setup -q -T -D -a 23 -n %{name}-%{version}
%setup -q -T -D -a 24 -n %{name}-%{version}
%setup -q -T -D -a 25 -n %{name}-%{version}
%setup -q -T -D -a 26 -n %{name}-%{version}
%setup -q -T -D -a 27 -n %{name}-%{version}
%setup -q -T -D -a 28 -n %{name}-%{version}
%setup -q -T -D -a 29 -n %{name}-%{version}
%setup -q -T -D -a 30 -n %{name}-%{version}
%setup -q -T -D -a 31 -n %{name}-%{version}
%build
%install
	cd xtrans-1.3.5
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libX11-1.6.5
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd-
	cd libXext-1.3.3
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libFS-1.0.7
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libICE-1.0.9
		./configure $XORG_CONFIG  ICE_LIBS=-lpthread
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd-
	cd libSM-1.2.2
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd-
	cd libXScrnSaver-1.2.2
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd-
	cd libXt-1.1.5
		./configure $XORG_CONFIG--with-appdefaultdir=/etc/X11/app-defaults
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXmu-1.1.2
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXpm-3.5.12
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXaw-1.0.13
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXfixes-5.0.3
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXcomposite-0.4.4
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXrender-0.9.10
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXcursor-1.1.14
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXdamage-1.1.4
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd-
	cd libfontenc-1.1.3
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXfont2-2.0.1
		./configure $XORG_CONFIG --disable-devel-docs
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXft-2.3.2
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXi-1.7.9
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXinerama-1.1.3
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXrandr-1.5.1
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXres-1.0.7
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXtst-1.2.3
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXv-1.0.11
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXvMC-1.0.10
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXxf86dga-1.1.4
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libXxf86vm-1.1.4
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd-
	cd libdmx-1.1.3
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libpciaccess-0.13.5
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libxkbfile-1.0.9
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
	cd libxshmfence-1.2
		./configure $XORG_CONFIG
		make -j2
		make DESTDIR=%{_buildroot}/%{name}-%{version} install
	cd -
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
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Mon Feb 11 2018 baho-utot <baho-utot@columbus.rr.com> xorg-libraries-7-1
-	Initial build.	First version