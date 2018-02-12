Summary:	The Xorg protocol headers provide the header files required to build the system
Name:		xorg-protocol-headers
Version:	7
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
BuildArch:	noarch
Requires:	util-macros >= 1.19.1
Source0:	bigreqsproto-1.1.2.tar.bz2
Source1:	compositeproto-0.4.2.tar.bz2
Source2:	damageproto-1.2.1.tar.bz2
Source3:	dmxproto-2.3.1.tar.bz2
Source4:	dri2proto-2.8.tar.bz2
Source5:	dri3proto-1.0.tar.bz2
Source6:	fixesproto-5.0.tar.bz2
Source7:	fontsproto-2.1.3.tar.bz2
Source8:	glproto-1.4.17.tar.bz2
Source9:	inputproto-2.3.2.tar.bz2
Source10:	kbproto-1.0.7.tar.bz2
Source11:	presentproto-1.1.tar.bz2
Source12:	randrproto-1.5.0.tar.bz2
Source13:	recordproto-1.14.2.tar.bz2
Source14:	renderproto-0.11.1.tar.bz2
Source15:	resourceproto-1.2.0.tar.bz2
Source16:	scrnsaverproto-1.2.2.tar.bz2
Source17:	videoproto-2.3.3.tar.bz2
Source18:	xcmiscproto-1.2.2.tar.bz2
Source19:	xextproto-7.3.0.tar.bz2
Source20:	xf86bigfontproto-1.2.0.tar.bz2
Source21:	xf86dgaproto-2.1.tar.bz2
Source22:	xf86driproto-2.1.1.tar.bz2
Source23:	xf86vidmodeproto-2.3.1.tar.bz2
Source24:	xineramaproto-1.2.1.tar.bz2
Source25:	xproto-7.0.31.tar.bz2
%description
	The Xorg protocol headers provide the header files required to build the system,
	and to allow other applications to build against the installed X Window system. 

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

%build
%install
	 LIST="bigreqsproto-1.1.2 compositeproto-0.4.2 damageproto-1.2.1 "
	LIST+="dmxproto-2.3.1 dri2proto-2.8 dri3proto-1.0 fixesproto-5.0 "
	LIST+="fontsproto-2.1.3 glproto-1.4.17 inputproto-2.3.2 kbproto-1.0.7 "
	LIST+="presentproto-1.1 randrproto-1.5.0 recordproto-1.14.2 "
	LIST+="renderproto-0.11.1 resourceproto-1.2.0 scrnsaverproto-1.2.2 "
	LIST+="videoproto-2.3.3 xcmiscproto-1.2.2 xextproto-7.3.0 "
	LIST+="xf86bigfontproto-1.2.0 xf86dgaproto-2.1 xf86driproto-2.1.1 "
	LIST+="xf86vidmodeproto-2.3.1 xineramaproto-1.2.1 xproto-7.0.31 "
	for i in $LIST; do
		pushd ${i}
		./configure %{XORG_CONFIG}
		make DESTDIR=%{buildroot} install
		popd
	done
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
*	Mon Feb 11 2018 baho-utot <baho-utot@columbus.rr.com> xorg-protocol-headers-7-1
-	Initial build.	First version