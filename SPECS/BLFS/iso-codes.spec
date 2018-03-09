#		  https://pkg-isocodes.alioth.debian.org/downloads/iso-codes-3.75.tar.xz
Summary:	The ISO Codes package contains a list of country, language and currency names and it is used as a central database for accessing this data
Name:		iso-codes
Version:	3.75
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Requires:	Python
Source0:	%{name}-%{version}.tar.xz
%description
	The ISO Codes package contains a list of country, language and currency names and it is used as a central database for accessing this data
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix}
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}%{_datarootdir}/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}/usr/share/locale" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files  -f filelist.rpm
	%defattr(-,root,root)
#	%%{buildroot}%%{_datarootdir}/licenses/%%{name}/LICENSE
	%{_datarootdir}/pkgconfig/iso-codes.pc
	%{_datarootdir}/iso-codes
	%{_datarootdir}/xml/iso-codes
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 3.75-1
-	Initial build.	First version