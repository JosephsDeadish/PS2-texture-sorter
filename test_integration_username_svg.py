#!/usr/bin/env python3
"""
Integration Test for Username Feature and SVG Support
Validates that both features work together without conflicts.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.features.panda_character import PandaCharacter, PandaGender
from src.file_handler.file_handler import FileHandler, HAS_SVG
from src.config import config


def test_panda_username_integration():
    """Test that PandaCharacter username feature works."""
    print("Testing PandaCharacter with username...")
    
    # Test initialization with username
    panda = PandaCharacter(username="TestUser")
    assert panda.username == "TestUser", "Username should be set"
    
    # Test set_username
    panda.set_username("NewUser")
    assert panda.username == "NewUser", "Username should be updated"
    
    # Test that panda can respond with username
    response = panda.on_click()
    assert isinstance(response, str), "Response should be a string"
    assert len(response) > 0, "Response should not be empty"
    
    print("✓ PandaCharacter username integration works")
    return True


def test_file_handler_svg_support():
    """Test that FileHandler has SVG support properly configured."""
    print("Testing FileHandler SVG support...")
    
    # Initialize FileHandler
    fh = FileHandler()
    
    # Check that SVG formats are in supported formats
    assert '.svg' in FileHandler.SUPPORTED_FORMATS, "SVG should be in supported formats"
    assert '.svgz' in FileHandler.SUPPORTED_FORMATS, "SVGZ should be in supported formats"
    
    # Check vector formats
    assert '.svg' in FileHandler.VECTOR_FORMATS, "SVG should be in vector formats"
    assert '.svgz' in FileHandler.VECTOR_FORMATS, "SVGZ should be in vector formats"
    
    print(f"✓ FileHandler SVG support configured (available: {HAS_SVG})")
    return True


def test_features_coexist():
    """Test that both features can coexist without conflicts."""
    print("Testing that both features coexist...")
    
    # Initialize both features
    panda = PandaCharacter(username="IntegrationTest")
    fh = FileHandler()
    
    # Test panda works
    response = panda.on_click()
    assert isinstance(response, str), "Panda should respond"
    
    # Test file handler works
    assert hasattr(fh, 'create_backup'), "FileHandler should have attributes"
    
    # Test that username is preserved
    assert panda.username == "IntegrationTest", "Username should be preserved"
    
    # Test that SVG formats are still recognized
    assert '.svg' in FileHandler.SUPPORTED_FORMATS, "SVG should still be supported"
    
    print("✓ Both features coexist without conflicts")
    return True


def test_config_integration():
    """Test that config supports both features."""
    print("Testing config integration...")
    
    # Test username config
    username = config.get('panda', 'username', default="")
    assert isinstance(username, str), "Username config should be a string"
    
    # Test that config doesn't interfere with file handler
    # (there's no SVG-specific config, but we can verify config works)
    backup_setting = config.get('file_handling', 'create_backup', default=True)
    assert isinstance(backup_setting, bool), "Backup setting should work"
    
    print("✓ Config supports both features")
    return True


def test_panda_initialization_with_username():
    """Test that PandaCharacter can be initialized with all parameters including username."""
    print("Testing PandaCharacter initialization with all parameters...")
    
    # Test with all parameters (as done in main.py)
    panda = PandaCharacter(
        name="TestPanda",
        gender=PandaGender.FEMALE,
        username="FullTestUser"
    )
    
    assert panda.name == "TestPanda", "Name should be set"
    assert panda.gender == PandaGender.FEMALE, "Gender should be set"
    assert panda.username == "FullTestUser", "Username should be set"
    
    print("✓ PandaCharacter initialization with all parameters works")
    return True


if __name__ == "__main__":
    print("\n" + "="*70)
    print("Integration Test: Username Feature + SVG Support")
    print("="*70 + "\n")
    
    try:
        test_panda_username_integration()
        test_file_handler_svg_support()
        test_features_coexist()
        test_config_integration()
        test_panda_initialization_with_username()
        
        print("\n" + "="*70)
        print("✓ All integration tests passed!")
        print("✓ Username feature and SVG support work together correctly")
        print("="*70 + "\n")
        
    except AssertionError as e:
        print(f"\n✗ Integration test failed: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
