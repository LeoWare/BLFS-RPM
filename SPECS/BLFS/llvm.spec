#	llvm-4.0.1.src.tar.xz
Summary:	The LLVM package contains a collection of modular and reusable compiler and toolchain technologies.
Name:		llvm
Version:	4.0.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	CMake >= 3.9.1,  libffi >= 3.2.1, Python2 >= 2.7.13 	
Source0:	%{name}-%{version}.src.tar.xz
%description
	The LLVM package contains a collection of modular and reusable compiler and toolchain technologies.
	The Low Level Virtual Machine (LLVM) Core libraries provide a modern source and target-independent
	optimizer, along with code generation support for many popular CPUs (as well as some less common ones!).
	These libraries are built around a well specified code representation known as the LLVM intermediate
	representation ("LLVM IR"). 
%prep
%setup -q -n %{NAME}-%{VERSION}.src
%build
	mkdir -v build
	cd build
	CC=gcc CXX=g++ \
	cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
		-DLLVM_ENABLE_FFI=ON \
		-DCMAKE_BUILD_TYPE=Release \
		-DLLVM_BUILD_LLVM_DYLIB=ON \
		-DLLVM_TARGETS_TO_BUILD="host;AMDGPU" \
		-Wno-dev .. 
	make
%install
	cd build
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post
	pushd /usr/share/info
	rm -v dir
	for f in *
		do install-info $f dir 2>/dev/null
	done
	popd
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> llvm-4.0.1-1
-	Initial build.	First version