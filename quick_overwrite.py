#!/usr/bin/env python3
"""
Quick Overwrite - Simple tool to choose between similar code
"""

def show_simple_options():
    print("🎯 When you find similar code, choose:")
    print("1. Keep the first version")
    print("2. Keep the second version") 
    print("3. Create a shared function")
    print("4. Skip (keep all)")
    
    choice = input("Enter choice (1-4): ")
    return choice

def handle_similar_code(code1, code2, file1, file2):
    print(f"\n📁 Found similar code in:")
    print(f"   File 1: {file1}")
    print(f"   File 2: {file2}")
    
    choice = show_simple_options()
    
    if choice == "1":
        print(f"✅ Keeping version from {file1}")
        return code1
    elif choice == "2":
        print(f"✅ Keeping version from {file2}")
        return code2
    elif choice == "3":
        print("🔧 Creating shared function...")
        return "shared_function()"
    else:
        print("⏭️ Skipping - keeping all versions")
        return None

# Usage example:
# result = handle_similar_code(code1, code2, "file1.py", "file2.py") 