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