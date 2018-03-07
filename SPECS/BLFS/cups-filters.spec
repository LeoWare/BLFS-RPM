#		https://www.openprinting.org/download/cups-filters/cups-filters-1.17.2.tar.xz
Summary:	The CUPS Filters package contains backends, filters and other software
Name:		cups-filters
Version:	1.17.2
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
#	Requires:	 Cups-2.2.4, GLib-2.52.3, ghostscript-9.21, IJS-0.35, Little CMS-2.8, mupdf-1.11 (mutool), Poppler-0.57.0, and Qpdf-6.0.0 
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Source0:	%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.bz2
Source0:	%{name}-%{version}.tar.xz
Patch0:		
%description
	The CUPS Filters package contains backends, filters and other software that was once 
	part of the core CUPS distribution but is no longer maintained by Apple Inc
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

%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 1.17.2-1
-	Initial build.	First version