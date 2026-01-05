# Spec-Driven Development (SDD): A Master Guide

## 1. What is Spec-Driven Development?

**Spec-Driven Development (SDD)** is an engineering methodology where you define the **entire behavior and interface** of a system in a machine-readable, human-understandable "Spec" *before* writing a single line of implementation logic.

Unlike traditional requirements documents which are "dead text," an SDD Spec is a **living artifact**. It serves as:
1.  **The Blueprint**: For the engineer (or AI agent) to build.
2.  **The Law**: For the validator to test against.
3.  **The Documentation**: For the consumer to understand.

### The Golden Rule of SDD
> "If it's not in the Spec, it doesn't exist. If the code implies it but the Spec doesn't, the code is wrong (or the Spec is outdated)."

---

## 2. SDD vs. The World

How does this differ from what you already know?

### vs. Test-Driven Development (TDD)
*   **TDD**: Write a failing test -> Write code to fix it -> Refactor.
    *   *Focus*: Code correctness and design at the function/unit level.
    *   *Gap*: TDD doesn't inherently describe *why* or the *holistic architecture*. It's often "bottom-up."
*   **SDD**: Write the interface/behavior spec -> Generate/Write Tests + Code -> Verify.
    *   *Focus*: System behavior, contracts, and boundaries. "Top-down."
    *   *Diff*: In SDD, you might **generate** your TDD tests *from* the Spec.

### vs. Documentation-Driven Development
*   **Doc code**: Write a README or design doc -> Write code.
    *   *Focus*: Communication.
    *   *Gap*: Docs drift. Code changes, docs rot. There is no automated link.
*   **SDD**: The Spec *is* the build input.
    *   *Diff*: If you change the Spec, your validation suite breaks immediately. You cannot drift.

### vs. Prompt-Only Workflows (The Agentic Trap)
*   **Prompt-Only**: "Hey Claude, build me a CI pipeline for Node.js."
    *   *Risk*: Ambiguity. The LLM hallucinates assumptions. Results are flaky. Hard to iterate deterministically.
*   **SDD**: "Here is the `pipeline.spec.yaml` defining stages, triggers, and artifacts. Implement this exact contract."
    *   *Win*: Constrained search space. Deterministic validation. You treat the AI as a "Transpiler" (Spec -> Code), not a "Designer."

---

## 3. Core Artifacts of SDD

To practice SDD, you need three distinct elements:

1.  **The Spec (The "What")**
    *   *Format*: YAML, JSON, CUE, or strictly structured Markdown.
    *   *Content*: Interfaces, data shapes, error states, constraints, config values.
    *   *Example*: OpenApi (Swagger) is the classic HTTP API spec. Terraform Modules are Infrastructure specs.

2.  **The Implementation (The "How")**
    *   *Format*: Python, Go, Terraform HCL, Dockerfile.
    *   *Role*: It is purely a servant to the spec. It has no "personality" outside what the spec allows.

3.  **The Validator (The "Judge")**
    *   *Format*: Test suite, Policy-as-Code (OPA/Sentinel), Linter.
    *   *Role*: It reads the *Spec* and checks the *Implementation*.
    *   *Crucial*: The validator does *not* read the implementation logic; it tests behavior against the Spec.

---

## 4. The Agentic SDD Workflow

This is where you, as an AI Engineer, gain superpowers. Agents excel at translating structured constraints into code.

### The Loop
1.  **Draft**: You (Human) write the high-level `feature.spec.yaml`.
2.  **Critique**: You ask an AI Agent: "Review this spec for edge cases or security holes."
3.  **Refine**: Update the Spec.
4.  **Generate**: You give the Spec to an Agent: "Implement this. Do not deviate."
5.  **Verify**: You run the auto-generated validation suite.
6.  **Iterate**: If tests fail, you fix the code (or spec).

### Why Agents Love Specs
*   **Context Window Efficiency**: A dense YAML spec is token-efficient compared to 10 pages of prose.
*   **Reduced Hallucination**: The "Ground Truth" is explicit.
*   **Self-Correction**: If the Agent creates code that fails the Spec validation, it can read the error and try again autonomously.

---

## 5. Failure Modes (Avoid These)

*   **The "Shadow Spec"**: You have a spec, but you add "just one little thing" in the code that isn't in the spec. *Result*: Drift. Trust is lost.
*   **The "Vague Spec"**: "Field: `data` (string)". *Result*: Interpretation varies. Be specific: "Field: `data` (base64 encoded json string, max 1MB)."
*   **Spec-as-Code coupling**: Writing the spec *in* the language of the implementation (e.g., using Python decorators as the only source of truth). This binds you to the language. Keep data (YAML) separate from logic (Python).

---
*Next, we will apply this to a real CI/CD pipeline.*
