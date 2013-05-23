Summary:	A file transfer program to keep remote files in sync
Name:		rsync
Version:	3.0.9
Release:	1
License:	GPLv3
URL:		http://samba.anu.edu.au/rsync/
Group:		BLFS/NetworkingPrograms
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	%{name}-%{version}.tar.gz
%description
The rsync package contains the rsync utility. This is useful for 
synchronizing large file archives over a network.
%prep
%setup -q
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--with-included-popt
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
#find %{buildroot}/%{_libdir} -name '*.a'  -delete
#find %{buildroot}/%{_libdir} -name '*.la' -delete
#rm %{buildroot}/%{_infodir}
#%find_lang %{name}
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
#%{_bindir}/*
#%{_libdir}/*
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
*	Thu May 23 2013 baho-utot <baho-utot@columbus.rr.com> 3.0.9-1
-	Initial build.	First version