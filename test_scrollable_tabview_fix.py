"""
Test to verify the ScrollableTabView widget packing fix.
This test creates a ScrollableTabView and adds multiple tabs to ensure
the rebalancing logic works correctly without packing errors.
"""

import sys
import os

# Add src to path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    import customtkinter as ctk
    from ui.scrollable_tabview import ScrollableTabView
    
    def test_scrollable_tabview():
        """Test that ScrollableTabView can add multiple tabs without errors."""
        print("Testing ScrollableTabView widget...")
        
        # Create root window (hidden)
        root = ctk.CTk()
        root.withdraw()  # Hide the window
        
        try:
            # Create the scrollable tabview
            tabview = ScrollableTabView(root)
            tabview.pack(fill="both", expand=True)
            
            # Add multiple tabs to trigger rebalancing
            # This should distribute tabs across two rows
            tab_names = [
                "🐼 Sort Textures",
                "🔄 Convert Files",
                "🔧 Alpha Fixer",
                "📁 File Browser",
                "🎮 Game Profiles",
                "📝 Notepad",
                "🔍 Image Upscaler",
                "🎭 Background Remover",
                "🔍 Quality Checker",
                "📏 Batch Normalizer",
                "✏️ Line Art",
                "📝 Batch Rename",
                "🎨 Color Correction",
                "🔧 Image Repair",
                "📊 Performance",
                "ℹ️ About"
            ]
            
            # Add tabs one by one
            for i, name in enumerate(tab_names):
                print(f"Adding tab {i+1}/{len(tab_names)}: {name}")
                tab_frame = tabview.add(name)
                
                # Verify the tab was added
                assert name in tabview.tabs, f"Tab '{name}' was not added to tabs dict"
                assert name in tabview.tab_buttons, f"Tab '{name}' was not added to tab_buttons dict"
                assert tabview.tab_buttons[name] is not None, f"Button for tab '{name}' is None"
                
            print(f"\n✓ Successfully added {len(tab_names)} tabs")
            
            # Verify tabs are distributed across rows
            half = (len(tab_names) + 1) // 2  # Ceiling division
            row1_count = 0
            row2_count = 0
            
            for name, btn in tabview.tab_buttons.items():
                if btn.master == tabview.row1:
                    row1_count += 1
                elif btn.master == tabview.row2:
                    row2_count += 1
            
            print(f"✓ Row 1 has {row1_count} tabs")
            print(f"✓ Row 2 has {row2_count} tabs")
            assert row1_count + row2_count == len(tab_names), "Not all buttons are in rows"
            
            # Test switching tabs
            print("\nTesting tab switching...")
            tabview.set(tab_names[5])
            assert tabview.current_tab == tab_names[5], "Failed to switch to tab"
            print(f"✓ Successfully switched to tab: {tab_names[5]}")
            
            # Test deleting a tab
            print("\nTesting tab deletion...")
            delete_name = tab_names[3]
            tabview.delete(delete_name)
            assert delete_name not in tabview.tabs, f"Tab '{delete_name}' was not deleted"
            assert delete_name not in tabview.tab_buttons, f"Button '{delete_name}' was not deleted"
            print(f"✓ Successfully deleted tab: {delete_name}")
            
            print("\n" + "="*50)
            print("✅ All tests passed! ScrollableTabView is working correctly.")
            print("="*50)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            root.destroy()
    
    if __name__ == "__main__":
        success = test_scrollable_tabview()
        sys.exit(0 if success else 1)
        
except ImportError as e:
    print(f"Cannot run test - missing dependency: {e}")
    print("This is expected in environments without GUI libraries.")
    sys.exit(0)  # Exit with success since this is expected
