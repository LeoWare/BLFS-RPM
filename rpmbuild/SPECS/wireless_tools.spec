Summary:	Set of tools allowing manipulation of the Wireless Extensions
Name:		wireless_tools
Version:	29
Release:	1
License:	GPLv1
URL:		http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux
Group:		BLFS/Networking
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/%{name}.%{version}.tar.gz

%description
The Wireless Extension (WE) is a generic API in the Linux kernel
allowing a driver to expose configuration and statistics specific
to common Wireless LANs to user space. A single set of tools can
support all the variations of Wireless LANs, regardless of their
type as long as the driver supports Wireless Extensions. WE 
parameters may also be changed on the fly without restarting the
driver or Linux.
%prep
%setup -q -n %{name}.%{version}
%build
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make \
	INSTALL_DIR="%{buildroot}/usr/bin" \
	INSTALL_LIB="%{buildroot}/usr/lib" \
	INSTALL_INC="%{buildroot}/usr/include" \
	INSTALL_MAN="%{buildroot}/usr/share/man" \
	install
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p/sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_includedir}/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%changelog
*	Wed May 22 2013 baho-utot <baho-utot@columbus.rr.com> 29-1
-	Initial build.	First version