.. _version_guidelines:

Version Guidelines for SOLARNET Metadata Recommendations
--------------------------------------------------------

Purpose
~~~~~~~

This document outlines the versioning strategy for the SOLARNET Metadata Recommendations project, encompassing both the documentation and the associated Python package code. The goal is to maintain a unified versioning system that reflects changes in both components, ensuring clarity and consistency for users and developers.

Versioning Approach
~~~~~~~~~~~~~~~~~~~

The SOLARNET Metadata Recommendations project adopts a single version number to encapsulate both the documentation and the Python package code. This unified versioning ensures that updates to either the documentation or the code are reflected in a single, cohesive version number, facilitating synchronized development and communication.

The process for updating the SOLARNET Metadata Recommendations and the associated Python package involves the following steps:

1. **Suggest New Keywords or Clarifications**: Community members or developers propose new metadata keywords or clarifications to existing ones.
2. **Develop Documentation and Code Updates**: The development team iteratively updates both the documentation and the code to incorporate the suggestions.
3. **Merge Updates into Main Branch**: Once the updates are ready, they are merged into the main branch via a merge request.
4. **Determine Version Increment**: Based on the nature of the changes, the appropriate version increment (MAJOR, MINOR, or PATCH) is determined according to the Version Increment Rules.
5. **Create Release and Notify Stakeholders**: A new release is generated with the updated version number, and stakeholders are notified of the changes.

.. graphviz::

   digraph {
        layout=neato;
        node [shape=box, style=rounded, width=2, height=1, fixedsize=true];
        
        A [label="Suggest New\nKeywords or\nClarifications", pos="0,2!"];
        B [label="Develop\nDocumentation and\nCode Updates", pos="1.9,0.6!"];
        C [label="Merge Updates to\nMain Branch", pos="1.2,-1.6!"];
        D [label="Determine Version\nIncrement", pos="-1.2,-1.6!"];
        E [label="Create Release &\nNotify Stakeholders", pos="-1.9,0.6!"];
        
        A -> B;
        B -> C;
        C -> D;
        D -> E;
        E -> A;
        B -> B [constraint=false];
    }

This structured approach ensures that both the documentation and the code remain synchronized and that all changes are properly versioned and communicated.

Semantic Versioning
^^^^^^^^^^^^^^^^^^^

The project follows `Semantic Versioning (SemVer) <https://semver.org/>`_ principles, using the format ``MAJOR.MINOR.PATCH``:

- **MAJOR**: Incremented for significant changes or breaking updates to either the documentation or the code that may impact the user API or fundamentally alter the metadata recommendations.
- **MINOR**: Incremented for non-breaking improvements, such as new features in the code or substantial updates to the documentation (e.g., new sections or significant clarifications).
- **PATCH**: Incremented for minor changes, such as bug fixes in the code or small edits to the documentation (e.g., typo corrections, improved readability, or content reorganization).

Synchronized Updates
^^^^^^^^^^^^^^^^^^^^

Updates to the documentation should ideally correspond with updates to the code, and vice versa, to maintain consistency. For example:

- If a breaking code change is introduced, relevant code examples or references in the documentation must be updated to reflect this change.
- If the documentation is revised (e.g., to improve clarity or add new recommendations), any necessary adjustments to the code should be made to ensure alignment.

Version Increment Rules
^^^^^^^^^^^^^^^^^^^^^^^

1. **Code Changes**:

   - **Breaking Changes**: Increment the MAJOR version. Examples include changes to the architecture that impact the user API or significant shifts in metadata structure.
   - **Non-Breaking Features**: Increment the MINOR version. Examples include new functionality or enhancements that maintain backward compatibility.
   - **Bug Fixes**: Increment the PATCH version. Examples include fixes that do not alter the API or user-facing behavior.

2. **Documentation Changes**:

   - **Breaking Changes (MAJOR version increment)**:
      - Adding new required keywords that data providers must implement
      - Fundamental changes to keyword semantics or interpretation
      - Changes that require users to modify their existing implementations

   - **Non-Breaking Additions (MINOR version increment)**:
      - Adding new optional keywords
      - Deprecating existing keywords (generally, with possible exceptions for critical keywords)
      - Extending existing keywords (e.g., adding wildcard syntax or expanding allowed values)

   - **Minor Improvements (PATCH version increment)**:
      - Adding new sections with additional guidance or clarification on recommendations
      - Correcting typos or grammatical errors
      - Improving readability of existing content
      - Adding examples that illustrate existing requirements

3. **Combined Changes**:

   - If both code and documentation are updated, the version increment is determined by the most significant change. For example, a breaking code change paired with minor documentation edits results in a MAJOR version increment.

Implementation Notes
~~~~~~~~~~~~~~~~~~~~

- **Git Tags**: Version numbers will be applied as Git tags in the format ``vX.Y.Z`` (e.g., ``v1.0.0``) to mark releases in the repository.
- **Repository Management**: The repository version will be bumped according to the rules above, ensuring that both code and documentation changes are reflected in the version history.
- **Automation**: While automated versioning for documentation changes alone is not currently implemented, manual version bumps will be applied as needed to reflect significant documentation updates.


References
~~~~~~~~~~

- `Semantic Versioning Specification <https://semver.org/>`_
- `SOLARNET Metadata Recommendations Repository <https://github.com/IHDE-Alliance/solarnet_metadata>`_
