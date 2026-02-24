import importlib
import pkg_resources

# 包名与要求版本
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
    "pykan": None,  # 或 kan
}

print("="*60)
print("包安装与版本检测结果：")
print("="*60)

for pkg, req_version in requirements.items():
    mod_name = pkg
    # 部分包导入名与pip名不同
    if pkg == "scikit-learn":
        mod_name = "sklearn"
    if pkg == "pykan":
        mod_name = "kan"
    if pkg == "pyyaml":
        mod_name = "yaml"  # pyyaml 实际导入名为 yaml
    try:
        mod = importlib.import_module(mod_name)
        # 获取版本
        version = getattr(mod, "__version__", None)
        if not version:
            try:
                version = pkg_resources.get_distribution(pkg).version
            except Exception:
                version = "未知"
        if req_version:
            # 允许 tensorflow/tf/torch 等包带有 +cpu 后缀
            base_version = version.split('+')[0] if version else version
            if pkg in ["tensorflow", "torch", "torchvision", "torchaudio"]:
                if base_version == req_version:
                    print(f"✅ {pkg} 已安装，版本匹配: {version}")
                else:
                    print(f"⚠️  {pkg} 已安装，版本不符: {version} (要求: {req_version})")
            else:
                if version == req_version:
                    print(f"✅ {pkg} 已安装，版本匹配: {version}")
                else:
                    print(f"⚠️  {pkg} 已安装，版本不符: {version} (要求: {req_version})")
        else:
            print(f"✅ {pkg} 已安装，版本: {version}")
    except ImportError:
        print(f"❌ {pkg} 未安装")
    except Exception as e:
        print(f"⚠️  {pkg} 检查异常: {e}")

print("="*60)
print("检测完成。")
print("="*60)