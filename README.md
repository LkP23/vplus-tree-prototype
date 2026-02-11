# V+-Tree Prototype (Python)

## Overview
This repository contains a **research prototype** of a **V+-tree (V++-tree)**, an authenticated variant of the B+ tree designed for **verifiable data membership proofs**. The implementation extends a class-based B+ tree in Python to support commitment-ready node structures.

This codebase is intended for **research and paper submission**, not for production use.

---

## Motivation
In practical systems, it is often infeasible to prove the existence of a data item by revealing the entire data structure.  
The V+-tree enables **mathematically verifiable proofs of membership**, allowing a verifier to confirm that a value exists in the tree by checking only a short proof path from the root to a leaf.

The V+-tree combines:
- The **search and insert efficiency** of a B+ tree, and
- **Merkle-style authentication** using commitment-based internal nodes.

---

## Scope of This Repository
The current implementation focuses strictly on the following:

### Included
- Class-based B+ tree implementation
- Insert operation
- Search operation
- Clear distinction between:
  - Leaf nodes (data only)
  - Internal nodes (routing + commitments)
- Extension of node structure with:
  - Left Pointer Commitment (LPC)
  - Right Pointer Commitment (RPC)
  - Control Flag (CP, placeholder)

### Explicitly Excluded (by design)
- Delete operation
- Commitment mathematics (e.g., vector commitments, proof equations)
- Performance optimizations

These exclusions are intentional and align with the research discussion.

---

## Repository Structure
