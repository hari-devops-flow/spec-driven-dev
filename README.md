# Spec-Driven Development (SDD) Mastery

Welcome to your structured guide on **Spec-Driven Development**. This repository contains theory, examples, and templates to help you master SDD for DevOps and Agentic Engineering.

## 📚 Core Resources

1.  **[The Master Guide](./SDD_GUIDE.md)**: Start here. Understand the "What", "Why", and "How" of SDD, and how it differs from TDD/DDD.
2.  **[Templates](./templates/)**: Reusable files to kickstart your next project.
    *   [Feature Spec](./templates/feature-spec.md)
    *   [Infrastructure Spec](./templates/infra-spec.yaml)
    *   [Agent Prompt](./templates/agent-prompt-spec.md)

## 🛠️ Hands-On Examples

We believe in learning by doing. Examples include a "Spec", an "Implementation", and an "Automated Validator".

### 1. [CI/CD Pipeline](./examples/01-ci-cd-pipeline/)
*   **Spec**: `pipeline.spec.yaml` (The abstract requirement)
*   **Impl**: `impl/azure-pipelines.yml` (The concrete Azure DevOps code)
*   **Validate**: `tests/validate_pipeline.py` (The script ensuring the Impl matches the Spec)

## 🗺️ Learning Roadmap

### Phase 1: The Basics (Now)
- [ ] Read **[SDD_GUIDE.md](./SDD_GUIDE.md)** to understand the philosophy.
- [ ] Run the **[Pipeline Example](./examples/01-ci-cd-pipeline/)** validation script to see SDD in action.
- [ ] Try creating a simple Spec for a small script using the **[Feature Template](./templates/feature-spec.md)**.

### Phase 2: Agentic Workflow
- [ ] Use the **[Agent Prompt](./templates/agent-prompt-spec.md)** to ask an AI to build a new module for you.
- [ ] Challenge the AI: "Update the code." -> *Validation Fails*. -> "Update the Spec first!"

### Phase 3: Advanced
- [ ] Implement a "Spec Generator": Generate your Specs from higher-level requirements using LLMs.
- [ ] Implement "Policy-as-Code": Use OPA to validate your Specs before they even reach implementation.

---
*Created by your AI Pair Programmer.*