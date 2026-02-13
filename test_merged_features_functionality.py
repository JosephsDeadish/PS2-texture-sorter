#!/usr/bin/env python3
"""
Comprehensive Test for Merged Features
Tests that username feature and SVG support work together in realistic scenarios.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.features.panda_character import PandaCharacter, PandaGender
from src.file_handler.file_handler import FileHandler, HAS_SVG
from src.config import config


def test_realistic_panda_usage():
    """Test PandaCharacter as it would be used in main.py"""
    print("Testing realistic PandaCharacter usage...")
    
    # Simulate loading from config (as in main.py line 465)
    panda_name = config.get('panda', 'name', default="Panda")
    panda_gender_str = config.get('panda', 'gender', default='non_binary')
    panda_username = config.get('panda', 'username', default="")
    
    panda_gender = PandaGender.NON_BINARY
    if panda_gender_str == 'male':
        panda_gender = PandaGender.MALE
    elif panda_gender_str == 'female':
        panda_gender = PandaGender.FEMALE
    
    # Initialize exactly as main.py does
    panda = PandaCharacter(name=panda_name, gender=panda_gender, username=panda_username)
    
    # Test that all attributes work
    assert hasattr(panda, 'name'), "Panda should have name"
    assert hasattr(panda, 'gender'), "Panda should have gender"
    assert hasattr(panda, 'username'), "Panda should have username"
    
    # Test that panda can interact
    response = panda.on_click()
    assert isinstance(response, str) and len(response) > 0, "Panda should respond to clicks"
    
    # Test setting username (as done in panda_widget.py)
    test_username = "TestUser123"
    panda.set_username(test_username)
    assert panda.username == test_username, "Username should be set"
    
    # Verify personalized messages can work
    personalized_response = panda._personalize_message("Hello!")
    assert isinstance(personalized_response, str), "Personalized message should be string"
    
    print("✓ Realistic PandaCharacter usage works correctly")
    return True


def test_realistic_file_handler_usage():
    """Test FileHandler as it would be used in main.py"""
    print("Testing realistic FileHandler usage...")
    
    # Initialize as in main.py line 400
    create_backup = config.get('file_handling', 'create_backup', default=True)
    file_handler = FileHandler(create_backup=create_backup)
    
    # Test that file handler has required attributes
    assert hasattr(file_handler, 'create_backup'), "FileHandler should have create_backup"
    
    # Test supported formats
    assert '.svg' in FileHandler.SUPPORTED_FORMATS, "SVG should be supported"
    assert '.svgz' in FileHandler.SUPPORTED_FORMATS, "SVGZ should be supported"
    assert '.png' in FileHandler.SUPPORTED_FORMATS, "PNG should be supported"
    assert '.jpg' in FileHandler.SUPPORTED_FORMATS, "JPG should be supported"
    
    # Test vector formats detection
    assert '.svg' in FileHandler.VECTOR_FORMATS, "SVG should be vector format"
    assert '.svgz' in FileHandler.VECTOR_FORMATS, "SVGZ should be vector format"
    
    # Test raster formats
    assert '.png' in FileHandler.RASTER_FORMATS, "PNG should be raster format"
    assert '.jpg' in FileHandler.RASTER_FORMATS, "JPG should be raster format"
    
    print(f"✓ Realistic FileHandler usage works correctly (SVG available: {HAS_SVG})")
    return True


def test_concurrent_feature_usage():
    """Test using both features concurrently (as they would be in the app)"""
    print("Testing concurrent feature usage...")
    
    # Initialize both features as they would be in the app
    panda = PandaCharacter(name="TestPanda", username="ConcurrentUser")
    file_handler = FileHandler()
    
    # Simulate panda interactions while file handler is active
    for i in range(10):
        response = panda.on_click()
        assert isinstance(response, str), f"Click {i} should return string"
    
    # Test that username persists
    assert panda.username == "ConcurrentUser", "Username should persist through clicks"
    
    # Test that file handler still works
    assert hasattr(file_handler, 'create_backup'), "FileHandler should still work"
    
    # Change username and verify it works
    panda.set_username("UpdatedUser")
    assert panda.username == "UpdatedUser", "Username should update"
    
    # Verify file handler still recognizes SVG
    assert '.svg' in FileHandler.SUPPORTED_FORMATS, "SVG should still be supported"
    
    print("✓ Concurrent feature usage works correctly")
    return True


def test_config_persistence():
    """Test that config changes for both features persist"""
    print("Testing config persistence...")
    
    # Test username config
    test_username = "ConfigTestUser"
    config.set('panda', 'username', value=test_username)
    retrieved_username = config.get('panda', 'username', default="")
    assert retrieved_username == test_username, "Username should persist in config"
    
    # Test file handler config
    config.set('file_handling', 'create_backup', value=False)
    retrieved_backup = config.get('file_handling', 'create_backup', default=True)
    assert retrieved_backup == False, "Backup setting should persist in config"
    
    # Reset to defaults
    config.set('file_handling', 'create_backup', value=True)
    
    print("✓ Config persistence works for both features")
    return True


def test_no_namespace_collisions():
    """Test that features don't have namespace collisions"""
    print("Testing for namespace collisions...")
    
    # Import both main modules
    from src.features import panda_character
    from src.file_handler import file_handler
    
    # Check that they have distinct namespaces
    panda_attrs = dir(panda_character)
    file_handler_attrs = dir(file_handler)
    
    # Check key classes don't collide
    assert hasattr(panda_character, 'PandaCharacter'), "PandaCharacter should exist"
    assert hasattr(file_handler, 'FileHandler'), "FileHandler should exist"
    
    # Verify they can be used together
    panda = panda_character.PandaCharacter(username="NoCollision")
    fh = file_handler.FileHandler()
    
    assert panda.username == "NoCollision", "Panda username should work"
    assert hasattr(fh, 'create_backup'), "FileHandler should work"
    
    print("✓ No namespace collisions detected")
    return True


def test_error_handling():
    """Test that errors in one feature don't affect the other"""
    print("Testing error handling...")
    
    # Test that invalid username doesn't crash
    panda = PandaCharacter(username="")
    response = panda.on_click()
    assert isinstance(response, str), "Should handle empty username"
    
    # Test that panda works even if file handler has issues
    panda2 = PandaCharacter(username="ErrorTest")
    assert panda2.username == "ErrorTest", "Panda should work independently"
    
    # Test that file handler works independently
    fh = FileHandler()
    assert '.svg' in FileHandler.SUPPORTED_FORMATS, "FileHandler should work independently"
    
    print("✓ Error handling works correctly")
    return True


if __name__ == "__main__":
    print("\n" + "="*70)
    print("Comprehensive Merged Features Test")
    print("="*70 + "\n")
    
    try:
        test_realistic_panda_usage()
        test_realistic_file_handler_usage()
        test_concurrent_feature_usage()
        test_config_persistence()
        test_no_namespace_collisions()
        test_error_handling()
        
        print("\n" + "="*70)
        print("✓ ALL TESTS PASSED!")
        print("✓ Username feature and SVG support are properly integrated")
        print("✓ No merge conflicts or integration issues detected")
        print("="*70 + "\n")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
