Summary:	The rsync package contains the rsync utility.
Name:		rsync
Version:	3.1.2
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Networking_Programs
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	popt >= 1.16
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Source0:	%{name}-%{version}.tar.gz
%description
	The rsync package contains the rsync utility.
	This is useful for synchronizing large file archives over a network.

%prep
%setup -q -n %{NAME}-%{VERSION}
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
	/usr/sbin/groupadd -g 48 rsyncd
	/usr/sbin/useradd  -c "rsyncd Daemon" -d /home/rsync -g rsyncd -s /bin/false -u 48 rsyncd
%postun
	/usr/sbin/userdel rsyncd
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Mon Feb 11 2018 baho-utot <baho-utot@columbus.rr.com> rsync-3.1.2-1
-	Initial build.	First version