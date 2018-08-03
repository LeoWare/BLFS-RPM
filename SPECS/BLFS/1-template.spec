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
Requires:	
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Source0:	%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.bz2
Source0:	%{name}-%{version}.tar.xz
Patch0:		
%description
	
%prep
%setup -q -n %{NAME}-%{VERSION}
%setup -q -T -D -a 1  -n %{name}-%{version}
%patch0 -p1
%build
	./configure \
		--prefix=%{_prefix}\
		--disable-static
#		--docdir=%{_datarootdir}/doc/%{NAME}-%{VERSION}
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}%{_datarootdir}/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%pre
	/usr/bin/getent group  myservice || /usr/sbin/groupadd -g 
	/usr/bin/getent passwd myservice || /usr/sbin/useradd  -c
%post
	pushd /usr/share/info
	rm -v dir
	for f in *
		do install-info $f dir 2>/dev/null
	done
	popd
%postun
	/usr/sbin/userdel
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
	%defattr(-,root,root)
#	%%{buildroot}%%{_datarootdir}/licenses/%%{name}/LICENSE
%changelog
*	Fri Mar 09 2018 baho-utot <baho-utot@columbus.rr.com> -1
-	Initial build.	First version