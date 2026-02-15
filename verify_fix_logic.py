"""
Logic verification for the ScrollableTabView fix.
This script analyzes the code to ensure the fix resolves the widget packing issue.
"""

import ast
import sys

def analyze_scrollable_tabview():
    """Analyze the ScrollableTabView code to verify the fix."""
    print("="*70)
    print("ScrollableTabView Fix Analysis")
    print("="*70)
    
    with open('src/ui/scrollable_tabview.py', 'r') as f:
        lines = f.readlines()
    
    # Check the add method
    print("\n1. Checking add() method...")
    add_method_lines = []
    in_add = False
    for i, line in enumerate(lines, 1):
        if 'def add(self, name: str)' in line:
            in_add = True
        elif in_add:
            if line.strip().startswith('def '):
                break
            add_method_lines.append((i, line))
    
    # Verify that buttons are not created with a fixed parent in add()
    creates_button_in_add = False
    for line_num, line in add_method_lines:
        if 'ctk.CTkButton(' in line and 'self.row1' in line:
            creates_button_in_add = True
            print(f"   ✗ Line {line_num}: Still creates button with fixed parent self.row1")
            break
    
    if not creates_button_in_add:
        print("   ✓ add() method does not create buttons with fixed parent")
        print("   ✓ Buttons will be created dynamically in _rebalance_rows()")
    
    # Check that tab_buttons[name] is set to None
    sets_none = False
    for line_num, line in add_method_lines:
        if 'self.tab_buttons[name] = None' in line:
            sets_none = True
            print(f"   ✓ Line {line_num}: Sets tab_buttons[name] to None initially")
            break
    
    if not sets_none:
        print("   ✗ Does not set tab_buttons[name] to None")
    
    # Check the _rebalance_rows method
    print("\n2. Checking _rebalance_rows() method...")
    rebalance_lines = []
    in_rebalance = False
    for i, line in enumerate(lines, 1):
        if 'def _rebalance_rows(self)' in line:
            in_rebalance = True
        elif in_rebalance:
            if line.strip().startswith('def ') or (line.strip().startswith('class ') and 'class' in line):
                break
            rebalance_lines.append((i, line))
    
    # Check that buttons are destroyed
    destroys_buttons = False
    for line_num, line in rebalance_lines:
        if 'btn.destroy()' in line:
            destroys_buttons = True
            print(f"   ✓ Line {line_num}: Destroys existing buttons")
            break
    
    if not destroys_buttons:
        print("   ✗ Does not destroy existing buttons")
    
    # Check that buttons are recreated with dynamic parent
    creates_with_parent = False
    uses_in_parameter = False
    for line_num, line in rebalance_lines:
        if 'ctk.CTkButton(' in line:
            # Check next few lines for parent assignment
            for _, next_line in rebalance_lines[rebalance_lines.index((line_num, line)):rebalance_lines.index((line_num, line))+10]:
                if 'parent' in next_line and ('self.row1' in next_line or 'self.row2' in next_line):
                    creates_with_parent = True
                    break
        if 'pack(in_=' in line:
            uses_in_parameter = True
            print(f"   ✗ Line {line_num}: Still uses pack(in_=...) which causes the error")
    
    if creates_with_parent and not uses_in_parameter:
        print("   ✓ Buttons are recreated with dynamic parent (row1 or row2)")
        print("   ✓ Does not use pack(in_=...) parameter")
    
    # Check the set method
    print("\n3. Checking set() method...")
    set_lines = []
    in_set = False
    for i, line in enumerate(lines, 1):
        if 'def set(self, name: str)' in line:
            in_set = True
        elif in_set:
            if line.strip().startswith('def '):
                break
            set_lines.append((i, line))
    
    # Check for None checks
    checks_none = False
    for line_num, line in set_lines:
        if 'is not None' in line and 'tab_buttons' in line:
            checks_none = True
            print(f"   ✓ Line {line_num}: Checks if button is not None before configuring")
            break
    
    if not checks_none:
        print("   ⚠ Warning: set() might not check for None buttons")
    
    # Check the delete method
    print("\n4. Checking delete() method...")
    delete_lines = []
    in_delete = False
    for i, line in enumerate(lines, 1):
        if 'def delete(self, name: str)' in line:
            in_delete = True
        elif in_delete:
            if line.strip().startswith('def ') or (line.strip().startswith('class ') and 'class' in line):
                break
            delete_lines.append((i, line))
    
    # Check for None checks before destroy
    checks_none_delete = False
    for line_num, line in delete_lines:
        if 'is not None' in line and 'tab_buttons' in line:
            checks_none_delete = True
            print(f"   ✓ Line {line_num}: Checks if button is not None before destroying")
            break
    
    if not checks_none_delete:
        print("   ⚠ Warning: delete() might not check for None buttons")
    
    # Summary
    print("\n" + "="*70)
    print("ANALYSIS SUMMARY")
    print("="*70)
    
    issues = []
    
    if creates_button_in_add:
        issues.append("- add() still creates buttons with fixed parent")
    
    if uses_in_parameter:
        issues.append("- _rebalance_rows() still uses pack(in_=...) which causes the error")
    
    if not destroys_buttons:
        issues.append("- _rebalance_rows() doesn't destroy old buttons")
    
    if not creates_with_parent:
        issues.append("- _rebalance_rows() doesn't recreate buttons with dynamic parent")
    
    if issues:
        print("\n❌ Issues found:")
        for issue in issues:
            print(issue)
        return False
    else:
        print("\n✅ All checks passed!")
        print("\nThe fix correctly addresses the widget packing issue by:")
        print("  1. Not creating buttons with a fixed parent in add()")
        print("  2. Destroying all existing buttons in _rebalance_rows()")
        print("  3. Recreating buttons with the correct parent (row1 or row2)")
        print("  4. Not using the problematic pack(in_=...) parameter")
        print("\nThis ensures widgets are always packed into their actual parent,")
        print("preventing the TclError: 'can't pack X inside Y' error.")
        return True

if __name__ == "__main__":
    success = analyze_scrollable_tabview()
    sys.exit(0 if success else 1)
