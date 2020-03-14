# Firefox profiles

- There appear to be 3 ways the active Firefox profile is stored on a standard installation:
  - `installs.ini` -> only section -> key: 'Default'
  - `profiles.ini` -> only section name beginning with 'Install' -> key: 'Default'
  - `profiles.ini` -> section name beginning with 'Profile0' -> key: 'Path'
- Each of these stores the 'shortcode' or 'hash' unique to the Firefox profile.

As I understand it, the `installs.ini` file stores the installation-specific profile name,
and this "is used to lock a specific Firefox installation against a (dedicated) profile"
([source](http://forums.mozillazine.org/viewtopic.php?f=38&t=3055517)),
in other words the key value `Locked=1` means that the installation is locked to this profile.

The same section is found in the `profiles.ini` file, but the section name is prefixed with
the word 'Install', then the installation hash matching the section name in `installs.ini`.

The second way the default profile is stored is more ambiguous.

There are two entry titles beginning with 'Profile', and I think the way Firefox chooses
between them was previously to use the 'StartWithLastProfile' value but this was
[replaced](https://support.mozilla.org/en-US/kb/dedicated-profiles-firefox-installation#w_what-profile-changes-were-made-in-firefox-67)
(as of Firefox 67) with 'dedicated' profiles for each installation.

So basically, there's no need to deal with the latter, and to just use the profile name
belonging to the installation (either by reading `installs.ini` or the corresponding
entry in `profiles.ini`). I haven't got multiple installations on my PC, so I can't
make any guesses at how these are handled (and I won't try to work with them in pyx-sys).
