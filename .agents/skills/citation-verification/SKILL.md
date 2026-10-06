---
name: "citation-verification"
description: "Verify citation metadata and support for manuscript claims during drafting or pre-submission; never invent references."
---

# Citation Verification

Verify each reference as both a bibliographic record and evidence for the sentence that cites it.

1. Read the manuscript, bibliography, and any existing `Evidence ID` records. Build a list of unique citation keys and each location where a specific scientific claim relies on one.
2. Resolve metadata through primary or authoritative scholarly records (for example DOI registration, publisher, conference proceedings, arXiv for its own version, or Research Core). Check title, authors, venue, year, identifier, and the cited version.
3. For a claim-dependent citation, inspect the source itself and record the supporting section, table, figure, or page when available. Metadata alone does not verify that the source supports a claim.
4. Mark every entry `verified`, `metadata-only`, `claim-not-supported`, `unresolved`, `conflicted`, or `replace/remove`. Never infer missing metadata or fabricate a replacement citation.
5. For consequential sources, preserve the canonical identifier and version, retrieval date/route, exact support location, and local artifact/hash when one exists. Obsidian or another note system may link the record, but it does not replace the original source or verification status.
6. Record results in `docs/11_pre_submission_audit.md` under “引文核验”; preserve uncertain entries for author decision.

## Rules

- Prefer the canonical DOI/publisher record for final metadata; record preprint-versus-publication differences explicitly.
- A literature search result, abstract-only record, or citation count can discover a source but cannot substantiate a detailed technical claim.
- Keep discovery, bibliographic verification, lawful full-text acquisition, local parsing, and note storage as distinct provenance steps. Report a missing capability rather than silently changing the evidence route.
- Do not require a particular search engine, citation count, or fixed author-year tolerance.
- Do not edit prose, BibTeX, or claims unless the user separately asks for the correction.
