Summary: SELinux binary policy manipulation library
Name: libsepol
Version: 2.9
Release: 3%{?dist}
License: LGPLv2+
Source0: https://github.com/SELinuxProject/selinux/releases/download/20190315/libsepol-2.9.tar.gz
Patch0001: 0001-libsepol-cil-Fix-out-of-bound-read-of-file-context-p.patch
Patch0002: 0002-libsepol-cil-Destroy-classperms-list-when-resetting-.patch
Patch0003: 0003-libsepol-cil-Destroy-classperm-list-when-resetting-m.patch
Patch0004: 0004-libsepol-cil-cil_reset_classperms_set-should-not-res.patch
Patch0005: 0005-libsepol-cil-Set-class-field-to-NULL-when-resetting-.patch
Patch0006: 0006-libsepol-cil-More-strict-verification-of-constraint-.patch
Patch0007: 0007-libsepol-cil-Exit-with-an-error-if-declaration-name-.patch
Patch0008: 0008-libsepol-cil-Allow-permission-expressions-when-using.patch
Patch0009: 0009-libsepol-cil-Reorder-checks-for-invalid-rules-when-b.patch
Patch0010: 0010-libsepol-cil-Cleanup-build-AST-helper-functions.patch
Patch0011: 0011-libsepol-cil-Create-new-first-child-helper-function-.patch
Patch0012: 0012-libsepol-cil-Remove-unused-field-from-struct-cil_arg.patch
Patch0013: 0013-libsepol-cil-Destroy-disabled-optional-blocks-after-.patch
Patch0014: 0014-libsepol-cil-Check-if-name-is-a-macro-parameter-firs.patch
Patch0015: 0015-libsepol-cil-fix-NULL-pointer-dereference-in-__cil_i.patch
Patch0016: 0016-libsepol-cil-Report-disabling-an-optional-block-only.patch
Patch0017: 0017-libsepol-cil-Use-AST-to-track-blocks-and-optionals-w.patch
Patch0018: 0018-libsepol-cil-Reorder-checks-for-invalid-rules-when-r.patch
Patch0019: 0019-libsepol-cil-Sync-checks-for-invalid-rules-in-boolea.patch
Patch0020: 0020-libsepol-cil-Check-for-statements-not-allowed-in-opt.patch
URL: https://github.com/SELinuxProject/selinux/wiki
BuildRequires: gcc
BuildRequires: flex

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libsepol provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package devel
Summary: Header files and libraries used to build policy manipulation tools
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The libsepol-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies. 

%package static
Summary: static libraries used to build policy manipulation tools
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The libsepol-static package contains the static libraries and header files
needed for developing applications that manipulate binary policies. 

%prep
%autosetup -p 2 -n libsepol-%{version}

# sparc64 is an -fPIC arch, so we need to fix it here
%ifarch sparc64
sed -i 's/fpic/fPIC/g' src/Makefile
%endif

%build
make clean
make %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags}"

%install
mkdir -p ${RPM_BUILD_ROOT}/%{_lib} 
mkdir -p ${RPM_BUILD_ROOT}/%{_libdir} 
mkdir -p ${RPM_BUILD_ROOT}%{_includedir} 
mkdir -p ${RPM_BUILD_ROOT}%{_bindir} 
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
make DESTDIR="${RPM_BUILD_ROOT}" LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}" install
rm -f ${RPM_BUILD_ROOT}%{_bindir}/genpolbools
rm -f ${RPM_BUILD_ROOT}%{_bindir}/genpolusers
rm -f ${RPM_BUILD_ROOT}%{_bindir}/chkcon
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man8
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/ru/man8

%post
/sbin/ldconfig
exit 0

%postun -p /sbin/ldconfig

%files static
%{_libdir}/libsepol.a

%files devel
%{_libdir}/libsepol.so
%{_libdir}/pkgconfig/libsepol.pc
%{_includedir}/sepol/*.h
%{_mandir}/man3/*.3.gz
%dir %{_includedir}/sepol
%dir %{_includedir}/sepol/policydb
%{_includedir}/sepol/policydb/*.h
%dir %{_includedir}/sepol/cil
%{_includedir}/sepol/cil/*.h

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/libsepol.so.1

%changelog
* Wed Aug 18 2021 Vit Mojzis <vmojzis@redhat.com> - 2.9-3
- cil: Fix out-of-bound read of file context pattern ending with "\"
- cil: Destroy classperms list when resetting classpermission (#1983517)
- cil: Destroy classperm list when resetting map perms (#1983521)
- cil: cil_reset_classperms_set() should not reset classpermission (#1983525)
- cil: Set class field to NULL when resetting struct cil_classperms
- cil: More strict verification of constraint leaf expressions
- cil: Exit with an error if declaration name is a reserved word
- cil: Allow permission expressions when using map classes
- cil: Reorder checks for invalid rules when building AST
- cil: Cleanup build AST helper functions
- cil: Create new first child helper function for building AST
- cil: Remove unused field from struct cil_args_resolve
- cil: Destroy disabled optional blocks after pass is complete
- cil: Check if name is a macro parameter first
- cil: fix NULL pointer dereference in __cil_insert_name
- cil: Report disabling an optional block only at high verbose levels
- cil: Use AST to track blocks and optionals when resolving
- cil: Reorder checks for invalid rules when resolving AST
- cil: Sync checks for invalid rules in booleanifs
- cil: Check for statements not allowed in optional blocks (#1983530)

* Wed Jan 06 2021 Vit Mojzis <vmojzis@redhat.com> - 2.9-2
- Drop unnecessary telinit (#1838257)

* Mon Mar 18 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-1
- SELinux userspace 2.9 release

* Mon Nov  5 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-2
- Fix RESOURCE_LEAK coverity scan defects

* Fri May 25 2018 Petr Lautrbach <plautrba@workstation> - 2.8-1
- SELinux userspace 2.8 release

* Mon May 14 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc3.1
- SELinux userspace 2.8-rc1 release candidate

* Mon Apr 23 2018 Petr Lautrbach <plautrba@redhat.com> - 2.0-0.rc1.1
- SELinux userspace 2.8-rc1 release candidate

* Wed Mar 21 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-6
- Prevent freeing unitialized value in ibendport handling
- Add support for the SCTP portcon keyword
- Export sepol_polcap_getnum/name functions

* Tue Mar 13 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-5
- cil: Create new keep field for type attribute sets
- build: follow standard semantics for DESTDIR and PREFIX
- cil: show an error when cil_expr_to_string() fails

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-3
- free ibendport device names

* Fri Oct 20 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-2
- reset pointer after free in cil_strpool_destroy()
- cil: Add ability to redeclare types[attributes]
- cil: Keep attributes used by generated attributes in neverallow rules
- use IN6ADDR_ANY_INIT to initialize IPv6 addresses
- fix memory leak in sepol_bool_query()
- cil: drop wrong unused attribute
- cil: fix -Wwrite-strings warning
- cil: __cil_post_db_neverallow_attr_helper() does not use extra_args

* Mon Aug 07 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-1
- Update to upstream release 2017-08-04

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2.6-4
- Rebuild with binutils fix for ppc64le (#1475636)

* Fri Jul 28 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-3
- Fix neverallow bug when checking conditional policy
- Destroy the expanded level when mls_semantic_level_expand() fails
- Do not seg fault on sepol_*_key_free(NULL)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Feb 12 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-1
- Update to upstream release 2016-10-14

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 03 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-10
- Check for too many permissions in classes and commons in CIL
- Fix xperm mapping between avrule and avtab
- tests: Fix mispelling of optimization option
- Fix unused/uninitialized variables on mac build
- Produce more meaningful error messages for conflicting type rules in CIL
- make "make test" fail when a CUnit test fails
- tests: fix g_b_role_2 test
- Change which attributes CIL keeps in the binary policy
- Port str_read() from kernel and remove multiple occurances of similar code
- Use calloc instead of malloc for all the *_to_val_structs
- Fix bugs found by AFL
- Fix memory leak in expand.c
- Fix invalid read when policy file is corrupt
- Fix possible use of uninitialized variables

* Mon Aug 01 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-9
- Warn instead of fail if permission is not resolved
- Ignore object_r when adding userrole mappings to policydb

* Thu Jul 14 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-8
- Add missing return to sepol_node_query()
- Add missing <stdarg.h> include

* Thu Jun 23 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-7
- Correctly detect unknown classes in sepol_string_to_security_class
- Sort object files for deterministic linking order
- Fix neverallowxperm checking on attributes
- Remove libsepol.map when cleaning
- Add high-level language line marking support to CIL

* Fri May 06 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-6
- Change logic of bounds checking to match change in kernel
- Fix multiple spelling errors

* Mon May 02 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-5
- Only apply bounds checking to source types in rules
- Fix CIL and not add an attribute as a type in the attr_type_map

* Fri Apr 29 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-4
- Build policy on systems not supporting DCCP protocol
- Fix extended permissions neverallow checking
- Fix CIL neverallow and bounds checking
- Android.mk: Add -D_GNU_SOURCE to common_cflags

* Fri Apr 08 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-3
- Fix bug in CIL when resetting classes
- Add support for portcon dccp protocol

* Sun Feb 28 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-2
- Use fully versioned arch-specific requires

* Tue Feb 23 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-1
- Update to upstream release 2016-02-23

* Sun Feb 21 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-0.1.rc1
- Update to upstream rc1 release 2016-01-07

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 25 2015 Michal Srb <msrb@redhat.com> - 2.4-3
- Improve compatibility with Python 3 SWIG bindings
- Resolves: rhbz#1247714

* Fri Aug 14 2015 Adam Jackson <ajax@redhat.com> 2.4-2
- Pass ldflags to make so hardening works

* Mon Apr 13 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-0.1
- Update to upstream release 2.4

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.3-3
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 6 2014 Dan Walsh <dwalsh@redhat.com> - 2.3-1
- Update to upstream 
	* Improve error message for name-based transition conflicts.
	* Revert libsepol: filename_trans: use some better sorting to compare and merge.
	* Report source file and line information for neverallow failures.
	* Fix valgrind errors in constraint_expr_eval_reason from Richard Haines.
	* Add sepol_validate_transition_reason_buffer function from Richard Haines.

* Thu Oct 31 2013 Dan Walsh <dwalsh@redhat.com> - 2.2-1
- Update to upstream 
- Richard Haines patch V1 Allow constraint denials to be determined.
- Add separate role declarations as required by modern checkpolicy.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 7 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.9-1
- Update to upstream 
- filename_trans: use some better sorting to compare and merge
- coverity fixes
- implement default type policy syntax
- Fix memory leak issues found by Klocwork
- Add CONTRAINT_NAMES to the kernel 

* Sun Jan 27 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.8-8
- Update to latest patches from eparis/Upstream

* Fri Jan 25 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.8-7
- Update to latest patches from eparis/Upstream

* Tue Jan 8 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.8-6
- Fix libsepol.stack messages in audit2allow/audit2why

* Fri Jan 4 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.8-5
- Update to latest patches from eparis/Upstream

* Tue Nov 27 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.8-4
- Update Richard Haines patch to show constraint information

* Mon Nov 19 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.8-3
- Add sepol_compute_av_reason_buffer patch from Richard Haines

* Wed Sep 19 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.8-2
- Revert patch that was attempting to expand filetrans attributes, but is breaking filetrans rules

* Thu Sep 13 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.8-1
- Update to upstream 
	* fix neverallow checking on attributes
	* Move context_copy() after switch block in ocontext_copy_*().
	* check for missing initial SID labeling statement.
	* Add always_check_network policy capability
	* role_fix_callback skips out-of-scope roles during expansion.

* Mon Jul 30 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.7-4
- Try new patches

* Tue Jul 24 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.7-3
- Revert patches

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 4 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.7-1
- Update to upstream 
	* reserve policycapability for redhat testing of ptrace child
	* cosmetic changes to make the source easier to read
	* prepend instead of append to filename_trans list
	* Android/MacOS X build support
	* allocate enough space to hold filename in trans rules

* Mon Apr 23 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.5-3
- Fix off by one error that is causing file_name transition rules to be expanded- incorrectly on i686 machines

* Tue Apr 17 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.5-2
- Add support for ptrace_child

* Thu Mar 29 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.5-1
- Update to upstream 
  * checkpolicy: implement new default labeling behaviors

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-5
- Update to match eparis pool

* Thu Dec 15 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-4
- Additional fix for default transitioning labeling for semodule

* Thu Dec 15 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-3
- Add Eparis patch for handling of default transition labeling

* Mon Dec 5 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-2
- Allow policy to specify the source of target for generating the default user,role 
- or mls label for a new target.

* Fri Nov 4 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-1
- Update to upstream 
	* regenerate .pc on VERSION change
	* Move ebitmap_* functions from mcstrans to libsepol
	* expand: do filename_trans type comparison on mapped representation

* Mon Oct 31 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.3-2
-The filename_trans code had a bug where duplicate detection was being
done between the unmapped type value of a new rule and the type value of
rules already in policy.  This meant that duplicates were not being
silently dropped and were instead outputting a message that there was a
problem.  It made things hard because the message WAS using the mapped
type to convert to the string representation, so it didn't look like a
dup!

* Mon Sep 19 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.3-1
-Update to upstream
	* Skip writing role attributes for policy.X and
	* Indicate when boolean is indeed a tunable.
	* Separate tunable from boolean during compile.
	* Write and read TUNABLE flags in related
	* Copy and check the cond_bool_datum_t.flags during link.
	* Permanently discard disabled branches of tunables in
	* Skip tunable identifier and cond_node_t in expansion.
	* Create a new preserve_tunables flag
	* Preserve tunables when required by semodule program.
	* setools expects expand_module_avrules to be an exported
	* tree: default make target to all not

* Thu Sep 15 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.2-3
- Add patch to handle preserving tunables

* Thu Sep 1 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.2-2
- export expand_module_avrules 

* Thu Aug 18 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.2-0
- Update to upstream 
	* Only call role_fix_callback for base.p_roles during expansion.
	* use mapped role number instead of module role number

* Mon Aug 1 2011 Dan Walsh <dwalsh@redhat.com> 2.1.1-1
- Update to upstream 
	* Minor fix to reading policy with filename transition rules

* Wed Jul 27 2011 Dan Walsh <dwalsh@redhat.com> 2.1.0-1
- Update to upstream 
	* Release, minor version bump

* Tue May 3 2011 Dan Walsh <dwalsh@redhat.com> 2.0.45-1
- Update to upstream 
  * Warn if filename_trans rules are dropped by Steve Lawrence.

* Thu Apr 21 2011 Dan Walsh <dwalsh@redhat.com> 2.0.44-2
- Fixes for new role_transition class field by Eric Paris.

* Thu Apr 14 2011 Dan Walsh <dwalsh@redhat.com> 2.0.44-1
-Update to upstream
	* Fixes for new role_transition class field by Eric Paris.
	* Add libsepol support for filename_trans rules by Eric Paris.

* Tue Apr 12 2011 Dan Walsh <dwalsh@redhat.com> 2.0.43-3
- re-add Erics patch for filename transitions
	
* Tue Apr 12 2011 Dan Walsh <dwalsh@redhat.com> 2.0.43-1
-Update to upstream
	* Add new class field in role_transition by Harry Ciao.

* Tue Mar 29 2011 Dan Walsh <dwalsh@redhat.com> 2.0.42-3
- Apply Eparis Patch
  This patch add libsepol support for filename_trans rules.  These rules
allow on to make labeling decisions for new objects based partially on
the last path component.  They are stored in a list.  If we find that
the number of rules grows to an significant size I will likely choose to
store these in a hash, both in libsepol and in the kernel.  But as long
as the number of such rules stays small, this should be good.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Dan Walsh <dwalsh@redhat.com> 2.0.42-1
- Upgrade to latest from NSA
  * Fix compliation under GCC 4.6 by Justin Mattock

* Thu Feb 18 2010 Dan Walsh <dwalsh@redhat.com> 2.0.41-3
- Fix libsepol.pc file

* Thu Jan 28 2010 Dan Walsh <dwalsh@redhat.com> 2.0.41-2
- Resolve specfile problems
Resolves: #555835

* Wed Nov 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.41-1
- Upgrade to latest from NSA
  * Fixed typo in error message from Manoj Srivastava.

* Mon Nov 2 2009 Dan Walsh <dwalsh@redhat.com> 2.0.40-1
- Upgrade to latest from NSA
  * Add pkgconfig file from Eamon Walsh.

* Wed Oct 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.39-1
- Upgrade to latest from NSA
  * Add support for building Xen policies from Paul Nuzzi.

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> 2.0.38-1
- Upgrade to latest from NSA
  * Check last offset in the module package against the file size.
  Reported by Manoj Srivastava for bug filed by Max Kellermann.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 7 2009 Dan Walsh <dwalsh@redhat.com> 2.0.37-1
- Upgrade to latest from NSA
  * Add method to check disable dontaudit flag from Christopher Pardy.

* Wed Mar 25 2009 Dan Walsh <dwalsh@redhat.com> 2.0.36-1
- Upgrade to latest from NSA
  * Fix boolean state smashing from Joshua Brindle.

* Thu Mar 5 2009 Dan Walsh <dwalsh@redhat.com> 2.0.35-3
- Fix license specification to be LGPL instead of GPL

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.35-2

* Wed Feb 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.35-1
- Upgrade to latest from NSA
        * Fix alias field in module format, caused by boundary format change
          from Caleb Case.

* Tue Oct 14 2008 Dan Walsh <dwalsh@redhat.com> 2.0.34-1
- Upgrade to latest from NSA
  * Add bounds support from KaiGai Kohei.
  * Fix invalid aliases bug from Joshua Brindle.

* Tue Sep 30 2008 Dan Walsh <dwalsh@redhat.com> 2.0.33-1
- Upgrade to latest from NSA
  * Revert patch that removed expand_rule.

* Mon Jul 7 2008 Dan Walsh <dwalsh@redhat.com> 2.0.32-1
- Upgrade to latest from NSA
  * Allow require then declare in the source policy from Joshua Brindle.

* Sun Jun 22 2008 Dan Walsh <dwalsh@redhat.com> 2.0.31-1
- Upgrade to latest from NSA
  * Fix mls_semantic_level_expand() to handle a user require w/o MLS information from Stephen Smalley.

* Wed Jun 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.30-1
- Upgrade to latest from NSA
  * Fix endianness bug in the handling of network node addresses from Stephen Smalley.
    Only affects big endian platforms.
    Bug reported by John Weeks of Sun upon policy mismatch between x86 and sparc.

* Wed May 28 2008 Dan Walsh <dwalsh@redhat.com> 2.0.29-1
- Upgrade to latest from NSA
  * Merge user and role mapping support from Joshua Brindle.

* Mon May 19 2008 Dan Walsh <dwalsh@redhat.com> 2.0.28-1
- Upgrade to latest from NSA
  * Fix mls_level_convert() to gracefully handle an empty user declaration/require from Stephen Smalley.
  * Belatedly merge test for policy downgrade from Todd Miller.

* Thu Mar 27 2008 Dan Walsh <dwalsh@redhat.com> 2.0.26-1
- Upgrade to latest from NSA
  * Add permissive domain support from Eric Paris.

* Thu Mar 13 2008 Dan Walsh <dwalsh@redhat.com> 2.0.25-1
- Upgrade to latest from NSA
  * Drop unused ->buffer field from struct policy_file.
  * Add policy_file_init() initalizer for struct policy_file and use it, from Todd C. Miller.


* Thu Feb 28 2008 Dan Walsh <dwalsh@redhat.com> 2.0.23-1
- Upgrade to latest from NSA
  * Accept "Flask" as an alternate identifier string in kernel policies from Stephen Smalley.
  * Add support for open_perms policy capability from Eric Paris.

* Wed Feb 20 2008 Dan Walsh <dwalsh@redhat.com> 2.0.21-1
- Upgrade to latest from NSA
  * Fix invalid memory allocation in policydb_index_others() from Jason Tang.

* Mon Feb 4 2008 Dan Walsh <dwalsh@redhat.com> 2.0.20-1
- Upgrade to latest from NSA
  * Port of Yuichi Nakamura's tune avtab to reduce memory usage patch from the kernel avtab to libsepol from Stephen Smalley.

* Sat Feb 2 2008 Dan Walsh <dwalsh@redhat.com> 2.0.19-1
- Upgrade to latest from NSA
  * Add support for consuming avrule_blocks during expansion to reduce
    peak memory usage.

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> 2.0.18-2
- Fixed for spec review

* Fri Jan 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.18-1
- Upgrade to latest from NSA
  * Added support for policy capabilities from Todd Miller.
  * Prevent generation of policy.18 with MLS enabled from Todd Miller.

* Mon Dec 10 2007 Dan Walsh <dwalsh@redhat.com> 2.0.16-1
- Upgrade to latest from NSA
  * print module magic number in hex on mismatch, from Todd Miller.

* Fri Nov 30 2007 Dan Walsh <dwalsh@redhat.com> 2.0.15-1
- Upgrade to latest from NSA
  * clarify and reduce neverallow error reporting from Stephen Smalley.

* Tue Nov 6 2007 Dan Walsh <dwalsh@redhat.com> 2.0.14-1
- Upgrade to latest from NSA
  * Reject self aliasing at link time from Stephen Smalley.
  * Allow handle_unknown in base to be overridden by semanage.conf from Stephen Smalley.
  * Fixed bug in require checking from Stephen Smalley.
  * Added user hierarchy checking from Todd Miller.  

* Wed Sep 26 2007 Dan Walsh <dwalsh@redhat.com> 2.0.11-1
  * Pass CFLAGS to CC even on link command, per Dennis Gilmore.

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.10-1
- Upgrade to latest from NSA
  * Merged support for the handle_unknown policydb flag from Eric Paris.

* Fri Aug 31 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-1
- Upgrade to latest from NSA
  * Moved next_entry and put_entry out-of-line to reduce code size from Ulrich Drepper.
  * Fixed module_package_read_offsets bug introduced by the prior patch.

* Thu Aug 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-1
- Upgrade to latest from NSA
  * Eliminate unaligned accesses from policy reading code from Stephen Smalley.

* Mon Aug 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.6-1
- Upgrade to latest from NSA
  * Allow dontaudits to be turned off during policy expansion


* Fri Aug 10 2007 Dan Walsh <dwalsh@redhat.com> 2.0.5-1
- Upgrade to latest from NSA
     * Fix sepol_context_clone to handle a NULL context correctly.
          This happens for e.g. semanage_fcontext_set_con(sh, fcontext, NULL)
    to set the file context entry to "<<none>>".
- Apply patch from Joshua Brindle to disable dontaudit rules


* Thu Jun 21 2007 Dan Walsh <dwalsh@redhat.com> 2.0.4-1
- Upgrade to latest from NSA
  * Merged error handling patch from Eamon Walsh.

* Tue Apr 17 2007 Dan Walsh <dwalsh@redhat.com> 2.0.3-1
- Upgrade to latest from NSA
  * Merged add boolmap argument to expand_module_avrules() from Chris PeBenito.

* Fri Mar 30 2007 Dan Walsh <dwalsh@redhat.com> 2.0.2-1
- Upgrade to latest from NSA
  * Merged fix from Karl to remap booleans at expand time to 
    avoid holes in the symbol table.

* Wed Feb 7 2007 Dan Walsh <dwalsh@redhat.com> 2.0.1-1
- Upgrade to latest from NSA
  * Merged libsepol segfault fix from Stephen Smalley for when
    sensitivities are required but not present in the base.
  * Merged patch to add errcodes.h to libsepol by Karl MacMillan.
  
* Fri Jan 19 2007 Dan Walsh <dwalsh@redhat.com> 1.16.0-1
- Upgrade to latest from NSA
  * Updated version for stable branch.

* Tue Dec 12 2006 Adam Jackson <ajax@redhat.com> 1.15.3-1
- Add dist tag and rebuild, fixes 6 to 7 upgrades.

* Tue Nov 28 2006 Dan Walsh <dwalsh@redhat.com> 1.15.3-1
- Upgrade to latest from NSA
  * Merged patch to compile wit -fPIC instead of -fpic from
    Manoj Srivastava to prevent hitting the global offest table
    limit. Patch changed to include libselinux and libsemanage in
    addition to libselinux.

* Wed Nov 1 2006 Dan Walsh <dwalsh@redhat.com> 1.15.2-1
- Upgrade to latest from NSA
  * Merged fix from Karl MacMillan for a segfault when linking
    non-MLS modules with users in them.

* Tue Oct 24 2006 Dan Walsh <dwalsh@redhat.com> 1.15.1-1
- Upgrade to latest from NSA
  * Merged fix for version comparison that was preventing range
    transition rules from being written for a version 5 base policy
    from Darrel Goeddel.

* Tue Oct 17 2006 Dan Walsh <dwalsh@redhat.com> 1.14-1
- NSA Released version - Same as previous but changed release number

* Tue Oct 17 2006 Dan Walsh <dwalsh@redhat.com> 1.12.28-1
- Upgrade to latest from NSA
  * Build libsepol's static object files with -fpic

* Thu Sep 28 2006 Dan Walsh <dwalsh@redhat.com> 1.12.27-1
- Upgrade to latest from NSA
  * Merged mls user and range_transition support in modules
    from Darrel Goeddel

* Wed Sep 6 2006 Dan Walsh <dwalsh@redhat.com> 1.12.26-1
- Upgrade to latest from NSA
  * Merged range transition enhancements and user format changes
    Darrel Goeddel

* Fri Aug 25 2006 Dan Walsh <dwalsh@redhat.com> 1.12.25-3
- Fix location of include directory to devel package

* Fri Aug 25 2006 Dan Walsh <dwalsh@redhat.com> 1.12.25-2
- Remove invalid Requires 

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 1.12.25-1
- Upgrade to latest from NSA
  * Merged conditionally expand neverallows patch from Jeremy Mowery.
  * Merged refactor expander patch from Jeremy Mowery.

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 1.12.24-1
- Upgrade to latest from NSA
  * Merged libsepol unit tests from Joshua Brindle.
  * Merged symtab datum patch from Karl MacMillan.
  * Merged netfilter contexts support from Chris PeBenito.

* Tue Aug 1 2006 Dan Walsh <dwalsh@redhat.com> 1.12.21-1
- Upgrade to latest from NSA
  * Merged helpful hierarchy check errors patch from Joshua Brindle.
  * Merged semodule_deps patch from Karl MacMillan.
    This adds source module names to the avrule decls.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.12.19-1.1
- rebuild

* Tue Jul 4 2006 Dan Walsh <dwalsh@redhat.com> 1.12.19-1
- Upgrade to latest from NSA
  * Lindent.
  * Merged optionals in base take 2 patch set from Joshua Brindle.

* Tue Jun 13 2006 Bill Nottingham <notting@redhat.com> 1.12.17-2
- bump so it's newer than the FC5 version

* Mon Jun 5 2006 Dan Walsh <dwalsh@redhat.com> 1.12.17-1
- Upgrade to latest from NSA
  * Revert 1.12.16.
  * Merged cleaner fix for bool_ids overflow from Karl MacMillan,
    replacing the prior patch.
  * Merged fixes for several memory leaks in the error paths during
    policy read from Serge Hallyn.

* Tue May 30 2006 Dan Walsh <dwalsh@redhat.com> 1.12.14-1
- Upgrade to latest from NSA
  * Fixed bool_ids overflow bug in cond_node_find and cond_copy_list,
    based on bug report and suggested fix by Cedric Roux.
  * Merged sens_copy_callback, check_role_hierarchy_callback,
    and node_from_record fixes from Serge Hallyn.

* Tue May 23 2006 Dan Walsh <dwalsh@redhat.com> 1.12.12-1
- Upgrade to latest from NSA
  * Added sepol_policydb_compat_net() interface for testing whether
    a policy requires the compatibility support for network checks
    to be enabled in the kernel.

* Thu May 18 2006 Dan Walsh <dwalsh@redhat.com> 1.12.11-1
- Upgrade to latest from NSA
  * Merged patch to initialize sym_val_to_name arrays from Kevin Carr.
    Reworked to use calloc in the first place, and converted some other
    malloc/memset pairs to calloc calls.

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 1.12.10-1
- Upgrade to latest from NSA
  * Merged patch to revert role/user decl upgrade from Karl MacMillan.

* Thu May 11 2006 Steve Grubb <sgrubb@redhat.com> 1.12.9
- Couple minor spec file clean ups

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 1.12.9-1
- Upgrade to latest from NSA
  * Dropped tests from all Makefile target.
  * Merged fix warnings patch from Karl MacMillan.
  * Merged libsepol test framework patch from Karl MacMillan.

* Mon May 1 2006 Dan Walsh <dwalsh@redhat.com> 1.12.6-1
- Upgrade to latest from NSA
  * Fixed cond_normalize to traverse the entire cond list at link time.

* Wed Apr 5 2006 Dan Walsh <dwalsh@redhat.com> 1.12.5-1
- Upgrade to latest from NSA
  * Merged fix for leak of optional package sections from Ivan Gyurdiev.

* Wed Mar 29 2006 Dan Walsh <dwalsh@redhat.com> 1.12.4-1
- Upgrade to latest from NSA
  * Generalize test for bitmap overflow in ebitmap_set_bit.

* Mon Mar 27 2006 Dan Walsh <dwalsh@redhat.com> 1.12.3-1
- Upgrade to latest from NSA
  * Fixed attr_convert_callback and expand_convert_type_set
    typemap bug.

* Fri Mar 24 2006 Dan Walsh <dwalsh@redhat.com> 1.12.2-1
- Upgrade to latest from NSA
  * Fixed avrule_block_write num_decls endian bug.

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> 1.12.1-1
- Upgrade to latest from NSA
  * Fixed sepol_module_package_write buffer overflow bug.

* Fri Mar 10 2006 Dan Walsh <dwalsh@redhat.com> 1.12-2
- Upgrade to latest from NSA
  * Updated version for release.
  * Merged cond_evaluate_expr fix from Serge Hallyn (IBM).
  * Fixed bug in copy_avrule_list reported by Ivan Gyurdiev.
  * Merged sepol_policydb_mls_enabled interface and error handling
    changes from Ivan Gyurdiev.

* Mon Feb 20 2006 Dan Walsh <dwalsh@redhat.com> 1.11.18-2
- Rebuild for fc5-head

* Fri Feb 17 2006 Dan Walsh <dwalsh@redhat.com> 1.11.18-1
- Upgrade to latest from NSA
  * Merged node_expand_addr bugfix and node_compare* change from
    Ivan Gyurdiev.

* Thu Feb 16 2006 Dan Walsh <dwalsh@redhat.com> 1.11.17-1
- Upgrade to latest from NSA
  * Merged nodes, ports: always prepend patch from Ivan Gyurdiev.
  * Merged bug fix patch from Ivan Gyurdiev.
  * Added a defined flag to level_datum_t for use by checkpolicy.
  * Merged nodecon support patch from Ivan Gyurdiev.
  * Merged cleanups patch from Ivan Gyurdiev.  

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> 1.11.14-2
- Fix post install not to fire if /dev/initctr does not exist

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> 1.11.14-1
- Upgrade to latest from NSA
  * Merged optionals in base patch from Joshua Brindle.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.11.13-1.1
- bump again for double-long bug on ppc(64)

* Tue Feb 7 2006 Dan Walsh <dwalsh@redhat.com> 1.11.13-1
- Upgrade to latest from NSA
  * Merged seuser/user_extra support patch from Joshua Brindle.
  * Merged fix patch from Ivan Gyurdiev.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.11.12-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 2 2006 Dan Walsh <dwalsh@redhat.com> 1.11.12-1
- Upgrade to latest from NSA
  * Merged assertion copying bugfix from Joshua Brindle.
  * Merged sepol_av_to_string patch from Joshua Brindle.
  * Merged clone record on set_con patch from Ivan Gyurdiev.  

* Mon Jan 30 2006 Dan Walsh <dwalsh@redhat.com> 1.11.10-1
- Upgrade to latest from NSA
  * Merged cond_expr mapping and package section count bug fixes
    from Joshua Brindle.
  * Merged improve port/fcontext API patch from Ivan Gyurdiev.  
  * Merged fixes for overflow bugs on 64-bit from Ivan Gyurdiev.

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.11.9-1
- Upgrade to latest from NSA
  * Merged size_t -> unsigned int patch from Ivan Gyurdiev.

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 1.11.8-1
- Upgrade to latest from NSA
  * Merged 2nd const in APIs patch from Ivan Gyurdiev.

* Fri Jan 6 2006 Dan Walsh <dwalsh@redhat.com> 1.11.7-1
- Upgrade to latest from NSA
  * Merged const in APIs patch from Ivan Gyurdiev.
  * Merged compare2 function patch from Ivan Gyurdiev.
  * Fixed hierarchy checker to only check allow rules.

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.11.5-1
- Upgrade to latest from NSA
  * Merged further fixes from Russell Coker, specifically:
    - av_to_string overflow checking
    - sepol_context_to_string error handling
    - hierarchy checking memory leak fixes and optimizations
    - avrule_block_read variable initialization
  * Marked deprecated code in genbools and genusers.

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.11.4-1
- Upgrade to latest from NSA
  * Merged bugfix for sepol_port_modify from Russell Coker.
  * Fixed bug in sepol_iface_modify error path noted by Ivan Gyurdiev.
  * Merged port ordering patch from Ivan Gyurdiev.

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 1.11.2-2
- Upgrade to latest from NSA
  * Merged patch series from Ivan Gyurdiev.
    This includes patches to:
    - support ordering of records in compare function
    - enable port interfaces
    - add interfaces for context validity and range checks
    - add include guards

* Tue Dec 27 2005 Dan Walsh <dwalsh@redhat.com> 1.11.1-2
- Add Ivans patch to make ports work

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 1.11.1-1
- Upgrade to latest from NSA
  * Fixed mls_range_cpy bug.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec 7 2005 Dan Walsh <dwalsh@redhat.com> 1.10-1
- Upgrade to latest from NSA

* Mon Dec 5 2005 Dan Walsh <dwalsh@redhat.com> 1.9.42-1
- Upgrade to latest from NSA
  * Dropped handle from user_del_role interface.  

* Mon Nov 28 2005 Dan Walsh <dwalsh@redhat.com> 1.9.41-1
- Upgrade to latest from NSA
  * Merged remove defrole from sepol patch from Ivan Gyurdiev.

* Wed Nov 16 2005 Dan Walsh <dwalsh@redhat.com> 1.9.40-1
- Upgrade to latest from NSA
  * Merged module function and map file cleanup from Ivan Gyurdiev.
  * Merged MLS and genusers cleanups from Ivan Gyurdiev.

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 1.9.39-1
- Upgrade to latest from NSA
  Prepare for removal of booleans* and *.users files.
  * Cleaned up sepol_genbools to not regenerate the image if
    there were no changes in the boolean values, including the
    degenerate case where there are no booleans or booleans.local
    files.
  * Cleaned up sepol_genusers to not warn on missing local.users.
  
* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.9.38-1
- Upgrade to latest from NSA
  * Removed sepol_port_* from libsepol.map, as the port interfaces
    are not yet stable.

* Mon Nov 7 2005 Dan Walsh <dwalsh@redhat.com> 1.9.37-1
- Upgrade to latest from NSA
  * Merged context destroy cleanup patch from Ivan Gyurdiev.

* Thu Nov 3 2005 Dan Walsh <dwalsh@redhat.com> 1.9.36-1
- Upgrade to latest from NSA
  * Merged context_to_string interface change patch from Ivan Gyurdiev.

* Thu Nov 3 2005 Dan Walsh <dwalsh@redhat.com> 1.9.35-1
- Upgrade to latest from NSA
  * Added src/dso.h and src/*_internal.h.
    Added hidden_def for exported symbols used within libsepol.
    Added hidden for symbols that should not be exported by
    the wildcards in libsepol.map.

* Mon Oct 31 2005 Dan Walsh <dwalsh@redhat.com> 1.9.34-1
- Upgrade to latest from NSA
  * Merged record interface, record bugfix, and set_roles patches 
    from Ivan Gyurdiev.

* Fri Oct 28 2005 Dan Walsh <dwalsh@redhat.com> 1.9.33-1
- Upgrade to latest from NSA
  * Merged count specification change from Ivan Gyurdiev.  

* Wed Oct 26 2005 Dan Walsh <dwalsh@redhat.com> 1.9.32-1
- Upgrade to latest from NSA
  * Added further checking and error reporting to 
    sepol_module_package_read and _info.
  * Merged sepol handle passing, DEBUG conversion, and memory leak
    fix patches from Ivan Gyurdiev.

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.9.30-1
- Upgrade to latest from NSA
  * Removed processing of system.users from sepol_genusers and
    dropped delusers logic.
  * Removed policydb_destroy from error path of policydb_read,
    since create/init/destroy/free of policydb is handled by the
    caller now.
  * Fixed sepol_module_package_read to handle a failed policydb_read
    properly.
  * Merged query/exists and count patches from Ivan Gyurdiev.
  * Merged fix for pruned types in expand code from Joshua Brindle.
  * Merged new module package format code from Joshua Brindle.


* Mon Oct 24 2005 Dan Walsh <dwalsh@redhat.com> 1.9.26-1
- Upgrade to latest from NSA
  * Merged context interface cleanup, record conversion code, 
    key passing, and bug fix patches from Ivan Gyurdiev.               

* Fri Oct 21 2005 Dan Walsh <dwalsh@redhat.com> 1.9.25-1
- Upgrade to latest from NSA
  * Merged users cleanup patch from Ivan Gyurdiev.
  * Merged user record memory leak fix from Ivan Gyurdiev.
  * Merged reorganize users patch from Ivan Gyurdiev.

- Need to check for /sbin/telinit

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.9.23-1
- Upgrade to latest from NSA
  * Added check flag to expand_module() to control assertion
    and hierarchy checking on expansion.
  * Reworked check_assertions() and hierarchy_check_constraints()
    to take handles and use callback-based error reporting.
  * Changed expand_module() to call check_assertions() and 
    hierarchy_check_constraints() prior to returning the expanded
    policy.

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.9.21-1
- Upgrade to latest from NSA
  * Changed sepol_module_package_set_file_contexts to copy the
    file contexts data since it is internally managed.
  * Added sepol_policy_file_set_handle interface to associate
    a handle with a policy file.
  * Added handle argument to policydb_from_image/to_image.
  * Added sepol_module_package_set_file_contexts interface.
  * Dropped sepol_module_package_create_file interface.
  * Reworked policydb_read/write, policydb_from_image/to_image, 
    and sepol_module_package_read/write to use callback-based error
    reporting system rather than DEBUG.  

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.9.19-1
- Upgrade to latest from NSA
  * Reworked link_packages, link_modules, and expand_module to use
  callback-based error reporting system rather than error buffering.

* Sat Oct 15 2005 Dan Walsh <dwalsh@redhat.com> 1.9.18-1
- Upgrade to latest from NSA
  * Merged conditional expression mapping fix in the module linking
  code from Joshua Brindle.

* Fri Oct 14 2005 Dan Walsh <dwalsh@redhat.com> 1.9.17-2
- Tell init to reexec itself in post script

* Mon Oct 10 2005 Dan Walsh <dwalsh@redhat.com> 1.9.17-1
- Upgrade to latest from NSA
  * Hid sepol_module_package type definition, and added get interfaces.
  * Merged new callback-based error reporting system from Ivan
  Gyurdiev.
  * Merged support for require blocks inside conditionals from
  Joshua Brindle (Tresys).

* Mon Oct 10 2005 Dan Walsh <dwalsh@redhat.com> 1.9.14.1-1
- Upgrade to latest from NSA
  * Fixed use of policydb_from_image/to_image to ensure proper
  init of policydb.
  * Isolated policydb internal headers under <sepol/policydb/*.h>.
  These headers should only be used by users of the static libsepol.
  Created new <sepol/policydb.h> with new public types and interfaces
  for shared libsepol.
  Created new <sepol/module.h> with public types and interfaces moved
  or wrapped from old module.h, link.h, and expand.h, adjusted for
  new public types for policydb and policy_file.
  Added public interfaces to libsepol.map.
  Some implementation changes visible to users of the static libsepol:
  1) policydb_read no longer calls policydb_init.
  Caller must do so first.
  2) policydb_init no longer takes policy_type argument.
  Caller must set policy_type separately.
  3) expand_module automatically enables the global branch.  
  Caller no longer needs to do so.
  4) policydb_write uses the policy_type and policyvers from the 
  policydb itself, and sepol_set_policyvers() has been removed.

* Fri Oct 7 2005 Dan Walsh <dwalsh@redhat.com> 1.9.12-1
- Upgrade to latest from NSA
  * Merged function renaming and static cleanup from Ivan Gyurdiev.

* Thu Oct 6 2005 Dan Walsh <dwalsh@redhat.com> 1.9.11-1
- Upgrade to latest from NSA
  * Merged bug fix for check_assertions handling of no assertions
  from Joshua Brindle (Tresys).
  
* Tue Oct 4 2005 Dan Walsh <dwalsh@redhat.com> 1.9.10-1
- Upgrade to latest from NSA
  * Merged iterate patch from Ivan Gyurdiev.
  * Merged MLS in modules patch from Joshua Brindle (Tresys).

* Mon Oct 3 2005 Dan Walsh <dwalsh@redhat.com> 1.9.8-1
- Upgrade to latest from NSA
  * Merged pointer typedef elimination patch from Ivan Gyurdiev.
  * Merged user list function, new mls functions, and bugfix patch
    from Ivan Gyurdiev.

* Wed Sep 28 2005 Dan Walsh <dwalsh@redhat.com> 1.9.7-1
- Upgrade to latest from NSA
  * Merged sepol_get_num_roles fix from Karl MacMillan (Tresys).

* Fri Sep 23 2005 Dan Walsh <dwalsh@redhat.com> 1.9.6-1
- Upgrade to latest from NSA
  * Merged bug fix patches from Joshua Brindle (Tresys).

* Wed Sep 21 2005 Dan Walsh <dwalsh@redhat.com> 1.9.5-1
- Upgrade to latest from NSA
  * Merged boolean record and memory leak fix patches from Ivan
  Gyurdiev.

* Tue Sep 20 2005 Dan Walsh <dwalsh@redhat.com> 1.9.4-1
- Upgrade to latest from NSA
  * Merged interface record patch from Ivan Gyurdiev.

* Thu Sep 15 2005 Dan Walsh <dwalsh@redhat.com> 1.9.3-1
- Upgrade to latest from NSA
  * Merged fix for sepol_enable/disable_debug from Ivan
  Gyurdiev.

* Wed Sep 14 2005 Dan Walsh <dwalsh@redhat.com> 1.9.1-2
- Upgrade to latest from NSA
  * Merged stddef.h patch and debug conversion patch from 
  Ivan Gyurdiev.

* Mon Sep 12 2005 Dan Walsh <dwalsh@redhat.com> 1.9.1-1
- Upgrade to latest from NSA
  * Fixed expand_avtab and expand_cond_av_list to keep separate
  entries with identical keys but different enabled flags.
  * Updated version for release.

* Thu Sep 1 2005 Dan Walsh <dwalsh@redhat.com> 1.7.24-1
- Upgrade to latest from NSA
  * Fixed symtab_insert return value for duplicate declarations.
  * Merged fix for memory error in policy_module_destroy from
  Jason Tang (Tresys).

* Mon Aug 29 2005 Dan Walsh <dwalsh@redhat.com> 1.7.22-1
- Upgrade to latest from NSA
  * Merged fix for memory leak in sepol_context_to_sid from
  Jason Tang (Tresys).
  * Merged fixes for resource leaks on error paths and
    change to scope_destroy from Joshua Brindle (Tresys).

* Tue Aug 23 2005 Dan Walsh <dwalsh@redhat.com> 1.7.20-1
- Upgrade to latest from NSA
  * Merged more fixes for resource leaks on error paths 
    from Serge Hallyn (IBM).  Bugs found by Coverity. 

* Fri Aug 19 2005 Dan Walsh <dwalsh@redhat.com> 1.7.19-1
- Upgrade to latest from NSA
  * Changed to treat all type conflicts as fatal errors.
  * Merged several error handling fixes from 
    Serge Hallyn (IBM).  Bugs found by Coverity.  

* Mon Aug 15 2005 Dan Walsh <dwalsh@redhat.com> 1.7.17-1
- Upgrade to latest from NSA
  * Fixed several memory leaks found by valgrind.

* Sun Aug 14 2005 Dan Walsh <dwalsh@redhat.com> 1.7.15-1
- Upgrade to latest from NSA
  * Fixed empty list test in cond_write_av_list.  Bug found by
    Coverity, reported by Serge Hallyn (IBM).
  * Merged patch to policydb_write to check errors 
    when writing the type->attribute reverse map from
    Serge Hallyn (IBM).  Bug found by Coverity.
  * Fixed policydb_destroy to properly handle NULL type_attr_map
    or attr_type_map.

* Sat Aug 13 2005 Dan Walsh <dwalsh@redhat.com> 1.7.14-1
- Upgrade to latest from NSA
  * Fixed empty list test in cond_write_av_list.  Bug found by
    Coverity, reported by Serge Hallyn (IBM).
  * Merged patch to policydb_write to check errors 
    when writing the type->attribute reverse map from
    Serge Hallyn (IBM).  Bug found by Coverity.
  * Fixed policydb_destroy to properly handle NULL type_attr_map
    or attr_type_map.


* Thu Aug 11 2005 Dan Walsh <dwalsh@redhat.com> 1.7.13-1
- Upgrade to latest from NSA
  * Improved memory use by SELinux by both reducing the avtab 
    node size and reducing the number of avtab nodes (by not
    expanding attributes in TE rules when possible).  Added
    expand_avtab and expand_cond_av_list functions for use by
    assertion checker, hierarchy checker, compatibility code,
    and dispol.  Added new inline ebitmap operators and converted
    existing users of ebitmaps to the new operators for greater 
    efficiency.
    Note:  The binary policy format version has been incremented to 
    version 20 as a result of these changes.

* Thu Aug 11 2005 Dan Walsh <dwalsh@redhat.com> 1.7.12-1
- Upgrade to latest from NSA
  * Fixed bug in constraint_node_clone handling of name sets.

* Wed Aug 10 2005 Dan Walsh <dwalsh@redhat.com> 1.7.11-1
- Upgrade to latest from NSA
  * Fix range_trans_clone to map the type values properly.

* Fri Aug 5 2005 Dan Walsh <dwalsh@redhat.com> 1.7.10-1
- Upgrade to latest from NSA
  * Merged patch to move module read/write code from libsemanage
    to libsepol from Jason Tang (Tresys).

* Tue Aug 2 2005 Dan Walsh <dwalsh@redhat.com> 1.7.9-1
- Upgrade to latest from NSA
  * Enabled further compiler warning flags and fixed them.
  * Merged user, context, port records patch from Ivan Gyurdiev.
  * Merged key extract function patch from Ivan Gyurdiev.
  * Merged mls_context_to_sid bugfix from Ivan Gyurdiev.

* Wed Jul 27 2005 Dan Walsh <dwalsh@redhat.com> 1.7.6-2
- Fix MLS Free 

* Mon Jul 25 2005 Dan Walsh <dwalsh@redhat.com> 1.7.6-1
- Upgrade to latest from NSA
  * Merged context reorganization, memory leak fixes, 
    port and interface loading, replacements for genusers and
    genbools, debug traceback, and bugfix patches from Ivan Gyurdiev.
  * Merged uninitialized variable bugfix from Dan Walsh.

* Mon Jul 25 2005 Dan Walsh <dwalsh@redhat.com> 1.7.5-2
- Fix unitialized variable problem

* Mon Jul 18 2005 Dan Walsh <dwalsh@redhat.com> 1.7.5-1
- Upgrade to latest from NSA
  * Merged debug support, policydb conversion functions from Ivan Gyurdiev (Red Hat).
  * Removed genpolbools and genpolusers utilities.
  * Merged hierarchy check fix from Joshua Brindle (Tresys).



* Thu Jul 14 2005 Dan Walsh <dwalsh@redhat.com> 1.7.3-1
- Upgrade to latest from NSA
  * Merged header file cleanup and memory leak fix from Ivan Gyurdiev (Red Hat).
  * Merged genbools debugging message cleanup from Red Hat.

* Thu Jul 7 2005 Dan Walsh <dwalsh@redhat.com> 1.7-2
- Remove genpolbools and genpoluser 

* Thu Jul 7 2005 Dan Walsh <dwalsh@redhat.com> 1.7-1
- Upgrade to latest from NSA
  * Merged loadable module support from Tresys Technology.

* Wed Jun 29 2005 Dan Walsh <dwalsh@redhat.com> 1.6-1
- Upgrade to latest from NSA
  * Updated version for release.

* Tue May 17 2005 Dan Walsh <dwalsh@redhat.com> 1.5.10-1
- Fix reset booleans warning message
- Upgrade to latest from NSA
  * License changed to LGPL v2.1, see COPYING.

* Tue May 17 2005 Dan Walsh <dwalsh@redhat.com> 1.5.9-2
- Upgrade to latest from NSA
  * Added sepol_genbools_policydb and sepol_genusers_policydb for
    audit2why.

* Mon May 16 2005 Dan Walsh <dwalsh@redhat.com> 1.5.8-2
- export sepol_context_to_sid

* Mon May 16 2005 Dan Walsh <dwalsh@redhat.com> 1.5.8-1
- Upgrade to latest from NSA
  * Added sepol_ prefix to Flask types to avoid 
    namespace collision with libselinux.

* Fri May 13 2005 Dan Walsh <dwalsh@redhat.com> 1.5.7-1
- Upgrade to latest from NSA
  * Added sepol_compute_av_reason() for audit2why.

* Tue Apr 26 2005 Dan Walsh <dwalsh@redhat.com> 1.5.6-1
- Upgrade to latest from NSA
  * Fixed bug in role hierarchy checker.

* Mon Apr 25 2005 Dan Walsh <dwalsh@redhat.com> 1.5.5-2
- Fixes found via intel compiler

* Thu Apr 14 2005 Dan Walsh <dwalsh@redhat.com> 1.5.5-1
- Update from NSA

* Tue Mar 29 2005 Dan Walsh <dwalsh@redhat.com> 1.5.3-1
- Update from NSA

* Thu Mar 24 2005 Dan Walsh <dwalsh@redhat.com> 1.5.2-2
- Handle booleans.local

* Thu Mar 17 2005 Dan Walsh <dwalsh@redhat.com> 1.5.2-1
- Update to latest from NSA
  * Added man page for sepol_check_context.
  * Added man page for sepol_genusers function.
  * Merged man pages for genpolusers and chkcon from Manoj Srivastava.

* Thu Mar 10 2005 Dan Walsh <dwalsh@redhat.com> 1.4-1
- Update to latest from NSA

* Tue Mar 8 2005 Dan Walsh <dwalsh@redhat.com> 1.3.8-1
- Update to latest from NSA
        * Cleaned up error handling in sepol_genusers and sepol_genbools.

* Tue Mar 1 2005 Dan Walsh <dwalsh@redhat.com> 1.3.7-1
- Update to latest from NSA
  * Merged sepol_debug and fclose patch from Dan Walsh.

* Fri Feb 18 2005 Dan Walsh <dwalsh@redhat.com> 1.3.6-3
- Make sure local_files file pointer is closed
- Stop outputing error messages

* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.3.6-1
- Update to latest from NSA
  * Changed sepol_genusers to also use getline and correctly handle
    EOL.
* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.3.5-1
- Update to latest from NSA
  * Merged endianness and compute_av patches from Darrel Goeddel (TCS).
  * Merged range_transition support from Darrel Goeddel (TCS).
  * Added sepol_genusers function.

* Thu Feb 10 2005 Dan Walsh <dwalsh@redhat.com> 1.3.2-1
- Update to latest from NSA
  * Changed relabel Makefile target to use restorecon.

* Mon Feb 7 2005 Dan Walsh <dwalsh@redhat.com> 1.3.1-1
- Update to latest from NSA
  * Merged enhanced MLS support from Darrel Goeddel (TCS).

* Thu Jan 20 2005 Dan Walsh <dwalsh@redhat.com> 1.2.1.1-1
- Update to latest from NSA
  * Merged build fix patch from Manoj Srivastava.

* Thu Nov 4 2004 Dan Walsh <dwalsh@redhat.com> 1.2.1-1
- Update to latest from NSA

* Mon Aug 30 2004 Dan Walsh <dwalsh@redhat.com> 1.1.1-2
- Add optargs for build

* Sun Aug 22 2004 Dan Walsh <dwalsh@redhat.com> 1.1.1-1
- New version from NSA

* Fri Aug 20 2004 Colin Walters <walters@redhat.com> 1.0-2
- Apply Stephen's chkcon patch

* Thu Aug 19 2004 Colin Walters <walters@redhat.com> 1.0-1
- New upstream version

* Mon Aug 16 2004 Dan Walsh <dwalsh@redhat.com> 0.4.2-1
- Newversion from upstream implementing stringcase compare

* Fri Aug 13 2004 Bill Nottingham <notting@redhat.com> 0.4.1-2
- ldconfig tweaks

* Thu Aug 12 2004 Dan Walsh <dwalsh@redhat.com> 0.4.1-1
- Ignore case of true/false

* Wed Aug 11 2004 Dan Walsh <dwalsh@redhat.com> 0.4.1-1
- New version from NSA

* Tue Aug 10 2004 Dan Walsh <dwalsh@redhat.com> 0.3.1-1
- Initial version
- Created by Stephen Smalley <sds@epoch.ncsc.mil> 


