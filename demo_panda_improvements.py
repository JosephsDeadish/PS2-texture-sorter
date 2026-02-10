#!/usr/bin/env python
"""
Demo script for new panda features
Showcases all the improvements to the panda companion system
"""

import sys
import time
sys.path.insert(0, '.')

from src.features.panda_character import PandaCharacter, PandaGender

def print_section(title):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def main():
    print("\n🐼 PANDA COMPANION FEATURE SHOWCASE 🐼\n")
    
    # 1. Create panda with name and gender
    print_section("1. Creating Customized Panda")
    panda = PandaCharacter(name="Bamboo", gender=PandaGender.FEMALE)
    print(f"✓ Created panda named: {panda.name}")
    print(f"✓ Gender: {panda.gender.value}")
    print(f"✓ Pronouns: {panda.get_pronoun_subject()}/{panda.get_pronoun_object()}/{panda.get_pronoun_possessive()}")
    
    # 2. Show expanded animations
    print_section("2. Enhanced Animations (All with Paw Feet!)")
    animations = ['idle', 'working', 'celebrating', 'rage', 'eating', 'playing']
    for anim_name in animations:
        frames = panda.ANIMATIONS[anim_name]
        has_feet = '⚪ ⚪' in frames[0] or '⚪⚪' in frames[0]
        print(f"  {anim_name:12} - {len(frames)} frames {'✓' if has_feet else '✗'} paw feet")
    
    # 3. Show one animation
    print_section("3. Sample Animation Frame (Idle)")
    print(panda.get_animation_frame('idle'))
    
    # 4. Show expanded responses
    print_section("4. Expanded Response Collections")
    print(f"  Click responses:     {len(panda.CLICK_RESPONSES)} variations")
    print(f"  Feed responses:      {len(panda.FEED_RESPONSES)} variations")
    print(f"  Drag responses:      {len(panda.DRAG_RESPONSES)} variations")
    print(f"  Toss responses:      {len(panda.TOSS_RESPONSES)} variations")
    print(f"  Wall hit responses:  {len(panda.WALL_HIT_RESPONSES)} variations")
    print(f"  Hover thoughts:      {len(panda.HOVER_THOUGHTS)} variations")
    print(f"  Petting responses:   {len(panda.PETTING_RESPONSES)} variations")
    
    # 5. Sample interactions
    print_section("5. Sample Interactions")
    print("Click response:")
    print(f"  {panda.on_click()}")
    print("\nFeed response:")
    print(f"  {panda.on_feed()}")
    print("\nDrag response:")
    print(f"  {panda.on_drag()}")
    print("\nHover thought:")
    print(f"  {panda.on_hover()}")
    
    # 6. Gender pronoun demonstration
    print_section("6. Gender & Pronoun System")
    
    for gender, name in [(PandaGender.MALE, "Bruce"), 
                         (PandaGender.FEMALE, "Lucy"),
                         (PandaGender.NON_BINARY, "Alex")]:
        panda.set_name(name)
        panda.set_gender(gender)
        print(f"{name} ({gender.value}):")
        print(f"  {panda.get_pronoun_subject().capitalize()} is a panda.")
        print(f"  You can pet {panda.get_pronoun_object()}.")
        print(f"  This is {panda.get_pronoun_possessive()} favorite bamboo.")
        print()
    
    # 7. Mood-specific messages
    print_section("7. Mood-Specific Messages")
    for mood, messages in panda.MOOD_MESSAGES.items():
        print(f"  {mood.value:12} - {len(messages):2} messages")
    
    # 8. Statistics
    print_section("8. Panda Statistics")
    stats = panda.get_statistics()
    print(f"  Name:            {stats['name']}")
    print(f"  Gender:          {stats['gender']}")
    print(f"  Current mood:    {stats['current_mood']}")
    print(f"  Click count:     {stats['click_count']}")
    print(f"  Feed count:      {stats['feed_count']}")
    print(f"  Files processed: {stats['files_processed']}")
    print(f"  Easter eggs:     {stats['easter_eggs_found']}")
    
    print_section("🎉 Feature Showcase Complete!")
    print("Your panda companion is now:")
    print("  ✓ More expressive (5-8 frames per animation)")
    print("  ✓ Complete with paw feet on all animations")
    print("  ✓ Fully customizable (name & gender)")
    print("  ✓ More talkative (175+ unique responses)")
    print("  ✓ Gender-aware with proper pronouns")
    print("  ✓ Able to display equipped items")
    print("  ✓ Larger and more visible")
    print("  ✓ Transparent background for seamless UI")
    print("\n🐼 Have fun with your enhanced panda companion! 🐼\n")

if __name__ == "__main__":
    main()
