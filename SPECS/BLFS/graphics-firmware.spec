Summary:	ATI/AMD Graphics firmware	
Name:		graphics-firmware
Version:	8.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Firmware
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}.tar.gz
%description
		ATI/AMD Graphics firmware
%prep
	install -vdm 755  %{_builddir}/%{name}
	cd %{_builddir}/%{name}
	tar xf %{_sourcedir}/%{name}.tar.gz
%build
%install
	install -vdm 755 %{buildroot}/lib/firmware/radeon
	cp %{_builddir}/%{name}/HD6450/* %{buildroot}/lib/firmware/radeon
	cp %{_builddir}/%{name}/HD6770/* %{buildroot}/lib/firmware/radeon
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> -1
-	Initial build.	First version