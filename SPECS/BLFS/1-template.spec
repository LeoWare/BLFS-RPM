Summary:	
Name:		
Version:	
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Source0:	%{name}-%{version}
Patch0:		
%description
	The rsync package contains the rsync utility.
	This is useful for synchronizing large file archives over a network.

%prep
%setup -q -n %{NAME}-%{VERSION}
%patch0 -p1
%build
	#	CFLAGS='%_optflags ' \
	#	CXXFLAGS='%_optflags ' \
	./configure \
		--prefix=%{_prefix}
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	rm -rf %{buildroot}/%{_infodir}
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	#	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%pre
	/usr/sbin/groupadd -g 
	/usr/sbin/useradd  -c 
%post
%postun
	/usr/sbin/userdel
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Tue Jan 09 2018 baho-utot <baho-utot@columbus.rr.com> -1
-	Initial build.	First version