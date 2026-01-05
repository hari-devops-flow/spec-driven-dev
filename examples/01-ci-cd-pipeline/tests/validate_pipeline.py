
# tests/validate_pipeline.py
import yaml
import sys

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def validate(spec_path, impl_path):
    print(f"🔍 Validating {impl_path} against {spec_path}...")
    spec = load_yaml(spec_path)
    impl = load_yaml(impl_path)
    
    errors = []

    # 1. Validate Stages presence
    spec_stage_ids = {s['id'] for s in spec['stages']}
    impl_stages = {s['stage'] for s in impl['stages']}
    
    # Note: Azure Pipelines implementation might map ids differently, but for this demo 
    # we enforce 1:1 mapping for simplicity.
    if not spec_stage_ids.issubset(impl_stages):
        missing = spec_stage_ids - impl_stages
        errors.append(f"Missing stages in implementation: {missing}")

    # 2. Validate Triggers
    spec_push_branches = set(spec['triggers']['push']['branches'])
    impl_trigger_branches = set(impl['trigger']['branches']['include'])
    
    if spec_push_branches != impl_trigger_branches:
        errors.append(f"Trigger mismatch! Spec says {spec_push_branches}, Impl has {impl_trigger_branches}")

    # 3. Validate Critical Jobs
    # Checking if 'docker_build' exists in build_push stage
    spec_build_stage = next(s for s in spec['stages'] if s['id'] == 'build_push')
    impl_build_stage = next(s for s in impl['stages'] if s['stage'] == 'build_push')
    
    spec_jobs = {j['name'] for j in spec_build_stage['jobs']}
    impl_jobs = {j['job'] for j in impl_build_stage['jobs']}
    
    if not spec_jobs.issubset(impl_jobs):
         errors.append(f"Job mismatch in build_push! Spec required {spec_jobs}")

    if errors:
        print("❌ Validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("✅ Validation PASSED: Implementation honors the Spec.")

if __name__ == "__main__":
    validate(
        "../pipeline.spec.yaml",
        "../impl/azure-pipelines.yml"
    )
