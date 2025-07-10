#!/usr/bin/env python3
"""
Code Options Utility - Shows options for similar/repeating code patterns
"""

import os
import re
import difflib
from typing import List, Dict, Tuple

class CodeOptionsFinder:
    def __init__(self, project_path: str = "."):
        self.project_path = project_path
        self.code_patterns = {}
    
    def find_similar_patterns(self, min_similarity: float = 0.8) -> Dict[str, List[Tuple[str, str, float]]]:
        """
        Find similar code patterns across the project
        Returns: {pattern_id: [(file_path, code_snippet, similarity_score), ...]}
        """
        python_files = []
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        patterns = {}
        pattern_id = 0
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    # Find function definitions and similar blocks
                    for i, line in enumerate(lines):
                        if line.strip().startswith('def ') or line.strip().startswith('class '):
                            # Extract function/class block
                            block = self._extract_code_block(lines, i)
                            if len(block) > 3:  # Only consider substantial blocks
                                pattern_key = f"pattern_{pattern_id}"
                                patterns[pattern_key] = [(file_path, '\n'.join(block), 1.0)]
                                pattern_id += 1
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        # Find similar patterns
        similar_patterns = {}
        pattern_keys = list(patterns.keys())
        
        for i, key1 in enumerate(pattern_keys):
            for key2 in pattern_keys[i+1:]:
                code1 = patterns[key1][0][1]
                code2 = patterns[key2][0][1]
                
                similarity = difflib.SequenceMatcher(None, code1, code2).ratio()
                
                if similarity >= min_similarity:
                    group_key = f"similar_group_{len(similar_patterns)}"
                    if group_key not in similar_patterns:
                        similar_patterns[group_key] = []
                    
                    # Add both patterns to the group
                    if not any(code1 in item[1] for item in similar_patterns[group_key]):
                        similar_patterns[group_key].append(patterns[key1][0])
                    if not any(code2 in item[1] for item in similar_patterns[group_key]):
                        similar_patterns[group_key].append(patterns[key2][0])
        
        return similar_patterns
    
    def _extract_code_block(self, lines: List[str], start_line: int) -> List[str]:
        """Extract a complete code block starting from start_line"""
        block = []
        indent_level = None
        
        for i in range(start_line, len(lines)):
            line = lines[i]
            
            # Determine initial indent level
            if indent_level is None and line.strip():
                indent_level = len(line) - len(line.lstrip())
                block.append(line)
            elif indent_level is not None:
                if line.strip() == "":
                    block.append(line)
                elif len(line) - len(line.lstrip()) >= indent_level:
                    block.append(line)
                else:
                    break
        
        return block
    
    def show_options(self, similar_patterns: Dict[str, List[Tuple[str, str, float]]]):
        """Display options for similar code patterns"""
        print("🔍 Found similar code patterns:")
        print("=" * 50)
        
        for group_id, patterns in similar_patterns.items():
            if len(patterns) > 1:
                print(f"\n📁 Group: {group_id}")
                print(f"📊 Found {len(patterns)} similar patterns:")
                
                for i, (file_path, code, similarity) in enumerate(patterns, 1):
                    print(f"\n{i}. File: {file_path}")
                    print(f"   Similarity: {similarity:.2%}")
                    print(f"   Code Preview:")
                    print("   " + "-" * 40)
                    
                    # Show first few lines
                    lines = code.split('\n')
                    for j, line in enumerate(lines[:5]):
                        print(f"   {line}")
                    if len(lines) > 5:
                        print(f"   ... ({len(lines) - 5} more lines)")
                    print("   " + "-" * 40)
                
                print(f"\n💡 Options:")
                print(f"   1. Keep all versions (current)")
                print(f"   2. Create a shared function/class")
                print(f"   3. Choose one version to use everywhere")
                print(f"   4. Skip this group")
                
                choice = input(f"\n🎯 Choose option (1-4) for {group_id}: ").strip()
                
                if choice == "2":
                    self._create_shared_code(patterns)
                elif choice == "3":
                    self._choose_one_version(patterns)
    
    def _create_shared_code(self, patterns: List[Tuple[str, str, float]]):
        """Create a shared function/class for similar code"""
        print("\n🔧 Creating shared code...")
        
        # Analyze the patterns to find common structure
        common_lines = self._find_common_structure(patterns)
        
        if common_lines:
            shared_code = self._generate_shared_function(common_lines)
            
            # Create a new utility file
            utility_file = "shared_utils.py"
            with open(utility_file, 'w') as f:
                f.write(shared_code)
            
            print(f"✅ Created shared code in {utility_file}")
            print("📝 You can now import and use this shared function")
    
    def _find_common_structure(self, patterns: List[Tuple[str, str, float]]) -> List[str]:
        """Find common structure in similar patterns"""
        # Simple implementation - find lines that appear in most patterns
        line_counts = {}
        
        for _, code, _ in patterns:
            lines = code.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    line_counts[line] = line_counts.get(line, 0) + 1
        
        # Return lines that appear in at least 50% of patterns
        threshold = len(patterns) * 0.5
        common_lines = [line for line, count in line_counts.items() if count >= threshold]
        
        return common_lines
    
    def _generate_shared_function(self, common_lines: List[str]) -> str:
        """Generate a shared function from common lines"""
        return f'''"""
Shared utility functions for common code patterns
Generated automatically by CodeOptionsFinder
"""

def shared_function():
    """
    Shared function for common code pattern
    """
    # Common code structure:
{chr(10).join(f"    # {line}" for line in common_lines[:10])}
    pass

# Add more shared functions as needed
'''
    
    def _choose_one_version(self, patterns: List[Tuple[str, str, float]]):
        """Let user choose one version to use everywhere"""
        print("\n🎯 Choose which version to use everywhere:")
        
        for i, (file_path, code, similarity) in enumerate(patterns, 1):
            print(f"\n{i}. {file_path}")
            lines = code.split('\n')
            for j, line in enumerate(lines[:3]):
                print(f"   {line}")
            if len(lines) > 3:
                print(f"   ...")
        
        choice = input(f"\nEnter choice (1-{len(patterns)}): ").strip()
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(patterns):
                selected_pattern = patterns[choice_idx]
                print(f"\n✅ Selected: {selected_pattern[0]}")
                print("📝 You can now replace other similar patterns with this version")
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Invalid input")

def main():
    """Main function to run the code options finder"""
    finder = CodeOptionsFinder()
    
    print("🔍 Scanning for similar code patterns...")
    similar_patterns = finder.find_similar_patterns()
    
    if similar_patterns:
        finder.show_options(similar_patterns)
    else:
        print("✅ No similar code patterns found!")

if __name__ == "__main__":
    main() 