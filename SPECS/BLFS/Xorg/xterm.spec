#	xterm-330.tgz
Summary:	xterm is a terminal emulator for the X Window System. 
Name:		xterm
Version:	330
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	xorg-apps
Source0:	%{name}-%{version}.tgz
%description
	 xterm is a terminal emulator for the X Window System.
	This package is not a part of the Xorg katamari and is provided only
	as a dependency to other packages or for testing the completed
	Xorg installation. 
%define		XORG_CONFIG	--prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --disable-static
%prep
%setup -q -n %{NAME}-%{VERSION}
sed -i '/v0/{n;s/new:/new:kb=^?:/}' termcap
printf '\tkbs=\\177,\n' >> terminfo
%build
	TERMINFO=/usr/share/terminfo \
	./configure %{XORG_CONFIG} \
		--with-app-defaults=/etc/X11/app-defaults
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	# make DESTDIR=%{buildroot} install-ti
	install -vdm 755 %{buildroot}/etc
	cat >> %{buildroot}/etc/X11/app-defaults/XTerm <<- "EOF"
		*VT100*locale: true
		*VT100*faceName: Monospace
		*VT100*faceSize: 10
		*backarrowKeyIsErase: true
		*ptyInitialErase: true
	EOF
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
*	Fri Feb 16 2018 baho-utot <baho-utot@columbus.rr.com> xterm-330-1
-	Initial build.	First version