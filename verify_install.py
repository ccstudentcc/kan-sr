import importlib
import pkg_resources

# Package name and required version
requirements = {
    "numpy": "1.24.4",
    "scipy": "1.11.4",
    "pandas": "2.0.1",
    "matplotlib": "3.7.1",
    "seaborn": "0.13.2",
    "scikit-learn": "1.3.2",
    "tensorflow": "2.10.0",
    "torch": "2.1.2",
    "torchvision": "0.16.2",
    "torchaudio": "2.1.2",
    "feyn": "3.4.1",
    "gplearn": "0.4.2",
    "autora": "4.2.0",
    "autora.theorist.bms": None,
    "tqdm": "4.66.4",
    "sympy": "1.12",
    "setuptools": "68.2.2",
    "mdurl": None,
    "rich": None,
    "pyyaml": None,
    "ipykernel": None,
    "pykan": None,  # or kan
}

print("="*60)
print("Package installation and version check results:")
print("="*60)

for pkg, req_version in requirements.items():
    mod_name = pkg
    # Some packages have different import names and pip package names
    if pkg == "scikit-learn":
        mod_name = "sklearn"
    if pkg == "pykan":
        mod_name = "kan"
    if pkg == "pyyaml":
        mod_name = "yaml"  # pyyaml import name is yaml
    try:
        mod = importlib.import_module(mod_name)
        # Resolve installed version
        version = getattr(mod, "__version__", None)
        if not version:
            try:
                version = pkg_resources.get_distribution(pkg).version
            except Exception:
                version = "unknown"
        if req_version:
            # Allow +cpu suffix for related packages
            base_version = version.split('+')[0] if version else version
            if pkg in ["tensorflow", "torch", "torchvision", "torchaudio"]:
                if base_version == req_version:
                    print(f"✅ {pkg} installed, version match: {version}")
                else:
                    print(f"⚠️  {pkg} installed, version mismatch: {version} (required: {req_version})")
            else:
                if version == req_version:
                    print(f"✅ {pkg} installed, version match: {version}")
                else:
                    print(f"⚠️  {pkg} installed, version mismatch: {version} (required: {req_version})")
        else:
            print(f"✅ {pkg} installed, version: {version}")
    except ImportError:
        print(f"❌ {pkg} not installed")
    except Exception as e:
        print(f"⚠️  {pkg} check error: {e}")

print("="*60)
print("Check completed.")
print("="*60)
