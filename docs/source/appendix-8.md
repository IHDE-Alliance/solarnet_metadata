(appendix-viii)=

# <span class=new>Appendix VIII. File list wildcard patterns and sorting</span>

In SOLARNET fits files, keywords used to give comma-separated lists of files (or external extension references) may use the shell wildcards asterisk (*) matching any number of characters, question mark (?) matching a single character, and character set (e.g., `[ABCx-y]`) matching a single character as specified within the brackets (the resulting expressions are often referred to as "glob patterns"). The files matching the pattern should be sorted in lexicographic order before being interpreted as a list of file names. File lists may also use the relative path notation as specified for external extensions in [Appendix VII](#appendix-vii).

<span class=new>Wildcard patterns may also be used for directories in relative paths. E.g., `../../../*/*/*/*9936*.fits` will match against all files starting from three directories above the referencing file. This can be useful to e.g., reference file series spanning multiple days in a `yyyy/mm/dd` directory structure.</span>

<span class=new>Wildcard patterns in relative paths can always be tested by changing working directory to where the referring file is located and then issuing an `ls` command with the relative path listed.</span>
