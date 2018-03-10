Summary:	The Xorg applications provide the expected applications available in previous X Window implementations.
Name:		xorg-apps
Version:	7
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Requires:	xorg-protocol-headers
Requires:	libpng >= 1.6.31, mesa >= 17.1.6, xbitmaps >= 1.1.1, xcb-util >= 0.4.0 

Source0:	iceauth-1.0.7.tar.bz2
Source1:	luit-1.1.1.tar.bz2
Source2:	mkfontdir-1.0.7.tar.bz2
Source3:	mkfontscale-1.1.2.tar.bz2
Source4:	sessreg-1.1.1.tar.bz2
Source5:	setxkbmap-1.3.1.tar.bz2
Source6:	smproxy-1.0.6.tar.bz2
Source7:	x11perf-1.6.0.tar.bz2
Source8:	xauth-1.0.10.tar.bz2
Source9:	xbacklight-1.2.1.tar.bz2
Source10:	xcmsdb-1.0.5.tar.bz2
Source11:	xcursorgen-1.0.6.tar.bz2
Source12:	xdpyinfo-1.3.2.tar.bz2
Source13:	xdriinfo-1.0.5.tar.bz2
Source14:	xev-1.2.2.tar.bz2
Source15:	xgamma-1.0.6.tar.bz2
Source16:	xhost-1.0.7.tar.bz2
Source17:	xinput-1.6.2.tar.bz2
Source18:	xkbcomp-1.4.0.tar.bz2
Source19:	xkbevd-1.1.4.tar.bz2
Source20:	xkbutils-1.0.4.tar.bz2
Source21:	xkill-1.0.4.tar.bz2
Source22:	xlsatoms-1.1.2.tar.bz2
Source23:	xlsclients-1.1.3.tar.bz2
Source24:	xmessage-1.0.4.tar.bz2
Source25:	xmodmap-1.0.9.tar.bz2
Source26:	xpr-1.0.4.tar.bz2
Source27:	xprop-1.2.2.tar.bz2
Source28:	xrandr-1.5.0.tar.bz2
Source29:	xrdb-1.1.0.tar.bz2
Source30:	xrefresh-1.0.5.tar.bz2
Source31:	xset-1.2.3.tar.bz2
Source32:	xsetroot-1.1.1.tar.bz2
Source33:	xvinfo-1.1.3.tar.bz2
Source34:	xwd-1.0.6.tar.bz2
Source35:	xwininfo-1.1.3.tar.bz2
Source36:	xwud-1.0.4.tar.bz2
%description
	The Xorg applications provide the expected applications available in previous X Window implementations.

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
%setup -q -T -D -a 32 -n %{name}-%{version}
%setup -q -T -D -a 33 -n %{name}-%{version}
%setup -q -T -D -a 34 -n %{name}-%{version}
%setup -q -T -D -a 35 -n %{name}-%{version}
%setup -q -T -D -a 36 -n %{name}-%{version}

%build
LIST=""
LIST+="iceauth-1.0.7 luit-1.1.1 mkfontdir-1.0.7 mkfontscale-1.1.2 sessreg-1.1.1 setxkbmap-1.3.1 "
LIST+="smproxy-1.0.6 x11perf-1.6.0 xauth-1.0.10 xbacklight-1.2.1 xcmsdb-1.0.5 xcursorgen-1.0.6 "
LIST+="xdpyinfo-1.3.2 xdriinfo-1.0.5 xev-1.2.2 xgamma-1.0.6 xhost-1.0.7 xinput-1.6.2 xkbcomp-1.4.0 "
LIST+="xkbevd-1.1.4 xkbutils-1.0.4 xkill-1.0.4 xlsatoms-1.1.2 xlsclients-1.1.3 xmessage-1.0.4 "
LIST+="xmodmap-1.0.9 xpr-1.0.4 xprop-1.2.2 xrandr-1.5.0 xrdb-1.1.0 xrefresh-1.0.5 xset-1.2.3 "
LIST+="xsetroot-1.1.1 xvinfo-1.1.3 xwd-1.0.6 xwininfo-1.1.3 xwud-1.0.4"
for i in ${LIST}; do
	cd ${i}
	echo ${i}
	if [ "luit-1.1.1" == "${i}" ]; then
		sed -i -e "/D_XOPEN/s/5/6/" configure
	fi
	./configure %{XORG_CONFIG}
	make %{?_smp_mflags}
	echo ""
	cd -
done

%install
LIST=""
LIST+="iceauth-1.0.7 luit-1.1.1 mkfontdir-1.0.7 mkfontscale-1.1.2 sessreg-1.1.1 setxkbmap-1.3.1 "
LIST+="smproxy-1.0.6 x11perf-1.6.0 xauth-1.0.10 xbacklight-1.2.1 xcmsdb-1.0.5 xcursorgen-1.0.6 "
LIST+="xdpyinfo-1.3.2 xdriinfo-1.0.5 xev-1.2.2 xgamma-1.0.6 xhost-1.0.7 xinput-1.6.2 xkbcomp-1.4.0 "
LIST+="xkbevd-1.1.4 xkbutils-1.0.4 xkill-1.0.4 xlsatoms-1.1.2 xlsclients-1.1.3 xmessage-1.0.4 "
LIST+="xmodmap-1.0.9 xpr-1.0.4 xprop-1.2.2 xrandr-1.5.0 xrdb-1.1.0 xrefresh-1.0.5 xset-1.2.3 "
LIST+="xsetroot-1.1.1 xvinfo-1.1.3 xwd-1.0.6 xwininfo-1.1.3 xwud-1.0.4"
for i in ${LIST}; do
	cd ${i}
	echo ${i}
	make DESTDIR=%{buildroot} install
	echo ""
	cd -
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
for f in *;do install-info $f dir; 2>/dev/null done
popd

%files -f filelist.rpm
	%defattr(-,root,root)

%changelog
*	Thu Feb 15 2018 baho-utot <baho-utot@columbus.rr.com> xorg-apps-7-1
-	Initial build.	First version