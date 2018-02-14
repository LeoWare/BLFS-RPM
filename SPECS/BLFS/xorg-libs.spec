Summary:	The Xorg libraries meta package
Name:		xorg-libs
Version:	7
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	Fontconfig >= 2.12.4, libxcb >= 1.12
Requires:	xtrans >= 1.3.5
Requires:	libX11 >= 1.6.5
Requires:	libXext >= 1.3.3
Requires:	libFS >= 1.0.7
Requires:	libICE >= 1.0.9
Requires:	libSM >= 1.2.2
Requires:	libXScrnSaver >= 1.2.2
Requires:	libXt >= 1.1.5
Requires:	libXmu >= 1.1.2
Requires:	libXpm >= 3.5.12
Requires:	libXaw >= 1.0.13
Requires:	libXfixes >= 5.0.3
Requires:	libXcomposite >= 0.4.4
Requires:	libXrender >= 0.9.10
Requires:	libXcursor >= 1.1.14
Requires:	libXdamage >= 1.1.4
Requires:	libfontenc >= 1.1.3
Requires:	libXfont2 >= 2.0.1
Requires:	libXft >= 2.3.2
Requires:	libXi >= 1.7.9
Requires:	libXinerama >= 1.1.3
Requires:	libXrandr >= 1.5.1
Requires:	libXres >= 1.0.7
Requires:	libXtst >= 1.2.3
Requires:	libXv >= 1.0.11
Requires:	libXvMC >= 1.0.10
Requires:	libXxf86dga >= 1.1.4
Requires:	libXxf86vm >= 1.1.4
Requires:	libdmx >= 1.1.3
Requires:	libpciaccess >= 0.13.5
Requires:	libxkbfile >= 1.0.9
Requires:	libxshmfence >= 1.2
%description
	The Xorg libraries provide library routines that are used within all X Window applications.
%prep
%build
%install
%files
	%defattr(-,root,root)
%changelog
*	Tue Feb 13 2018 baho-utot <baho-utot@columbus.rr.com> -1
-	Initial build.	First version