Summary:	
Name:		
Version:	
Release:	1
License:
URL:		
Group:		
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	%{name}-%{version}.tar.gz
Patch0:		
%description

%prep
%setup -q
%patch0 -p0
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--htmldir=%{_docdir}/%{name}-%{version} \
	--docdir=%{_docdir}/%{name}-%{version}

./configure CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--exec-prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
	--sysconfdir=/etc \
	--datadir=/%{_datarootdir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--localstatedir=%{_localstatedir}
	--sharedstatedir=%{_sharedstatedir} \
	--mandir=%{_mandir} \
	--infodir=/%{_infodir}
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
#make PREFIX=%{buildroot}/usr install
#find %{buildroot}/%{_libdir} -name '*.a'  -delete
#find %{buildroot}/%{_libdir} -name '*.la' -delete
#rm %{buildroot}/%{_infodir}
#%find_lang %{name}
#install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
#%files -f %{name}.lang
%files
%defattr(-,root,root)
#%config(noreplace) /etc/*
#%{_bindir}/*
#%{_libdir}/*.so*
#%{_libdir}/pkgconfig/*
#%{_includedir}/*
#%{_datarootdir}/
#%{_docdir}/%{name}-%{version}/*
#%{_infodir}/*
#%{_mandir}/man1/*
#%{_mandir}/man2/*
#%{_mandir}/man3/*
#%{_mandir}/man4/*
#%{_mandir}/man5/*
#%{_mandir}/man6/*
#%{_mandir}/man7/*
#%{_mandir}/man8/*
%changelog
*	Wed May 22 2013 baho-utot <baho-utot@columbus.rr.com> -1
-	Initial build.	First version