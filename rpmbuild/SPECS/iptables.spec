Summary:	'Linux kernel packet control tool
Name:		iptables
Version:	1.4.18
Release:	1
License:	GPLv2
URL:		http://www.netfilter.org/projects/iptables
Group:		BLFS/ Security
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	%{name}-%{version}.tar.bz2
%description
The next part of this chapter deals with firewalls. The principal 
firewall tool for Linux is Iptables. You will need to install 
Iptables if you intend on using any form of a firewall.
%prep
%setup -q
%patch0 -p0
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--with-xtlibdir=%{_libdir}/iptables \
	--with-pkgconfigdir=/usr/lib/pkgconfig \
	--enable-libipq \
	--enable-devel
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
#ln -sfv ../../sbin/xtables-multi %{buildroot}%{_libdir}/iptables-xml
#for file in libip4tc libip6tc libipq libiptc libxtables
#do
#  ln -sfv ../../lib/`readlink /lib/${file}.so` %{buildroot}%{_libdir}/${file}.so
#  rm -v %{buildroot}/lib/${file}.so
#done
#make PREFIX=%{buildroot}/usr install
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
*	Thu May 23 2013 baho-utot <baho-utot@columbus.rr.com> 1.4.18-1
-	Initial build.	First version