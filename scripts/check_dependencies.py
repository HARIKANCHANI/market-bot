#!/usr/bin/env python3
"""
Check for dependency issues in the repository.
- Find all imports in Python files
- Compare with requirements.txt
- Identify missing dependencies
- Check for version conflicts
"""
import os
import re
import ast
from pathlib import Path
from collections import defaultdict

def find_python_files(root_dir):
    """Find all Python files, excluding venv and archive."""
    py_files = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ['venv', 'archive', '__pycache__', '.git', 'node_modules', '.venv']]
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files

def extract_imports(filepath):
    """Extract all import statements from a Python file."""
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Parse the file as AST
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
        except SyntaxError:
            # Fallback to regex if AST parsing fails
            import_lines = re.findall(r'^import\s+([a-zA-Z0-9_., ]+)', content, re.MULTILINE)
            from_lines = re.findall(r'^from\s+([a-zA-Z0-9_.]+)\s+import', content, re.MULTILINE)
            
            for imp in import_lines:
                for module in imp.split(','):
                    imports.add(module.strip().split('.')[0])
            
            for imp in from_lines:
                imports.add(imp.split('.')[0])
    
    except Exception as e:
        print(f"⚠️  Error reading {filepath}: {e}")
    
    return imports

def parse_requirements(req_file):
    """Parse requirements.txt and extract package names."""
    packages = {}
    try:
        with open(req_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name (before >= or ==)
                    match = re.match(r'^([a-zA-Z0-9_-]+)', line)
                    if match:
                        pkg_name = match.group(1)
                        packages[pkg_name] = line
    except FileNotFoundError:
        print(f"❌ {req_file} not found!")
    
    return packages

# Map import names to package names (some differ)
IMPORT_TO_PACKAGE = {
    'PIL': 'Pillow',
    'cv2': 'opencv-python',
    'sklearn': 'scikit-learn',
    'yaml': 'PyYAML',
    'dotenv': 'python-dotenv',
    'docx': 'python-docx',
    'graphviz': 'graphviz',
}

# Standard library modules (don't need to be in requirements.txt)
STDLIB_MODULES = {
    'os', 'sys', 'time', 'datetime', 're', 'json', 'logging', 'pathlib',
    'collections', 'itertools', 'functools', 'typing', 'ast', 'subprocess',
    'urllib', 'http', 'csv', 'math', 'random', 'hashlib', 'io', 'shutil',
    'tempfile', 'glob', 'pickle', 'copy', 'enum', 'abc', 'warnings',
    '__future__', 'argparse', 'configparser', 'unittest', 'traceback'
}

def main():
    root_dir = Path(__file__).parent.parent
    print(f"🔍 Scanning Python files in: {root_dir}\n")
    
    # Find all Python files
    py_files = find_python_files(root_dir)
    print(f"Found {len(py_files)} Python files\n")
    
    # Extract all imports
    all_imports = defaultdict(list)
    for py_file in py_files:
        rel_path = os.path.relpath(py_file, root_dir)
        imports = extract_imports(py_file)
        for imp in imports:
            if imp not in STDLIB_MODULES:
                all_imports[imp].append(rel_path)
    
    # Parse requirements.txt
    req_file = root_dir / 'requirements.txt'
    required_packages = parse_requirements(req_file)
    
    print(f"{'='*70}")
    print(f"📦 DEPENDENCY ANALYSIS")
    print(f"{'='*70}\n")
    
    # Check for missing dependencies
    missing = []
    for import_name, files in sorted(all_imports.items()):
        # Skip local imports (src, data, tests, scripts, utilities)
        if import_name in ['src', 'data', 'tests', 'scripts', 'utilities']:
            continue
        
        # Map import name to package name
        package_name = IMPORT_TO_PACKAGE.get(import_name, import_name)
        
        if package_name not in required_packages:
            missing.append((import_name, package_name, files))
    
    if missing:
        print(f"❌ MISSING DEPENDENCIES ({len(missing)}):\n")
        for import_name, package_name, files in missing:
            print(f"  📦 {import_name} (package: {package_name})")
            print(f"     Used in: {files[0]}")
            if len(files) > 1:
                print(f"     ... and {len(files)-1} more file(s)")
            print()
    else:
        print("✅ No missing dependencies found!\n")
    
    # Show current requirements
    print(f"{'='*70}")
    print(f"📋 CURRENT REQUIREMENTS")
    print(f"{'='*70}\n")
    for pkg, line in sorted(required_packages.items()):
        print(f"  ✓ {line}")
    
    print(f"\n{'='*70}")
    print(f"📊 SUMMARY")
    print(f"{'='*70}")
    print(f"Python files scanned: {len(py_files)}")
    print(f"Unique imports found: {len(all_imports)}")
    print(f"Required packages: {len(required_packages)}")
    print(f"Missing dependencies: {len(missing)}")
    
    return missing

if __name__ == "__main__":
    missing = main()
    exit(0 if not missing else 1)
