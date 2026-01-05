# Feature Specification: [Feature Name]

## 1. Overview
**Goal**: [One sentence summary]
**User Story**: As a [role], I want [action], so that [benefit].

## 2. Functional Requirements (The Contract)

### 2.1 Inputs
- **Field A**: [Type, constraints, example]
- **Field B**: [Type, constraints, example]

### 2.2 Logic & Behavior
- *Given* [condition]
- *When* [event]
- *Then* [result]

### 2.3 Outputs (API Response / UI State)
```json
{
  "status": "success",
  "data": { ... }
}
```

## 3. Constraints & Non-Functional
- **Performance**: Must respond in < 200ms.
- **Security**: Must validate X-Auth-Token.
- **Compatibility**: Mobile and Desktop.

## 4. Edge Cases
- [ ] What if network fails?
- [ ] What if input is empty?
