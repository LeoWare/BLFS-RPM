Summary:	The PCI Utils package contains a set of programs for listing PCI devices
Name:		pciutils
Version:	3.5.5
Release:	1
License:	Any
URL:		Any
Group:		BLFS/System_Utilities
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.xz
%description
	The PCI Utils package contains a set of programs for listing PCI devices,
	inspecting their status and setting their configuration registers.
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	make %{?_smp_mflags} PREFIX=/%{_prefix} SHAREDIR=/usr/share/hwdata SHARED=yes
%install
#	make DESTDIR=%{buildroot}
	make PREFIX=%{buildroot}/usr \
		SHAREDIR=%{buildroot}/usr/share/hwdata \
		SHARED=yes                 \
		install install-lib 
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Tue Jan 09 2018 baho-utot <baho-utot@columbus.rr.com> -1
-	Initial build.	First version