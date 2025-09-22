---
name: Bug Report
about: Create a report describing unexpected or incorrect behavior in the `solarnet_metadata` package.
title: "[TEXT]"
labels: bug
assignees: ''

---

We know opening issues takes effort, and we appreciate your time.

Please be aware that everyone has to follow our [code of conduct](https://github.com/IHDE-Alliance/solarnet_metadata?tab=coc-ov-file)

Please have a search on our GitHub repository to see if a similar issue has already been posted.
If a similar issue is closed, have a quick look to see if you are satisfied by the resolution.
If not please go ahead and open a new issue!

**Describe the bug you're experiencing**

A clear and concise description of what the bug is.

```
Please include the relevant log output.
```

**How to Reproduce**

Please include code that reproduces the issue whenever possible. The best reproductions are self-contained scripts with minimal dependencies.

```
Sample code to reproduce the problem
```

**Screenshots**

```
If applicable, add screenshots to help explain your problem.
```

**System Details**

You can run the following and paste the result in a code block. 
This will help us identify your environment.

```
import platform
import sys
import astropy
import solarnet_metadata

print(platform.platform())
print(sys.version_info)
print('astropy={0}'.format(astropy.__version__))
print('solarnet_metadata={0}'.format(solarnet_metadata.__version__))
```
