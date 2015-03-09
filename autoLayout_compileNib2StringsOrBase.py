#!/usr/bin/env python
#coding=utf-8

__author__ = 'TinyLiu@wistronits.com;TinyLiu@me.com'

'''# To compile nib for autolayout further runtime testing.'''
# 2015-01-23 update: solution for case which has space in file path

import os, sys, time
from socket import *

def client(locenv, script):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('10.4.2.6', 8989))
        s.send('%s process script %s in %s'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) , script, locenv))
        s.close()
    except:
        pass

def resetibtool():
	if not os.path.isdir('/Applications/Xcode.app'):
		while True:
			xcode = raw_input('## Can not detect Xcode, please assgin manually: ').strip()
			if xcode[-23:] == '/Applications/Xcode.app':
				return '%s/Contents/Developer/usr/bin/ibtool'%xcode
	else:
		return 'ibtool'

def nib2strings(nib, ibtool='ibtool'):
	localization = ['/Applications/', '/Library/', '/System/']
	targetStrings = ''
	for folder in localization:
		if folder in nib:
			targetStrings = nib[nib.find(folder):][:-3] + 'strings'
	targetStrings = targetStrings.replace(' ', '\ ')
	if not targetStrings:
		targetStrings = raw_input('Export to (filename.strings): ')
		if os.path.isdir(targetStrings) and '.nib' not in targetStrings:
			targetStrings = targetStrings + os.path.basename(nib)[:-4] + '.strings'

	targetNib = targetStrings[:-7] + 'nib'
	nib = nib.replace(' ', '\ ')
	os.system('sudo %s %s --export-strings-file %s'%(ibtool, nib, targetStrings))

	if os.path.exists(targetNib):
		os.system('sudo chmod -R 777 %s'%os.path.dirname(targetNib))
		os.rename(targetNib, '%s_org.nib'%targetNib[:-4])

def nib2base(nib, ibtool='ibtool'):
	localization = ['/Applications/', '/Library/', '/System/']
	targetBase = ''
	for folder in localization:
		if folder in nib:
			targetBase = nib[nib.find(folder):].replace(' ', '\ ')

	if not targetBase:
		targetBase = raw_input('Export to (Base.lproj/filename.nib): ')

	if os.path.exists(targetBase):
		os.system('sudo chmod -R 777 %s'%os.path.dirname(targetBase))
		try:
			os.rename(targetBase, '%s_org.nib'%targetBase[:-4])
		except:
			pass
	nib = nib.replace(' ', '\ ')
	os.system('sudo %s --compile %s --reference-external-strings %s'%(ibtool, targetBase, nib))

def main():
	if len(sys.argv) < 2:
		print '\n## usage: %s path/to/filename.nib {nib2base}\n\nScript can run nib2base and nib2strings automatically.\n\nEnter the second arg, fource to run nib2base.\n'%sys.argv[0]
		sys.exit()
	if sys.argv[1][-4:] != '.nib' or not os.path.isdir(sys.argv[1]):
		print '\n## Please enter an uncompiled nib file.\n'
		sys.exit()
	try:
		b = sys.argv[2]
		nib2base(sys.argv[1], resetibtool())
	except IndexError:
		if '/Base.lproj/' in sys.argv[1]:
			nib2base(sys.argv[1], resetibtool())
		else:
			nib2strings(sys.argv[1], resetibtool())
	client(sys.argv[1], 'nib2strings_nib2base')
if __name__ == '__main__':
	main()
