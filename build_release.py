#!/usr/bin/env python3
"""
COIN-OPERATED JRPG: Build and Release Automation
Automates building, testing, and packaging releases.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple
import shutil
import json
from datetime import datetime


class ReleaseManager:
    """Manages the release process."""
    
    def __init__(self, project_root: Path):
        """Initialize release manager."""
        self.root = project_root
        self.version = self._read_version()
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def _read_version(self) -> str:
        """Read version from package.json or default."""
        package_json = self.root / 'package.json'
        if package_json.exists():
            with open(package_json) as f:
                data = json.load(f)
                return data.get('version', '1.0.0')
        return '1.0.0'
    
    def run_command(self, cmd: List[str], description: str) -> Tuple[bool, str]:
        """Run a command and capture output."""
        print(f"  → {description}...")
        try:
            result = subprocess.run(
                cmd,
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                print(f"    ✅ {description} - Success")
                return True, result.stdout
            else:
                print(f"    ❌ {description} - Failed")
                self.errors.append(f"{description}: {result.stderr}")
                return False, result.stderr
        except subprocess.TimeoutExpired:
            print(f"    ❌ {description} - Timeout")
            self.errors.append(f"{description}: Timeout after 300s")
            return False, "Timeout"
        except Exception as e:
            print(f"    ❌ {description} - Error: {e}")
            self.errors.append(f"{description}: {str(e)}")
            return False, str(e)
    
    def check_prerequisites(self) -> bool:
        """Check if prerequisites are met."""
        print("\n📋 Checking Prerequisites...")
        
        all_good = True
        
        # Check Python version
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print("  ✅ Python 3.8+")
        else:
            print("  ❌ Python 3.8+ required")
            self.errors.append("Python version < 3.8")
            all_good = False
        
        # Check git
        success, _ = self.run_command(['git', '--version'], "Git available")
        all_good = all_good and success
        
        # Check dependencies
        try:
            import pygame
            print("  ✅ Pygame installed")
        except ImportError:
            print("  ❌ Pygame not installed")
            self.errors.append("Missing pygame")
            all_good = False
        
        try:
            import PIL
            print("  ✅ Pillow installed")
        except ImportError:
            print("  ❌ Pillow not installed")
            self.errors.append("Missing Pillow")
            all_good = False
        
        # Check required files
        required_files = [
            'launch_game.py',
            'python-core/interfaces.py',
            'python-core/graphics/adapter.py',
            'requirements.txt'
        ]
        
        for file_path in required_files:
            if (self.root / file_path).exists():
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path} missing")
                self.errors.append(f"Missing {file_path}")
                all_good = False
        
        return all_good
    
    def run_tests(self) -> bool:
        """Run all tests."""
        print("\n🧪 Running Tests...")
        
        all_passed = True
        
        # Run unit tests
        test_file = self.root / 'test_graphics_system.py'
        if test_file.exists():
            success, output = self.run_command(
                [sys.executable, str(test_file)],
                "Unit tests"
            )
            all_passed = all_passed and success
        else:
            print("  ⚠️  No test file found")
            self.warnings.append("No unit tests found")
        
        # Run validation scripts
        validation_dir = self.root / 'automation'
        if validation_dir.exists():
            for script in validation_dir.glob('validate_*.py'):
                success, _ = self.run_command(
                    [sys.executable, str(script)],
                    f"Validation: {script.stem}"
                )
                all_passed = all_passed and success
        else:
            print("  ⚠️  No validation scripts found")
            self.warnings.append("No validation scripts found")
        
        return all_passed
    
    def run_linting(self) -> bool:
        """Run code quality checks."""
        print("\n🔍 Running Code Quality Checks...")
        
        # Check for common issues
        success, _ = self.run_command(
            ['python3', '-m', 'py_compile'] + list(self.root.glob('python-core/**/*.py')),
            "Syntax check"
        )
        
        # Try to run flake8 if available
        try:
            result = subprocess.run(['flake8', '--version'], capture_output=True)
            if result.returncode == 0:
                self.run_command(
                    ['flake8', 'python-core/', '--max-line-length=100'],
                    "Flake8 linting"
                )
        except FileNotFoundError:
            print("  ℹ️  Flake8 not installed - skipping linting")
            self.warnings.append("Flake8 not available")
        
        return success
    
    def clean_build(self) -> bool:
        """Clean build artifacts."""
        print("\n🧹 Cleaning Build Artifacts...")
        
        # Remove __pycache__
        for pycache in self.root.rglob('__pycache__'):
            shutil.rmtree(pycache)
            print(f"  ✅ Removed {pycache.relative_to(self.root)}")
        
        # Remove .pyc files
        for pyc in self.root.rglob('*.pyc'):
            pyc.unlink()
            print(f"  ✅ Removed {pyc.relative_to(self.root)}")
        
        # Remove dist directory if exists
        dist_dir = self.root / 'dist'
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
            print(f"  ✅ Removed dist/")
        
        return True
    
    def build_package(self) -> bool:
        """Build release package."""
        print(f"\n📦 Building Release Package (v{self.version})...")
        
        # Create dist directory
        dist_dir = self.root / 'dist' / f'coin-operated-jrpg-v{self.version}'
        dist_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy essential files
        files_to_copy = [
            'launch_game.py',
            'requirements.txt',
            'README.md',
            'LICENSE',
        ]
        
        for file_name in files_to_copy:
            src = self.root / file_name
            if src.exists():
                dst = dist_dir / file_name
                shutil.copy2(src, dst)
                print(f"  ✅ Copied {file_name}")
        
        # Copy directories
        dirs_to_copy = [
            'python-core',
            'docs',
        ]
        
        for dir_name in dirs_to_copy:
            src = self.root / dir_name
            if src.exists():
                dst = dist_dir / dir_name
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
                print(f"  ✅ Copied {dir_name}/")
        
        # Create release notes
        release_notes = dist_dir / 'RELEASE_NOTES.txt'
        with open(release_notes, 'w') as f:
            f.write(f"COIN-OPERATED JRPG v{self.version}\n")
            f.write(f"Release Date: {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write("\n")
            f.write("Installation:\n")
            f.write("1. pip install -r requirements.txt\n")
            f.write("2. python3 launch_game.py\n")
            f.write("\n")
            f.write("Modes:\n")
            f.write("- Text: python3 launch_game.py --mode text\n")
            f.write("- Graphics: python3 launch_game.py --mode graphics\n")
            f.write("- SNES: python3 launch_game.py --mode snes\n")
        
        print(f"  ✅ Created release notes")
        
        # Create archive
        archive_name = f'coin-operated-jrpg-v{self.version}'
        archive_path = self.root / 'dist' / archive_name
        
        shutil.make_archive(
            str(archive_path),
            'zip',
            self.root / 'dist',
            archive_name
        )
        
        print(f"  ✅ Created {archive_name}.zip")
        
        return True
    
    def generate_checksums(self) -> bool:
        """Generate checksums for release files."""
        print("\n🔐 Generating Checksums...")
        
        import hashlib
        
        dist_dir = self.root / 'dist'
        archive = dist_dir / f'coin-operated-jrpg-v{self.version}.zip'
        
        if not archive.exists():
            print("  ❌ Archive not found")
            return False
        
        # Calculate SHA256
        sha256_hash = hashlib.sha256()
        with open(archive, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        checksum = sha256_hash.hexdigest()
        
        # Write checksum file
        checksum_file = archive.with_suffix('.sha256')
        with open(checksum_file, 'w') as f:
            f.write(f"{checksum}  {archive.name}\n")
        
        print(f"  ✅ SHA256: {checksum}")
        print(f"  ✅ Wrote {checksum_file.name}")
        
        return True
    
    def create_git_tag(self) -> bool:
        """Create git tag for release."""
        print(f"\n🏷️  Creating Git Tag v{self.version}...")
        
        # Check if tag exists
        success, output = self.run_command(
            ['git', 'tag', '-l', f'v{self.version}'],
            "Check existing tag"
        )
        
        if output.strip():
            print(f"  ⚠️  Tag v{self.version} already exists")
            self.warnings.append(f"Tag v{self.version} already exists")
            return True
        
        # Create tag
        success, _ = self.run_command(
            ['git', 'tag', '-a', f'v{self.version}', '-m', f'Release v{self.version}'],
            f"Create tag v{self.version}"
        )
        
        if success:
            print(f"  ℹ️  Push with: git push origin v{self.version}")
        
        return success
    
    def print_summary(self, success: bool):
        """Print build summary."""
        print("\n" + "=" * 70)
        print(f"Build Summary - v{self.version}".center(70))
        print("=" * 70)
        
        if success:
            print("\n✅ Build Successful!")
            
            dist_dir = self.root / 'dist'
            archive = dist_dir / f'coin-operated-jrpg-v{self.version}.zip'
            
            if archive.exists():
                size_mb = archive.stat().st_size / (1024 * 1024)
                print(f"\n📦 Release Package:")
                print(f"   Location: {archive}")
                print(f"   Size: {size_mb:.2f} MB")
            
            print(f"\n🎉 Ready to release v{self.version}!")
        else:
            print("\n❌ Build Failed!")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"   - {error}")
        
        print("\n" + "=" * 70)


def main():
    """Run release automation."""
    print("\n" + "=" * 70)
    print("COIN-OPERATED JRPG - Release Automation".center(70))
    print("=" * 70)
    
    project_root = Path(__file__).parent
    manager = ReleaseManager(project_root)
    
    # Run build steps
    steps = [
        ("Check Prerequisites", manager.check_prerequisites),
        ("Clean Build", manager.clean_build),
        ("Run Tests", manager.run_tests),
        ("Run Linting", manager.run_linting),
        ("Build Package", manager.build_package),
        ("Generate Checksums", manager.generate_checksums),
        ("Create Git Tag", manager.create_git_tag),
    ]
    
    overall_success = True
    
    for step_name, step_func in steps:
        success = step_func()
        overall_success = overall_success and success
        
        if not success and step_name in ["Check Prerequisites", "Run Tests"]:
            print(f"\n❌ Critical step failed: {step_name}")
            print("   Aborting build process")
            overall_success = False
            break
    
    # Print summary
    manager.print_summary(overall_success)
    
    return 0 if overall_success else 1


if __name__ == "__main__":
    sys.exit(main())
