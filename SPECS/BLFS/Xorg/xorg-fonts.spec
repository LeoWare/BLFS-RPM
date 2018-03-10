Summary:	The Xorg font packages provide some scalable fonts and supporting packages for Xorg applications.
Name:		xorg-fonts
Version:	7
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1

Source0:	font-util-1.3.1.tar.bz2
Source1:	encodings-1.0.4.tar.bz2
Source2:	font-alias-1.0.3.tar.bz2
Source3:	font-adobe-utopia-type1-1.0.4.tar.bz2
Source4:	font-bh-ttf-1.0.3.tar.bz2
Source5:	font-bh-type1-1.0.3.tar.bz2
Source6:	font-ibm-type1-1.0.3.tar.bz2
Source7:	font-misc-ethiopic-1.0.3.tar.bz2
Source8:	font-xfree86-type1-1.0.4.tar.bz2

%description
	The Xorg font packages provide some scalable fonts and supporting packages for Xorg applications.

%define		XORG_CONFIG	--prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --disable-static
%define		XORG_PREFIX	%{_prefix}
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

%build
	LIST=""
	LIST+="font-util-1.3.1 encodings-1.0.4 font-alias-1.0.3 font-adobe-utopia-type1-1.0.4 "
	LIST+="font-bh-ttf-1.0.3 font-bh-type1-1.0.3 font-ibm-type1-1.0.3 font-misc-ethiopic-1.0.3 "
	LIST+="font-xfree86-type1-1.0.4"
	for i in ${LIST}; do
		cd ${i}
		echo ${i}
		./configure %{XORG_CONFIG}
		make %{?_smp_mflags}
		echo ""
		cd -
	done
%install
	LIST+="font-util-1.3.1 encodings-1.0.4 font-alias-1.0.3 font-adobe-utopia-type1-1.0.4 "
	LIST+="font-bh-ttf-1.0.3 font-bh-type1-1.0.3 font-ibm-type1-1.0.3 font-misc-ethiopic-1.0.3 "
	LIST+="font-xfree86-type1-1.0.4"
	for i in ${LIST}; do
		cd ${i}
		echo ${i}
		make DESTDIR=%{buildroot} install
		echo ""
		cd -
	done
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	install -v -d -m755 %{buildroot}/usr/share/fonts
	ln -svfn %{XORG_PREFIX}/share/fonts/X11/OTF %{buildroot}/usr/share/fonts/X11-OTF
	ln -svfn %{XORG_PREFIX}/share/fonts/X11/TTF %{buildroot}/usr/share/fonts/X11-TTF
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Thu Feb 15 2018 baho-utot <baho-utot@columbus.rr.com> xorg-fonts-7-1
-	Initial build.	First version