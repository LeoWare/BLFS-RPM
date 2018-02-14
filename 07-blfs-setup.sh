#!/bin/bash
#################################################
#	Title:	07-blfs-setup.sh		#
#        Date:	2018-02-09			#
#     Version:	1.1				#
#      Author:	baho-utot@columbus.rr.com	#
#     Options:					#
#################################################
#
set -o errexit					# exit if error...insurance ;)
set -o nounset					# exit if variable not initalized
set +h						# disable hashall
PRGNAME=${0##*/}				# script name minus the path
TOPDIR=${PWD}
PARENT=/usr/src/Octothorpe
LOGFILE=$(date +%Y-%m-%d).log
#LOGFILE=/dev/null				# uncomment to disable log file
#
#	Common support functions
#
die() {
	local _red="\\033[1;31m"
	local _normal="\\033[0;39m"
	[ -n "$*" ] && printf "${_red}$*${_normal}\n"
	false
	exit 1
}
msg() {
	printf "%s\n" "${1}"
	return
}
msg_line() {
	printf "%s" "${1}"
	return
}
msg_failure() {
	local _red="\\033[1;31m"
	local _normal="\\033[0;39m"
	printf "${_red}%s${_normal}\n" "FAILURE"
	exit 2
}
msg_success() {
	local _green="\\033[1;32m"
	local _normal="\\033[0;39m"
	printf "${_green}%s${_normal}\n" "SUCCESS"
	return
}
msg_log() {
	printf "\n%s\n\n" "${1}" >> ${_logfile} 2>&1
	return
}
end-run() {
	local _green="\\033[1;32m"
	local _normal="\\033[0;39m"
	printf "${_green}%s${_normal}\n" "Run Complete"
	return
}
#
#	Functions
#
_wget_list() {
	msg_line "	Creating wget-list: "
		cat > ${PARENT}/SOURCES/wget-blfs <<- EOF
			http://anduin.linuxfromscratch.org/BLFS/blfs-bootscripts/blfs-bootscripts-20170731.tar.xz
			https://www.kernel.org/pub/software/utils/pciutils/pciutils-3.5.5.tar.xz
			https://www.samba.org/ftp/rsync/src/rsync-3.1.2.tar.gz
			https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tar.xz
			http://ftp.osuosl.org/pub/blfs/8.1/p/python-3.6.2-docs-html.tar.bz2
		EOF
		#	dependencies
		cat >> ${PARENT}/SOURCES/wget-blfs <<- EOF
			https://sourceware.org/ftp/libffi/libffi-3.2.1.tar.gz
			https://dri.freedesktop.org/libdrm/libdrm-2.4.82.tar.bz2
			https://ftp.gnu.org/gnu/nettle/nettle-3.3.tar.gz
			https://sourceware.org/ftp/elfutils/0.170/elfutils-0.170.tar.bz2
			http://xmlsoft.org/sources/libxml2-2.9.4.tar.gz
			https://wayland.freedesktop.org/releases/wayland-1.14.0.tar.xz
			https://www.gnupg.org/ftp/gcrypt/libgpg-error/libgpg-error-1.27.tar.bz2
			https://www.gnupg.org/ftp/gcrypt/libgcrypt/libgcrypt-1.8.0.tar.bz2
			https://people.freedesktop.org/~aplattner/vdpau/libvdpau-1.1.1.tar.bz2
			https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tar.xz
			https://files.pythonhosted.org/packages/source/f/funcsigs/funcsigs-1.0.2.tar.gz
			https://files.pythonhosted.org/packages/source/B/Beaker/Beaker-1.9.0.tar.gz
			https://files.pythonhosted.org/packages/source/M/MarkupSafe/MarkupSafe-1.0.tar.gz
			https://files.pythonhosted.org/packages/source/M/Mako/Mako-1.0.4.tar.gz
			http://anduin.linuxfromscratch.org/BLFS/other/make-ca.sh-20170514
			http://anduin.linuxfromscratch.org/BLFS/other/certdata.txt
			http://www.cacert.org/certs/root.crt
			https://curl.haxx.se/download/curl-7.55.1.tar.xz
			http://www.libarchive.org/downloads/libarchive-3.3.2.tar.gz
			https://cmake.org/files/v3.9/cmake-3.9.1.tar.gz
		EOF
		#	Xorg
		cat >> ${PARENT}/SOURCES/wget-blfs <<- EOF
			https://www.x.org/pub/individual/util/util-macros-1.19.1.tar.bz2
			https://www.x.org/pub/individual/proto/bigreqsproto-1.1.2.tar.bz2
			https://www.x.org/pub/individual/proto/compositeproto-0.4.2.tar.bz2
			https://www.x.org/pub/individual/proto/damageproto-1.2.1.tar.bz2
			https://www.x.org/pub/individual/proto/dmxproto-2.3.1.tar.bz2
			https://www.x.org/pub/individual/proto/dri2proto-2.8.tar.bz2
			https://www.x.org/pub/individual/proto/dri3proto-1.0.tar.bz2
			https://www.x.org/pub/individual/proto/fixesproto-5.0.tar.bz2
			https://www.x.org/pub/individual/proto/fontsproto-2.1.3.tar.bz2
			https://www.x.org/pub/individual/proto/glproto-1.4.17.tar.bz2
			https://www.x.org/pub/individual/proto/inputproto-2.3.2.tar.bz2
			https://www.x.org/pub/individual/proto/kbproto-1.0.7.tar.bz2
			https://www.x.org/pub/individual/proto/presentproto-1.1.tar.bz2
			https://www.x.org/pub/individual/proto/randrproto-1.5.0.tar.bz2
			https://www.x.org/pub/individual/proto/recordproto-1.14.2.tar.bz2
			https://www.x.org/pub/individual/proto/renderproto-0.11.1.tar.bz2
			https://www.x.org/pub/individual/proto/resourceproto-1.2.0.tar.bz2
			https://www.x.org/pub/individual/proto/scrnsaverproto-1.2.2.tar.bz2
			https://www.x.org/pub/individual/proto/videoproto-2.3.3.tar.bz2
			https://www.x.org/pub/individual/proto/xcmiscproto-1.2.2.tar.bz2
			https://www.x.org/pub/individual/proto/xextproto-7.3.0.tar.bz2
			https://www.x.org/pub/individual/proto/xf86bigfontproto-1.2.0.tar.bz2
			https://www.x.org/pub/individual/proto/xf86dgaproto-2.1.tar.bz2
			https://www.x.org/pub/individual/proto/xf86driproto-2.1.1.tar.bz2
			https://www.x.org/pub/individual/proto/xf86vidmodeproto-2.3.1.tar.bz2
			https://www.x.org/pub/individual/proto/xineramaproto-1.2.1.tar.bz2
			https://www.x.org/pub/individual/proto/xproto-7.0.31.tar.bz2
			https://www.x.org/pub/individual/lib/libXau-1.0.8.tar.bz2
			https://www.x.org/pub/individual/lib/libXdmcp-1.1.2.tar.bz2
			https://xcb.freedesktop.org/dist/xcb-proto-1.12.tar.bz2
			http://www.linuxfromscratch.org/patches/blfs/8.1/xcb-proto-1.12-python3-1.patch
			http://www.linuxfromscratch.org/patches/blfs/8.1/xcb-proto-1.12-schema-1.patch
			https://xcb.freedesktop.org/dist/libxcb-1.12.tar.bz2
			http://www.linuxfromscratch.org/patches/blfs/8.1/libxcb-1.12-python3-1.patch
			https://www.x.org/pub/individual/lib/xtrans-1.3.5.tar.bz2
			https://www.x.org/pub/individual/lib/libX11-1.6.5.tar.bz2
			https://www.x.org/pub/individual/lib/libXext-1.3.3.tar.bz2
			https://www.x.org/pub/individual/lib/libFS-1.0.7.tar.bz2
			https://www.x.org/pub/individual/lib/libICE-1.0.9.tar.bz2
			https://www.x.org/pub/individual/lib/libSM-1.2.2.tar.bz2
			https://www.x.org/pub/individual/lib/libXScrnSaver-1.2.2.tar.bz2
			https://www.x.org/pub/individual/lib/libXt-1.1.5.tar.bz2
			https://www.x.org/pub/individual/lib/libXmu-1.1.2.tar.bz2
			https://www.x.org/pub/individual/lib/libXpm-3.5.12.tar.bz2
			https://www.x.org/pub/individual/lib/libXaw-1.0.13.tar.bz2
			https://www.x.org/pub/individual/lib/libXfixes-5.0.3.tar.bz2
			https://www.x.org/pub/individual/lib/libXcomposite-0.4.4.tar.bz2
			https://www.x.org/pub/individual/lib/libXrender-0.9.10.tar.bz2
			https://www.x.org/pub/individual/lib/libXcursor-1.1.14.tar.bz2
			https://www.x.org/pub/individual/lib/libXdamage-1.1.4.tar.bz2
			https://www.x.org/pub/individual/lib/libfontenc-1.1.3.tar.bz2
			https://www.x.org/pub/individual/lib/libXfont2-2.0.1.tar.bz2
			https://www.x.org/pub/individual/lib/libXft-2.3.2.tar.bz2
			https://www.x.org/pub/individual/lib/libXi-1.7.9.tar.bz2
			https://www.x.org/pub/individual/lib/libXinerama-1.1.3.tar.bz2
			https://www.x.org/pub/individual/lib/libXrandr-1.5.1.tar.bz2
			https://www.x.org/pub/individual/lib/libXres-1.0.7.tar.bz2
			https://www.x.org/pub/individual/lib/libXtst-1.2.3.tar.bz2
			https://www.x.org/pub/individual/lib/libXv-1.0.11.tar.bz2
			https://www.x.org/pub/individual/lib/libXvMC-1.0.10.tar.bz2
			https://www.x.org/pub/individual/lib/libXxf86dga-1.1.4.tar.bz2
			https://www.x.org/pub/individual/lib/libXxf86vm-1.1.4.tar.bz2
			https://www.x.org/pub/individual/lib/libdmx-1.1.3.tar.bz2
			https://www.x.org/pub/individual/lib/libpciaccess-0.13.5.tar.bz2
			https://www.x.org/pub/individual/lib/libxkbfile-1.0.9.tar.bz2
			https://www.x.org/pub/individual/lib/libxshmfence-1.2.tar.bz2
			https://downloads.sourceforge.net/freetype/freetype-2.8.tar.bz2
			https://downloads.sourceforge.net/freetype/freetype-doc-2.8.tar.bz2
			https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.12.4.tar.bz2
			https://xcb.freedesktop.org/dist/xcb-util-0.4.0.tar.bz2
			https://xcb.freedesktop.org/dist/xcb-util-image-0.4.0.tar.bz2
			https://xcb.freedesktop.org/dist/xcb-util-keysyms-0.4.0.tar.bz2
			https://xcb.freedesktop.org/dist/xcb-util-renderutil-0.3.9.tar.bz2
			https://xcb.freedesktop.org/dist/xcb-util-wm-0.4.1.tar.bz2
			https://xcb.freedesktop.org/dist/xcb-util-cursor-0.1.3.tar.bz2
		EOF
	msg_success
	return
}
_md5sum_list(){
	msg_line "	Creating wget-list: "
		cat > ${PARENT}/SOURCES/md5sum-blfs <<- EOF
			238d9969cc0de8b9105d972007d9d546	SOURCES/pciutils-3.5.5.tar.xz
			feeffb543c42d3a9790d4e77437b57db	SOURCES/blfs-bootscripts-20170731.tar.xz
			0f758d7e000c0f7f7d3792610fad70cb 	SOURCES/rsync-3.1.2.tar.gz
			2c68846471994897278364fc18730dd9	SOURCES/Python-3.6.2.tar.xz
		EOF
		#	Dependencies
		cat >> ${PARENT}/SOURCES/md5sum-blfs <<- EOF
			83b89587607e3eb65c70d361f13bab43	SOURCES/libffi-3.2.1.tar.gz
			29867814123c3d23056b1d05aada1b9d	SOURCES/libdrm-2.4.82.tar.bz2
			10f969f78a463704ae73529978148dbe	SOURCES/nettle-3.3.tar.gz
			03599aee98c9b726c7a732a2dd0245d5	SOURCES/elfutils-0.170.tar.bz2
			ae249165c173b1ff386ee8ad676815f5 	SOURCES/libxml2-2.9.4.tar.gz
			0235f6075c32c3be61cff94fa0b9f108 	SOURCES/wayland-1.14.0.tar.xz
			5217ef3e76a7275a2a3b569a12ddc989 	SOURCES/libgpg-error-1.27.tar.bz2
			530db74602b558209f9ad7356a680971	SOURCES/libgcrypt-1.8.0.tar.bz2
			2fa0b05a4f4d06791eec83bc9c854d14 	SOURCES/libvdpau-1.1.1.tar.bz2
			53b43534153bb2a0363f08bae8b9d990	SOURCES/Python-2.7.13.tar.xz
			7e583285b1fb8a76305d6d68f4ccc14e	SOURCES/funcsigs-1.0.2.tar.gz
			38b3fcdfa24faf97c6cf66991eb54e9c	SOURCES/Beaker-1.9.0.tar.gz
			2fcedc9284d50e577b5192e8e3578355	SOURCES/MarkupSafe-1.0.tar.gz
			c5fc31a323dd4990683d2f2da02d4e20	SOURCES/Mako-1.0.4.tar.gz
			a21a04d6ff5c4645c748220dbaa9f221	SOURCES/make-ca.sh-20170514
			ac4a59c38c47adc160ea71eace20257b	SOURCES/curl-7.55.1.tar.xz
			4583bd6b2ebf7e0e8963d90879eb1b27	SOURCES/libarchive-3.3.2.tar.gz
			00f43c6a56d4903436317c14f9ca7f37	SOURCE/cmake-3.9.1.tar.gz

		EOF
		#	Xorg
		cat >> ${PARENT}/SOURCES/md5sum-blfs <<- EOF
			6e76e546a4e580f15cebaf8019ef1625	SOURCES/util-macros-1.19.1.tar.bz2
			1a05fb01fa1d5198894c931cf925c025	SOURCES/bigreqsproto-1.1.2.tar.bz2
			98482f65ba1e74a08bf5b056a4031ef0	SOURCES/compositeproto-0.4.2.tar.bz2
			998e5904764b82642cc63d97b4ba9e95	SOURCES/damageproto-1.2.1.tar.bz2
			4ee175bbd44d05c34d43bb129be5098a	SOURCES/dmxproto-2.3.1.tar.bz2
			b2721d5d24c04d9980a0c6540cb5396a	SOURCES/dri2proto-2.8.tar.bz2
			a3d2cbe60a9ca1bf3aea6c93c817fee3	SOURCES/dri3proto-1.0.tar.bz2
			e7431ab84d37b2678af71e29355e101d	SOURCES/fixesproto-5.0.tar.bz2
			36934d00b00555eaacde9f091f392f97	SOURCES/fontsproto-2.1.3.tar.bz2
			5565f1b0facf4a59c2778229c1f70d10	SOURCES/glproto-1.4.17.tar.bz2
			b290a463af7def483e6e190de460f31a	SOURCES/inputproto-2.3.2.tar.bz2
			94afc90c1f7bef4a27fdd59ece39c878	SOURCES/kbproto-1.0.7.tar.bz2
			92f9dda9c870d78a1d93f366bcb0e6cd	SOURCES/presentproto-1.1.tar.bz2
			a46765c8dcacb7114c821baf0df1e797	SOURCES/randrproto-1.5.0.tar.bz2
			1b4e5dede5ea51906f1530ca1e21d216	SOURCES/recordproto-1.14.2.tar.bz2
			a914ccc1de66ddeb4b611c6b0686e274	SOURCES/renderproto-0.11.1.tar.bz2
			cfdb57dae221b71b2703f8e2980eaaf4	SOURCES/resourceproto-1.2.0.tar.bz2
			edd8a73775e8ece1d69515dd17767bfb	SOURCES/scrnsaverproto-1.2.2.tar.bz2
			fe86de8ea3eb53b5a8f52956c5cd3174	SOURCES/videoproto-2.3.3.tar.bz2
			5f4847c78e41b801982c8a5e06365b24	SOURCES/xcmiscproto-1.2.2.tar.bz2
			70c90f313b4b0851758ef77b95019584	SOURCES/xextproto-7.3.0.tar.bz2
			120e226ede5a4687b25dd357cc9b8efe	SOURCES/xf86bigfontproto-1.2.0.tar.bz2
			a036dc2fcbf052ec10621fd48b68dbb1	SOURCES/xf86dgaproto-2.1.tar.bz2
			1d716d0dac3b664e5ee20c69d34bc10e	SOURCES/xf86driproto-2.1.1.tar.bz2
			e793ecefeaecfeabd1aed6a01095174e	SOURCES/xf86vidmodeproto-2.3.1.tar.bz2
			9959fe0bfb22a0e7260433b8d199590a	SOURCES/xineramaproto-1.2.1.tar.bz2
			16791f7ca8c51a20608af11702e51083	SOURCES/xproto-7.0.31.tar.bz2
			685f8abbffa6d145c0f930f00703b21b	SOURCES/libXau-1.0.8.tar.bz2
			18aa5c1279b01f9d18e3299969665b2e	SOURCES/libXdmcp-1.1.2.tar.bz2
			14e60919f859560f28426a685a555962	SOURCES/xcb-proto-1.12.tar.bz2
			28e552bd78bc1050b6b26ca1db0e5bb6	SOURCES/libxcb-1.12.tar.bz2
			c5ba432dd1514d858053ffe9f4737dd8	SOURCES/xtrans-1.3.5.tar.bz2
			0f618db70c4054ca67cee0cc156a4255	SOURCES/libX11-1.6.5.tar.bz2
			52df7c4c1f0badd9f82ab124fb32eb97	SOURCES/libXext-1.3.3.tar.bz2
			d79d9fe2aa55eb0f69b1a4351e1368f7	SOURCES/libFS-1.0.7.tar.bz2
			addfb1e897ca8079531669c7c7711726	SOURCES/libICE-1.0.9.tar.bz2
			499a7773c65aba513609fe651853c5f3	SOURCES/libSM-1.2.2.tar.bz2
			7a773b16165e39e938650bcc9027c1d5	SOURCES/libXScrnSaver-1.2.2.tar.bz2
			8f5b5576fbabba29a05f3ca2226f74d3	SOURCES/libXt-1.1.5.tar.bz2
			41d92ab627dfa06568076043f3e089e4	SOURCES/libXmu-1.1.2.tar.bz2
			20f4627672edb2bd06a749f11aa97302	SOURCES/libXpm-3.5.12.tar.bz2
			e5e06eb14a608b58746bdd1c0bd7b8e3	SOURCES/libXaw-1.0.13.tar.bz2
			07e01e046a0215574f36a3aacb148be0	SOURCES/libXfixes-5.0.3.tar.bz2
			f7a218dcbf6f0848599c6c36fc65c51a	SOURCES/libXcomposite-0.4.4.tar.bz2
			802179a76bded0b658f4e9ec5e1830a4	SOURCES/libXrender-0.9.10.tar.bz2
			1e7c17afbbce83e2215917047c57d1b3	SOURCES/libXcursor-1.1.14.tar.bz2
			0cf292de2a9fa2e9a939aefde68fd34f	SOURCES/libXdamage-1.1.4.tar.bz2
			0920924c3a9ebc1265517bdd2f9fde50	SOURCES/libfontenc-1.1.3.tar.bz2
			0d9f6dd9c23bf4bcbfb00504b566baf5	SOURCES/libXfont2-2.0.1.tar.bz2
			331b3a2a3a1a78b5b44cfbd43f86fcfe	SOURCES/libXft-2.3.2.tar.bz2
			1f0f2719c020655a60aee334ddd26d67	SOURCES/libXi-1.7.9.tar.bz2
			9336dc46ae3bf5f81c247f7131461efd	SOURCES/libXinerama-1.1.3.tar.bz2
			28e486f1d491b757173dd85ba34ee884	SOURCES/libXrandr-1.5.1.tar.bz2
			45ef29206a6b58254c81bea28ec6c95f	SOURCES/libXres-1.0.7.tar.bz2
			ef8c2c1d16a00bd95b9fdcef63b8a2ca	SOURCES/libXtst-1.2.3.tar.bz2
			210b6ef30dda2256d54763136faa37b9	SOURCES/libXv-1.0.11.tar.bz2
			4cbe1c1def7a5e1b0ed5fce8e512f4c6	SOURCES/libXvMC-1.0.10.tar.bz2
			d7dd9b9df336b7dd4028b6b56542ff2c	SOURCES/libXxf86dga-1.1.4.tar.bz2
			298b8fff82df17304dfdb5fe4066fe3a	SOURCES/libXxf86vm-1.1.4.tar.bz2
			ba983eba5a9f05d152a0725b8e863151	SOURCES/libdmx-1.1.3.tar.bz2
			d810ab17e24c1418dedf7207fb2841d4	SOURCES/libpciaccess-0.13.5.tar.bz2
			4a4cfeaf24dab1b991903455d6d7d404	SOURCES/libxkbfile-1.0.9.tar.bz2
			66662e76899112c0f99e22f2fc775a7e	SOURCES/libxshmfence-1.2.tar.bz2
			2413ac3eaf508ada019c63959ea81a92	SOURCES/freetype-2.8.tar.bz2
			29105662c7d319720e0088a0ac53f494	SOURCES/fontconfig-2.12.4.tar.bz2
			2e97feed81919465a04ccc71e4073313	SOURCES/xcb-util-0.4.0.tar.bz2
			08fe8ffecc8d4e37c0ade7906b3f4c87	SOURCES/xcb-util-image-0.4.0.tar.bz2
			1022293083eec9e62d5659261c29e367	SOURCES/xcb-util-keysyms-0.4.0.tar.bz2
			468b119c94da910e1291f3ffab91019a	SOURCES/xcb-util-renderutil-0.3.9.tar.bz2
			87b19a1cd7bfcb65a24e36c300e03129	SOURCES/xcb-util-wm-0.4.1.tar.bz2
			6ac3b17cba51aaaa36ba035a53527214	SOURCES/xcb-util-cursor-0.1.3.tar.bz2
		EOF
	msg_success

	return
}
_copy_source() {
	#	Copy build system to $LFS
	#	Directories to copy
	msg_line "	Installing build system: "
		cp -ar *  ${PARENT}
		chmod 777 ${PARENT}/*.sh
	msg_success
	return
}
#
#	Main line
#
[ -z ${PARENT} ]		&& { echo "${PRGNAME}: PARENT: not set";exit 1; }
[ -z ${LOGFILE} ]		&& { echo "${PRGNAME}: LOGFILE: not set";exit 1; }
_copy_source			#	Copy build system to $LFS
_wget_list			#	Create wget list
_md5sum_list			#	Create md5sum list
end-run