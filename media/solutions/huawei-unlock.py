#!/usr/bin/env python
#
# Copyright 2010: dogbert <dogber1@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import hashlib, getopt, sys

def info():
	print "huawei-unlock.py: calculates unlock codes for Huawei modems"
	print "Copyright (c) 2010 dogbert <dogber1@gmail.com>"
	print "For information and updates, visit http://dogber1.blogspot.com"
	print ""

def usage():
	print "Options: -i*, --imei=*      IMEI of the device"
	print ""
	print "Example: huawei-unlock.py --imei=351234567891239"
	print ""

def testIMEIChecksum(digits):
	_sum = 0
	alt = False
	for d in reversed(digits):
		assert 0 <= d <= 9
		if alt:
			d *= 2
		if d > 9:
			d -= 9
		_sum += d
		alt = not alt
	return (_sum % 10) == 0

def checkIMEI(imei):
	digits = []
	if len(imei) != 15:
		print "IMEI too short/long"
		return False
	for i in imei:
		digits.append(int(i))
	if not testIMEIChecksum(digits):
		print "IMEI checksum invalid"
		return False
	return True

def getCode(imei, salt):
	digest = hashlib.md5((imei+salt).lower()).digest()
	code = 0
	for i in range(0,4):
		code += (ord(digest[i])^ord(digest[4+i])^ord(digest[8+i])^ord(digest[12+i])) << (3-i)*8
	code &= 0x1ffffff
	code |= 0x2000000
	return code

def main():
	info()
        try:   
                opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help", "imei="])
        except getopt.GetoptError, err:
                print str(err) # will print something like "option -a not recognized"
                usage()
                sys.exit(2)

	imei = ""
	interactive = False

        for o, a in opts:
                if o in ("-i", "--imei"):
                        imei = a
                elif o in ("-h", "--help"):
                        usage()
                        sys.exit()

	if imei == "":
		imei = raw_input("Please enter the IMEI of the device: ")
		interactive = True

	if checkIMEI(imei):
		print "Unlock Code: %d" % (getCode(imei, hashlib.md5("hwe620datacard").hexdigest()[8:24]))
		print "Flash Code:  %d" % (getCode(imei, hashlib.md5("e630upgrade").hexdigest()[8:24]))
		print "done."

	if interactive:
		raw_input()
	
if __name__ == "__main__":
	main()
