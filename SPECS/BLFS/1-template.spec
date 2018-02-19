#	
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
Source0:	%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.bz2
Source0:	%{name}-%{version}.tar.xz
Patch0:		
%description

%prep
	install -vdm 755  %{_builddir}/%{name}-%{version}
%setup -q -n %{NAME}-%{VERSION}
%setup -q -T -D -a 1  -n %{name}-%{version}
%patch0 -p1
%build
	./configure \
		--prefix=%{_prefix}
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%pre
	/usr/sbin/groupadd -g 
	/usr/sbin/useradd  -c 
%post
	pushd /usr/share/info
	rm -v dir
	for f in *
		do install-info $f dir 2>/dev/null
	done
	popd
%postun
	/usr/sbin/userdel
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> -1
-	Initial build.	First version