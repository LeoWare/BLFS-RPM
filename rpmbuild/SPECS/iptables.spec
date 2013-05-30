Summary:	'Linux kernel packet control tool
Name:		iptables
Version:	1.4.18
Release:	1
License:	GPLv2
URL:		http://www.netfilter.org/projects/iptables
Group:		BLFS/ Security
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	http://www.netfilter.org/projects/iptables/files/%{name}-%{version}.tar.bz2
Source1:	http://www.linuxfromscratch.org/blfs/downloads/svn/blfs-bootscripts-20130512.tar.bz2
%description
The next part of this chapter deals with firewalls. The principal 
firewall tool for Linux is Iptables. You will need to install 
Iptables if you intend on using any form of a firewall.
%prep
%setup -q
tar xf %{SOURCE1}
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--exec-prefix= \
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
ln -sfv ../../sbin/xtables-multi %{buildroot}%{_libdir}/iptables-xml
#	Install daemon script
pushd blfs-bootscripts-20130512
make DESTDIR=%{buildroot} install-iptables
popd
find %{buildroot}/%{_libdir} -name '*.a'  -delete
find %{buildroot}/%{_libdir} -name '*.la' -delete
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/sbin/*
%{_bindir}/*
%{_libdir}/*.so*
%{_libdir}/iptables-xml
%{_libdir}/iptables/*
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man8/*
%changelog
*	Thu May 23 2013 baho-utot <baho-utot@columbus.rr.com> 1.4.18-1
-	Initial build.	First version
