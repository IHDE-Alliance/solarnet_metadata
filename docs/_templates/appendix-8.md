(appendix-viii)=
# Appendix VIII. File list glob patterns and sorting

In SOLARNET fits files, keywords used to give comma-separated lists of files may use the shell glob patterns asterisk (\*) matching any number of characters, question mark (?) matching a single character, and character set (e.g., `[ABCx-y]`) matching a single character as specified within the brackets. The files matching the pattern should be sorted in lexicographic order before being interpreted as a list of file names. File lists may also use the relative path notation as specified in [Appendix VII](#appendix-vii).
