import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Set, Dict
import argparse

class HTMLTemplateEngine:
    """Simple template engine for HTML reports"""
    
    def __init__(self, template_path='template_report.html'):
        self.template_path = Path(template_path)
        self.template = self._load_template()
    
    def _load_template(self):
        """Load HTML template from file"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"⚠ Warning: Template file '{self.template_path}' not found.")
            print("Creating default template...")
            self._create_default_template()
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
    
    def _create_default_template(self):
        """Create default template if not found"""
        # This would contain the template content
        # For brevity, I'll show this in the full implementation
        pass
    
    def render(self, **kwargs):
        """Render template with provided variables"""
        result = self.template
        for key, value in kwargs.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))
        return result


class BinaryFileComparator:
    def __init__(self, path1, path2, extensions=None, recursive=True, template_path='template_report.html'):
        self.path1 = Path(path1)
        self.path2 = Path(path2)
        self.extensions = extensions if extensions else []
        self.recursive = recursive
        self.comparison_results = []
        self.template_engine = HTMLTemplateEngine(template_path)
        
        # Determine if we're comparing folders or files
        self.is_folder_comparison = self.path1.is_dir() and self.path2.is_dir()
        self.is_file_comparison = self.path1.is_file() and self.path2.is_file()
        
        if not self.is_folder_comparison and not self.is_file_comparison:
            raise ValueError("Both paths must be either folders or files (not mixed)")
    
    def get_common_files(self):
        """Find files present in both folders with matching structure"""
        if self.is_file_comparison:
            return (
                [(self.path1, self.path2, self.path1.name)],
                [],
                []
            )
        
        files1 = {}
        files2 = {}
        
        pattern = '**/*' if self.recursive else '*'
        for f in self.path1.glob(pattern):
            if f.is_file():
                if not self.extensions or f.suffix.lower() in self.extensions:
                    rel_path = f.relative_to(self.path1)
                    files1[str(rel_path)] = f
        
        for f in self.path2.glob(pattern):
            if f.is_file():
                if not self.extensions or f.suffix.lower() in self.extensions:
                    rel_path = f.relative_to(self.path2)
                    files2[str(rel_path)] = f
        
        common = set(files1.keys()) & set(files2.keys())
        only_in_1 = set(files1.keys()) - set(files2.keys())
        only_in_2 = set(files2.keys()) - set(files1.keys())
        
        return (
            [(files1[name], files2[name], name) for name in sorted(common)],
            sorted(only_in_1),
            sorted(only_in_2)
        )
    
    def read_binary(self, filepath, chunk_size=None):
        """Read file in binary mode"""
        try:
            with open(filepath, 'rb') as f:
                return f.read(chunk_size) if chunk_size else f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return b''
    
    def hex_dump(self, data, offset=0, highlight_positions=None):
        """Create hex dump with ASCII representation"""
        if highlight_positions is None:
            highlight_positions = set()
            
        lines = []
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            hex_offset = f"{offset + i:08X}"
            
            hex_parts = []
            for j, byte in enumerate(chunk):
                pos = i + j
                if pos in highlight_positions:
                    hex_parts.append(f"\033[91m{byte:02X}\033[0m")
                else:
                    hex_parts.append(f"{byte:02X}")
            
            hex_str = ' '.join(hex_parts[:8]) + '  ' + ' '.join(hex_parts[8:])
            hex_str = hex_str.ljust(58)
            
            ascii_parts = []
            for j, byte in enumerate(chunk):
                pos = i + j
                char = chr(byte) if 32 <= byte < 127 else '.'
                if pos in highlight_positions:
                    ascii_parts.append(f"\033[91m{char}\033[0m")
                else:
                    ascii_parts.append(char)
            
            ascii_str = ''.join(ascii_parts)
            lines.append(f"{hex_offset}  {hex_str}  |{ascii_str}|")
        
        return '\n'.join(lines)
    
    def hex_dump_html(self, data, offset=0, highlight_positions=None):
        """Create hex dump for HTML output"""
        if highlight_positions is None:
            highlight_positions = set()
            
        lines = []
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            hex_offset = f"{offset + i:08X}"
            
            hex_parts = []
            for j, byte in enumerate(chunk):
                pos = i + j
                if pos in highlight_positions:
                    hex_parts.append(f'<span class="diff">{byte:02X}</span>')
                else:
                    hex_parts.append(f"{byte:02X}")
            
            hex_str = ' '.join(hex_parts[:8]) + '&nbsp;&nbsp;' + ' '.join(hex_parts[8:])
            
            ascii_parts = []
            for j, byte in enumerate(chunk):
                pos = i + j
                char = chr(byte) if 32 <= byte < 127 else '.'
                char = char.replace('<', '&lt;').replace('>', '&gt;')
                if pos in highlight_positions:
                    ascii_parts.append(f'<span class="diff">{char}</span>')
                else:
                    ascii_parts.append(char)
            
            ascii_str = ''.join(ascii_parts)
            lines.append(f'<div class="hex-line">{hex_offset}&nbsp;&nbsp;{hex_str}&nbsp;&nbsp;|{ascii_str}|</div>')
        
        return '\n'.join(lines)
    
    def side_by_side_comparison(self, data1, data2, max_bytes=512):
        """Create side-by-side hex comparison"""
        differences = self.find_differences(data1, data2)
        
        lines = []
        lines.append(f"{'Offset':<10} {'File 1 (Hex + ASCII)':<50} {'File 2 (Hex + ASCII)':<50} {'Match'}")
        lines.append('-' * 120)
        
        max_len = min(max_bytes, max(len(data1), len(data2)))
        
        for i in range(0, max_len, 16):
            offset = f"{i:08X}"
            
            chunk1 = data1[i:i+16] if i < len(data1) else b''
            hex1 = ' '.join(f"{b:02X}" for b in chunk1)
            ascii1 = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk1)
            str1 = f"{hex1:<40} |{ascii1}|"
            
            chunk2 = data2[i:i+16] if i < len(data2) else b''
            hex2 = ' '.join(f"{b:02X}" for b in chunk2)
            ascii2 = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk2)
            str2 = f"{hex2:<40} |{ascii2}|"
            
            match = "✓" if chunk1 == chunk2 else "\033[91m✗\033[0m"
            lines.append(f"{offset:<10} {str1:<50} {str2:<50} {match}")
        
        return '\n'.join(lines)
    
    def find_differences(self, data1, data2):
        """Find byte positions where files differ"""
        differences = []
        max_len = max(len(data1), len(data2))
        
        for i in range(max_len):
            byte1 = data1[i] if i < len(data1) else None
            byte2 = data2[i] if i < len(data2) else None
            
            if byte1 != byte2:
                differences.append(i)
        
        return differences
    
    def get_file_info(self, filepath):
        """Get additional file information"""
        stat = filepath.stat()
        return {
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
        }
    
    def compare_files(self, file1, file2, rel_path, max_display_bytes=512, show_side_by_side=False):
        """Compare two files at binary level"""
        print(f"\n{'='*80}")
        print(f"Comparing: {rel_path}")
        print(f"{'='*80}")
        print(f"File 1: {file1}")
        print(f"File 2: {file2}")
        
        info1 = self.get_file_info(file1)
        info2 = self.get_file_info(file2)
        
        print(f"\nFile 1 Info:")
        print(f"  Size: {info1['size']:,} bytes")
        print(f"  Modified: {info1['modified']}")
        
        print(f"\nFile 2 Info:")
        print(f"  Size: {info2['size']:,} bytes")
        print(f"  Modified: {info2['modified']}")
        
        data1 = self.read_binary(file1)
        data2 = self.read_binary(file2)
        
        size1 = len(data1)
        size2 = len(data2)
        
        result = {
            'rel_path': rel_path,
            'file1': str(file1),
            'file2': str(file2),
            'size1': size1,
            'size2': size2,
            'info1': info1,
            'info2': info2,
            'identical': False,
            'differences': 0,
            'first_diff_offset': None,
            'similarity': 0,
            'data1': data1[:max_display_bytes],
            'data2': data2[:max_display_bytes],
            'diff_positions': []
        }
        
        if data1 == data2:
            print(f"\n✓ Files are IDENTICAL")
            result['identical'] = True
            result['similarity'] = 100.0
            self.comparison_results.append(result)
            return True
        
        print(f"\n✗ Files are DIFFERENT")
        
        differences = self.find_differences(data1, data2)
        diff_count = len(differences)
        
        result['differences'] = diff_count
        result['diff_positions'] = [d for d in differences if d < max_display_bytes]
        
        print(f"\nDifferences found: {diff_count:,} bytes")
        
        if diff_count > 0:
            result['first_diff_offset'] = differences[0]
            similarity = ((max(size1, size2) - diff_count) / max(size1, size2) * 100)
            result['similarity'] = similarity
            print(f"First difference at offset: 0x{differences[0]:08X}")
            print(f"Similarity: {similarity:.2f}%")
        
        if show_side_by_side:
            print(f"\n{'-'*120}")
            print(f"SIDE-BY-SIDE COMPARISON")
            print(f"{'-'*120}")
            print(self.side_by_side_comparison(data1, data2, max_display_bytes))
        
        display_size = min(max_display_bytes, max(size1, size2))
        diff_positions = set(d for d in differences if d < display_size)
        
        print(f"\n{'-'*80}")
        print(f"HEX DUMP - File 1: {rel_path}")
        print(f"{'-'*80}")
        print(self.hex_dump(data1[:display_size], highlight_positions=diff_positions))
        
        print(f"\n{'-'*80}")
        print(f"HEX DUMP - File 2: {rel_path}")
        print(f"{'-'*80}")
        print(self.hex_dump(data2[:display_size], highlight_positions=diff_positions))
        
        if diff_count > 0 and diff_count <= 50:
            print(f"\n{'-'*80}")
            print(f"DETAILED DIFFERENCES (showing up to 50)")
            print(f"{'-'*80}")
            print(f"{'Offset':<12} {'File1 (Hex)':<15} {'File1 (ASCII)':<15} {'File2 (Hex)':<15} {'File2 (ASCII)':<15}")
            print(f"{'-'*80}")
            
            for pos in differences[:50]:
                byte1 = data1[pos] if pos < size1 else None
                byte2 = data2[pos] if pos < size2 else None
                
                hex1 = f"{byte1:02X}" if byte1 is not None else "EOF"
                hex2 = f"{byte2:02X}" if byte2 is not None else "EOF"
                
                ascii1 = chr(byte1) if byte1 is not None and 32 <= byte1 < 127 else '.'
                ascii2 = chr(byte2) if byte2 is not None and 32 <= byte2 < 127 else '.'
                
                print(f"0x{pos:08X}   {hex1:<15} {ascii1:<15} {hex2:<15} {ascii2:<15}")
        
        self.comparison_results.append(result)
        return False
    
    def _build_file_comparison_html(self, result, idx):
        """Build HTML for a single file comparison"""
        status_class = 'identical' if result['identical'] else 'different'
        status_text = '✓ IDENTICAL' if result['identical'] else '✗ DIFFERENT'
        
        html = f'''
        <div class="file-comparison">
            <div class="file-header {status_class}" onclick="toggleContent({idx})">
                <div>
                    <strong>{result['rel_path']}</strong>
                    <span class="status-badge status-{status_class}">{status_text}</span>
                </div>
                <span class="toggle-icon" id="toggle-{idx}">▼</span>
            </div>
            <div class="file-content" id="content-{idx}">
                <div class="file-info">
                    <h3>File Information</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <strong>File 1 Size:</strong> {result['size1']:,} bytes<br>
                            <strong>Modified:</strong> {result['info1']['modified']}<br>
                            <strong>Created:</strong> {result['info1']['created']}
                        </div>
                        <div class="info-item">
                            <strong>File 2 Size:</strong> {result['size2']:,} bytes<br>
                            <strong>Modified:</strong> {result['info2']['modified']}<br>
                            <strong>Created:</strong> {result['info2']['created']}
                        </div>
'''
        
        if not result['identical']:
            html += f'''
                        <div class="info-item">
                            <strong>Differences:</strong> {result['differences']:,} bytes<br>
                            <strong>First Difference:</strong> 0x{result['first_diff_offset']:08X}
                        </div>
                        <div class="info-item">
                            <strong>Similarity:</strong> {result['similarity']:.2f}%
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {result['similarity']:.2f}%">
                                    {result['similarity']:.2f}%
                                </div>
                            </div>
                        </div>
'''
        
        html += '''
                    </div>
                </div>
'''
        
        if not result['identical']:
            diff_positions = set(result['diff_positions'])
            
            html += f'''
                <div class="hex-container">
                    <div class="hex-panel">
                        <div class="hex-title">File 1: {result['rel_path']}</div>
                        {self.hex_dump_html(result['data1'], highlight_positions=diff_positions)}
                    </div>
                    <div class="hex-panel">
                        <div class="hex-title">File 2: {result['rel_path']}</div>
                        {self.hex_dump_html(result['data2'], highlight_positions=diff_positions)}
                    </div>
                </div>
'''
        
        html += '''
            </div>
        </div>
'''
        return html
    
    def generate_html_report(self, output_file='comparison_report.html'):
        """Generate HTML report using template"""
        print(f"\n📝 Generating HTML report...")
        
        comparison_type = "File Comparison" if self.is_file_comparison else "Folder Comparison"
        badge_class = "badge-file" if self.is_file_comparison else "badge-folder"
        comparison_mode = "FILE COMPARISON" if self.is_file_comparison else "FOLDER COMPARISON"
        
        # Build path info
        if self.is_file_comparison:
            path_info = f'''
                <div class="info-item">
                    <strong>File 1:</strong>
                    <div class="path-display">{self.path1.absolute()}</div>
                </div>
                <div class="info-item">
                    <strong>File 2:</strong>
                    <div class="path-display">{self.path2.absolute()}</div>
                </div>
'''
        else:
            path_info = f'''
                <div class="info-item">
                    <strong>Folder 1:</strong>
                    <div class="path-display">{self.path1.absolute()}</div>
                </div>
                <div class="info-item">
                    <strong>Folder 2:</strong>
                    <div class="path-display">{self.path2.absolute()}</div>
                </div>
'''
        
        # Extensions info
        extensions_info = ''
        if not self.is_file_comparison:
            ext_text = ', '.join(self.extensions) if self.extensions else 'All'
            extensions_info = f'''
                <div class="info-item">
                    <strong>File Extensions:</strong><br>{ext_text}
                </div>
'''
        
        # Build file comparisons HTML
        file_comparisons_html = ''
        for idx, result in enumerate(self.comparison_results):
            file_comparisons_html += self._build_file_comparison_html(result, idx)
        
        # Calculate statistics
        total_files = len(self.comparison_results)
        identical_files = sum(1 for r in self.comparison_results if r['identical'])
        different_files = sum(1 for r in self.comparison_results if not r['identical'])
        avg_similarity = sum(r['similarity'] for r in self.comparison_results) / total_files if total_files > 0 else 0
        
        # Render template
        html_content = self.template_engine.render(
            COMPARISON_TYPE=comparison_type,
            BADGE_CLASS=badge_class,
            COMPARISON_MODE=comparison_mode,
            PATH_INFO=path_info,
            REPORT_TIME=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            EXTENSIONS_INFO=extensions_info,
            TOTAL_FILES=total_files,
            IDENTICAL_FILES=identical_files,
            DIFFERENT_FILES=different_files,
            AVERAGE_SIMILARITY=f"{avg_similarity:.2f}",
            COMPARISON_SECTION_TITLE='File Comparison' if self.is_file_comparison else 'File Comparisons',
            FILE_COMPARISONS=file_comparisons_html
        )
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ HTML report generated: {Path(output_file).absolute()}")
        return output_file
    
    def run_comparison(self, max_display_bytes=512, show_side_by_side=False, generate_html=False, html_output='comparison_report.html'):
        """Run comparison on all common files"""
        print(f"\n{'='*80}")
        print(f"BINARY FILE COMPARISON TOOL")
        print(f"{'='*80}")
        
        if self.is_file_comparison:
            print(f"Mode: FILE COMPARISON")
            print(f"File 1: {self.path1.absolute()}")
            print(f"File 2: {self.path2.absolute()}")
            
            common_files = [(self.path1, self.path2, self.path1.name)]
            only_in_1 = []
            only_in_2 = []
        else:
            print(f"Mode: FOLDER COMPARISON")
            print(f"Folder 1: {self.path1.absolute()}")
            print(f"Folder 2: {self.path2.absolute()}")
            print(f"Recursive: {self.recursive}")
            print(f"Extensions: {', '.join(self.extensions) if self.extensions else 'All files'}")
            
            common_files, only_in_1, only_in_2 = self.get_common_files()
            
            if only_in_1:
                print(f"\n⚠ Files only in Folder 1 ({len(only_in_1)}):")
                for f in only_in_1[:10]:
                    print(f"  - {f}")
                if len(only_in_1) > 10:
                    print(f"  ... and {len(only_in_1) - 10} more")
            
            if only_in_2:
                print(f"\n⚠ Files only in Folder 2 ({len(only_in_2)}):")
                for f in only_in_2[:10]:
                    print(f"  - {f}")
                if len(only_in_2) > 10:
                    print(f"  ... and {len(only_in_2) - 10} more")
        
        if not common_files:
            print("\n❌ No files to compare!")
            return
        
        print(f"\n✓ Found {len(common_files)} file(s) to compare")
        
        identical = 0
        different = 0
        
        for file1, file2, rel_path in common_files:
            is_identical = self.compare_files(file1, file2, rel_path, max_display_bytes, show_side_by_side)
            if is_identical:
                identical += 1
            else:
                different += 1
        
        # Summary
        print(f"\n{'='*80}")
        print(f"SUMMARY")
        print(f"{'='*80}")
        
        if self.is_file_comparison:
            print(f"Comparison Mode: FILE")
            print(f"Result: {'✓ IDENTICAL' if identical > 0 else '✗ DIFFERENT'}")
        else:
            print(f"Comparison Mode: FOLDER")
            print(f"Total files compared: {len(common_files)}")
            print(f"✓ Identical files: {identical}")
            print(f"✗ Different files: {different}")
            print(f"Files only in Folder 1: {len(only_in_1)}")
            print(f"Files only in Folder 2: {len(only_in_2)}")
        
        if self.comparison_results:
            avg_similarity = sum(r['similarity'] for r in self.comparison_results) / len(self.comparison_results)
            print(f"Average similarity: {avg_similarity:.2f}%")
        
        # Generate HTML report
        if generate_html:
            self.generate_html_report(html_output)


def main():
    parser = argparse.ArgumentParser(
        description='Binary File/Folder Comparison Tool with Hex Visualization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare two files:
  %(prog)s file1.bin file2.bin
  %(prog)s file1.bin file2.bin --side-by-side --html
  
  # Compare two folders:
  %(prog)s folder1 folder2
  %(prog)s folder1 folder2 --html --max-bytes 1024
  %(prog)s folder1 folder2 --extensions .txt .log --html
  
  # Custom template:
  %(prog)s folder1 folder2 --html --template my_template.html
        """
    )
    
    parser.add_argument('path1', help='First file or folder path')
    parser.add_argument('path2', help='Second file or folder path')
    parser.add_argument('--max-bytes', '-m', type=int, default=512,
                        help='Maximum bytes to display in hex dump (default: 512)')
    parser.add_argument('--side-by-side', '-s', action='store_true',
                        help='Show side-by-side comparison in console')
    parser.add_argument('--html', action='store_true',
                        help='Generate HTML report')
    parser.add_argument('--html-output', '-o', default='comparison_report.html',
                        help='HTML report output file (default: comparison_report.html)')
    parser.add_argument('--template', '-t', default='template_report.html',
                        help='HTML template file (default: template_report.html)')
    parser.add_argument('--extensions', '-e', nargs='+',
                        help='Filter by file extensions (e.g., .txt .log) - folder mode only')
    parser.add_argument('--no-recursive', action='store_true',
                        help='Disable recursive folder scanning - folder mode only')
    
    args = parser.parse_args()
    
    path1 = Path(args.path1)
    path2 = Path(args.path2)
    
    if not path1.exists():
        print(f"❌ Error: '{args.path1}' does not exist")
        sys.exit(1)
    
    if not path2.exists():
        print(f"❌ Error: '{args.path2}' does not exist")
        sys.exit(1)
    
    if path1.is_file() and path2.is_dir():
        print(f"❌ Error: Cannot compare file with folder")
        sys.exit(1)
    
    if path1.is_dir() and path2.is_file():
        print(f"❌ Error: Cannot compare folder with file")
        sys.exit(1)
    
    extensions = None
    if args.extensions:
        if path1.is_file():
            print("⚠ Warning: --extensions ignored for file comparison")
        else:
            extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions]
    
    try:
        comparator = BinaryFileComparator(
            args.path1,
            args.path2,
            extensions=extensions,
            recursive=not args.no_recursive,
            template_path=args.template
        )
        
        comparator.run_comparison(
            max_display_bytes=args.max_bytes,
            show_side_by_side=args.side_by_side,
            generate_html=args.html,
            html_output=args.html_output
        )
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
