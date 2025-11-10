# 📊 BIN-Eye Comparison Tool

## Developed by 'claude-sonnet-4-5-20250929-thinking-32k' on https://lmareana.ai, Assisted by TinToSer


A powerful Python-based tool for binary-level file and folder comparison with hex visualization, difference highlighting, and beautiful HTML reports.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📑 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
  - [File Comparison](#1-file-comparison)
  - [Folder Comparison](#2-folder-comparison)
  - [Advanced Options](#3-advanced-options)
- [Command Line Arguments](#-command-line-arguments)
- [Output Examples](#-output-examples)
- [HTML Template Customization](#-html-template-customization)
- [Use Cases](#-use-cases)
- [Benefits](#-benefits)
- [Technical Details](#-technical-details)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Features
- ✅ **Dual Mode Operation**: Compare individual files OR entire folder structures
- ✅ **Binary Level Comparison**: Byte-by-byte comparison with precise difference detection
- ✅ **Hex Visualization**: Standard hexdump format with ASCII representation
- ✅ **Difference Highlighting**: Visual highlighting of differing bytes (console & HTML)
- ✅ **Side-by-Side View**: Compare files side-by-side in the terminal
- ✅ **HTML Reports**: Professional, interactive HTML reports with modern UI
- ✅ **Template-Based**: Separate HTML template for easy customization
- ✅ **Recursive Scanning**: Deep folder comparison with subfolder support
- ✅ **File Filtering**: Filter by file extensions
- ✅ **Similarity Analysis**: Percentage-based similarity metrics
- ✅ **File Metadata**: Display file size, creation, and modification dates

### Advanced Features
- 📈 **Statistical Analysis**: Comprehensive comparison statistics
- 🎨 **Color-Coded Output**: Terminal colors for better readability
- 📱 **Responsive HTML**: Mobile-friendly HTML reports
- 🔍 **First Difference Detection**: Quickly locate where files start to differ
- 📊 **Progress Bars**: Visual similarity indicators in HTML reports
- 🗂️ **Folder Structure Matching**: Preserves relative paths in folder comparison
- ⚡ **Efficient Processing**: Optimized for large files and folders
- 🎯 **Auto-Expand**: HTML reports auto-expand first different file

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Setup

1. **Clone or Download**
   ```bash
   git clone https://github.com/TinToSer/bin-eye-comparison.git
   cd bin-eye-comparison
   ```

2. **Verify Installation**
   ```bash
   python BIN_Eye_Comparator.py --help
   ```

3. **File Structure**
   ```
   bin-eye-comparison/
   ├── BIN_Eye_Comparator.py      # Main script
   ├── template_report.html   # HTML template (auto-created if missing)
   └── README.md             # This file
   ```

---

## 🎯 Quick Start

### Compare Two Files
```bash
python BIN_Eye_Comparator.py file1.txt file2.txt
```

### Compare Two Folders with HTML Report
```bash
python BIN_Eye_Comparator.py folder1 folder2 --html
```

### Compare with All Features Enabled
```bash
python BIN_Eye_Comparator.py folder1 folder2 --side-by-side --html --max-bytes 2048
```

---

## 📖 Usage

### 1. File Comparison

#### Basic File Comparison
```bash
python BIN_Eye_Comparator.py document1.pdf document2.pdf
```

**Output:**
- File size information
- Identical/Different status
- Hex dump of both files
- Highlighted differences
- Byte-by-byte difference table (if < 50 differences)

#### File Comparison with Side-by-Side View
```bash
python BIN_Eye_Comparator.py image1.png image2.png --side-by-side
```

**Features:**
- Line-by-line hex comparison
- Match indicators (✓/✗)
- Synchronized offsets

#### File Comparison with HTML Report
```bash
python BIN_Eye_Comparator.py binary1.exe binary2.exe --html
```

**Generates:**
- Interactive HTML report
- Collapsible sections
- Hex dumps with highlighting
- Similarity progress bar

#### Advanced File Comparison
```bash
python BIN_Eye_Comparator.py large_file1.dat large_file2.dat \
  --max-bytes 4096 \
  --side-by-side \
  --html \
  --html-output detailed_report.html
```

---

### 2. Folder Comparison

#### Basic Folder Comparison
```bash
python BIN_Eye_Comparator.py /path/to/folder1 /path/to/folder2
```

**Features:**
- Finds all common files
- Lists files unique to each folder
- Compares matching files
- Summary statistics

#### Folder Comparison with Extension Filter
```bash
python BIN_Eye_Comparator.py folder1 folder2 --extensions .txt .log .dat
```

**Use Case:** Compare only specific file types

#### Non-Recursive Comparison (Top Level Only)
```bash
python BIN_Eye_Comparator.py folder1 folder2 --no-recursive
```

**Use Case:** Skip subdirectories

#### Complete Folder Analysis
```bash
python BIN_Eye_Comparator.py project_v1 project_v2 \
  --extensions .py .js .css \
  --html \
  --html-output project_comparison.html \
  --max-bytes 2048
```

---

### 3. Advanced Options

#### Custom Hex Display Size
```bash
# Display first 1024 bytes
python BIN_Eye_Comparator.py file1 file2 --max-bytes 1024

# Display first 8192 bytes (8KB)
python BIN_Eye_Comparator.py file1 file2 --max-bytes 8192
```

#### Custom HTML Template
```bash
python BIN_Eye_Comparator.py folder1 folder2 \
  --html \
  --template custom_template.html \
  --html-output report.html
```

#### Multiple Extensions
```bash
python BIN_Eye_Comparator.py logs_old logs_new \
  --extensions .log .txt .out .err \
  --html
```

#### Side-by-Side + HTML
```bash
python BIN_Eye_Comparator.py data1 data2 \
  --side-by-side \
  --html \
  --max-bytes 512
```

---

## 🎛️ Command Line Arguments

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `path1` | - | Required | - | First file or folder path |
| `path2` | - | Required | - | Second file or folder path |
| `--max-bytes` | `-m` | Integer | 512 | Maximum bytes to display in hex dump |
| `--side-by-side` | `-s` | Flag | False | Show side-by-side comparison in console |
| `--html` | - | Flag | False | Generate HTML report |
| `--html-output` | `-o` | String | comparison_report.html | Output filename for HTML report |
| `--template` | `-t` | String | template_report.html | HTML template file path |
| `--extensions` | `-e` | List | All | File extensions to compare (folder mode) |
| `--no-recursive` | - | Flag | False | Disable recursive folder scanning |

### Argument Details

#### `path1` and `path2`
- **Required**: Yes
- **Type**: File or folder path
- **Rules**: 
  - Both must be files OR both must be folders
  - Cannot mix file and folder
  - Paths must exist

#### `--max-bytes` / `-m`
- **Type**: Integer
- **Default**: 512
- **Range**: 1 to file size
- **Purpose**: Control how many bytes to display in hex dumps
- **Example**: 
  ```bash
  --max-bytes 1024  # Display first 1KB
  --max-bytes 4096  # Display first 4KB
  ```

#### `--side-by-side` / `-s`
- **Type**: Boolean flag
- **Purpose**: Show aligned hex comparison in terminal
- **Output**: 120-character wide comparison table
- **Best For**: Terminal comparison of small files

#### `--html`
- **Type**: Boolean flag
- **Purpose**: Generate HTML report
- **Output**: Creates interactive HTML file
- **Features**: 
  - Collapsible sections
  - Color-coded differences
  - Similarity progress bars
  - Mobile responsive

#### `--html-output` / `-o`
- **Type**: String (filename)
- **Default**: `comparison_report.html`
- **Purpose**: Specify output HTML filename
- **Example**: 
  ```bash
  --html-output my_report.html
  --html-output reports/comparison_$(date +%Y%m%d).html
  ```

#### `--template` / `-t`
- **Type**: String (filepath)
- **Default**: `template_report.html`
- **Purpose**: Use custom HTML template
- **Auto-Creation**: Creates default template if missing
- **Use Case**: Custom branding, different layouts

#### `--extensions` / `-e`
- **Type**: Space-separated list
- **Folder Mode Only**: Ignored for file comparison
- **Format**: With or without leading dot
- **Examples**:
  ```bash
  --extensions .txt .log
  --extensions txt log dat
  --extensions .py .js .css .html
  ```

#### `--no-recursive`
- **Type**: Boolean flag
- **Folder Mode Only**: Ignored for file comparison
- **Purpose**: Compare only top-level files
- **Use Case**: Avoid deep folder traversal

---

## 📊 Output Examples

### Console Output

```
================================================================================
BINARY FILE COMPARISON TOOL
================================================================================
Mode: FILE COMPARISON
File 1: /home/user/file1.bin
File 2: /home/user/file2.bin

✓ Found 1 file(s) to compare

================================================================================
Comparing: file1.bin
================================================================================
File 1: /home/user/file1.bin
File 2: /home/user/file2.bin

File 1 Info:
  Size: 1,024 bytes
  Modified: 2024-01-15 10:30:45

File 2 Info:
  Size: 1,024 bytes
  Modified: 2024-01-15 11:20:30

✗ Files are DIFFERENT

Differences found: 12 bytes
First difference at offset: 0x00000010
Similarity: 98.83%

--------------------------------------------------------------------------------
HEX DUMP - File 1: file1.bin
--------------------------------------------------------------------------------
00000000  48 65 6C 6C 6F 20 57 6F  72 6C 64 21 0A 54 68 69  |Hello World!.Thi|
00000010  73 20 69 73 20 61 20 74  65 73 74 20 66 69 6C 65  |s is a test file|
00000020  2E 0A 42 69 6E 61 72 79  20 63 6F 6D 70 61 72 69  |..Binary compari|

--------------------------------------------------------------------------------
DETAILED DIFFERENCES (showing up to 50)
--------------------------------------------------------------------------------
Offset       File1 (Hex)     File1 (ASCII)   File2 (Hex)     File2 (ASCII)
--------------------------------------------------------------------------------
0x00000010   73              s               74              t
0x00000015   61              a               62              b

================================================================================
SUMMARY
================================================================================
Comparison Mode: FILE
Result: ✗ DIFFERENT
Average similarity: 98.83%
```

### HTML Report Features

1. **Interactive Headers**
   - Click to expand/collapse file details
   - Auto-expand first different file
   - Smooth animations

2. **Visual Elements**
   - Color-coded status badges (green/red)
   - Progress bars showing similarity
   - Highlighted differences in hex dumps

3. **Information Panels**
   - File paths and sizes
   - Creation and modification times
   - Difference counts and locations

4. **Hex Dumps**
   - Side-by-side layout
   - Dark theme for better readability
   - Red highlighting for differences
   - ASCII representation

---

## 🎨 HTML Template Customization

### Template Structure

The `template_report.html` uses placeholder syntax: `{{VARIABLE_NAME}}`

### Available Placeholders

| Placeholder | Description | Example Value |
|------------|-------------|---------------|
| `{{COMPARISON_TYPE}}` | Type of comparison | "File Comparison" |
| `{{BADGE_CLASS}}` | CSS class for badge | "badge-file" |
| `{{COMPARISON_MODE}}` | Mode text | "FILE COMPARISON" |
| `{{PATH_INFO}}` | HTML for path display | File/folder paths |
| `{{REPORT_TIME}}` | Generation timestamp | "2024-01-15 14:30:00" |
| `{{EXTENSIONS_INFO}}` | Extension filter info | ".txt, .log" |
| `{{TOTAL_FILES}}` | Number of files compared | "5" |
| `{{IDENTICAL_FILES}}` | Number of identical files | "3" |
| `{{DIFFERENT_FILES}}` | Number of different files | "2" |
| `{{AVERAGE_SIMILARITY}}` | Average similarity | "95.50" |
| `{{FILE_COMPARISONS}}` | HTML for all comparisons | File comparison HTML |

### Customization Examples

#### 1. Change Color Scheme
```css
/* In template_report.html */
.file-header.different {
    background: #ff6b6b;  /* Custom red */
}

.file-header.identical {
    background: #51cf66;  /* Custom green */
}
```

#### 2. Add Company Logo
```html
<!-- In template_report.html, before h1 -->
<div class="logo">
    <img src="company-logo.png" alt="Company Logo">
</div>
```

#### 3. Custom Footer
```html
<!-- Replace footer section -->
<div class="footer">
    <p>© 2024 Your Company Name</p>
    <p>Generated by Binary Comparison Tool v1.0</p>
    <p>Contact: support@company.com</p>
</div>
```

#### 4. Dark Mode Support
```css
/* Add to style section */
@media (prefers-color-scheme: dark) {
    body {
        background: #1a1a1a;
        color: #e0e0e0;
    }
    
    .container {
        background: #2d2d2d;
    }
}
```

---

## 💼 Use Cases

### 1. Software Development

#### Version Comparison
```bash
# Compare compiled binaries
python BIN_Eye_Comparator.py build_v1.0/app.exe build_v2.0/app.exe --html

# Compare configuration files
python BIN_Eye_Comparator.py config_old config_new --extensions .conf .ini .xml
```

#### Build Verification
```bash
# Verify build reproducibility
python BIN_Eye_Comparator.py build1/output build2/output --html -o build_verification.html
```

### 2. Data Integrity

#### Backup Verification
```bash
# Verify backup integrity
python BIN_Eye_Comparator.py /data/original /backup/data --html
```

#### File Transfer Verification
```bash
# Verify file transfer
python BIN_Eye_Comparator.py local_file.dat remote_file.dat
```

### 3. Security & Forensics

#### Malware Analysis
```bash
# Compare suspicious files
python BIN_Eye_Comparator.py clean_file.exe suspicious_file.exe --side-by-side --html
```

#### System File Integrity
```bash
# Check system file modifications
python BIN_Eye_Comparator.py /system/original /system/current --extensions .dll .sys
```

### 4. Quality Assurance

#### Test Data Validation
```bash
# Compare test results
python BIN_Eye_Comparator.py expected_output actual_output --html
```

#### Database Dump Comparison
```bash
# Compare database exports
python BIN_Eye_Comparator.py dump_old.sql dump_new.sql --max-bytes 4096
```

### 5. Documentation

#### Archive Comparison
```bash
# Document differences between versions
python BIN_Eye_Comparator.py docs_v1 docs_v2 \
  --extensions .pdf .docx \
  --html \
  --html-output documentation_changes.html
```

### 6. Media & Assets

#### Image Comparison
```bash
# Compare image files
python BIN_Eye_Comparator.py images_original images_processed \
  --extensions .png .jpg .jpeg
```

#### Audio/Video Verification
```bash
# Compare media files
python BIN_Eye_Comparator.py master.mp4 encoded.mp4 --max-bytes 8192 --html
```

---

## 🏆 Benefits

### For Developers

1. **Debug Build Issues**
   - Quickly identify binary differences between builds
   - Verify compiler determinism
   - Track down unexpected changes

2. **Version Control**
   - Visual diff for binary files
   - Supplement to Git/SVN
   - Track binary asset changes

3. **Code Review**
   - Compare compiled outputs
   - Verify no unintended changes
   - Document binary modifications

### For QA Engineers

1. **Test Validation**
   - Verify test data integrity
   - Compare expected vs actual outputs
   - Document test discrepancies

2. **Regression Testing**
   - Detect unintended binary changes
   - Validate backwards compatibility
   - Track file format changes

3. **Automated Testing**
   - Integrate into CI/CD pipelines
   - Automated comparison reports
   - Pass/fail criteria based on similarity

### For System Administrators

1. **Backup Verification**
   - Ensure backup completeness
   - Verify file transfer integrity
   - Document backup differences

2. **System Monitoring**
   - Detect unauthorized file modifications
   - Track configuration changes
   - Security audit trail

3. **Migration Validation**
   - Verify data migration success
   - Compare before/after states
   - Document migration results

### For Security Professionals

1. **Malware Analysis**
   - Identify infected file modifications
   - Compare clean vs compromised files
   - Document malware behavior

2. **Forensics**
   - Detailed binary analysis
   - Evidence documentation
   - Timeline reconstruction

3. **Compliance**
   - File integrity verification
   - Audit documentation
   - Change tracking

### General Benefits

| Benefit | Description |
|---------|-------------|
| **Accuracy** | Byte-level precision, no false positives |
| **Speed** | Fast comparison even for large files |
| **Automation** | Command-line interface for scripting |
| **Documentation** | Professional HTML reports for stakeholders |
| **Portability** | Pure Python, works on Windows/Linux/Mac |
| **Flexibility** | File or folder mode, extensive filtering |
| **Visualization** | Hex dumps with ASCII, color highlighting |
| **Maintainability** | Separated template for easy customization |
| **No Dependencies** | Uses only Python standard library |
| **Open Source** | Fully customizable and extendable |

---

## 🔧 Technical Details

### Performance

- **Memory Efficient**: Reads files in chunks when needed
- **Fast Comparison**: Optimized byte-by-byte comparison
- **Scalable**: Handles folders with thousands of files
- **Large File Support**: No practical file size limit

### File Format Support

- **Universal**: Works with ANY file format (binary or text)
- **Common Formats**: 
  - Executables (.exe, .dll, .so)
  - Archives (.zip, .tar, .gz)
  - Media (.mp4, .png, .jpg, .mp3)
  - Documents (.pdf, .docx, .xlsx)
  - Databases (.db, .sqlite, .mdb)
  - And literally any other file type

### Output Formats

1. **Console Output**
   - ANSI color codes for highlighting
   - Formatted tables and hex dumps
   - Progress and status indicators

2. **HTML Output**
   - HTML5 compliant
   - CSS3 styling
   - JavaScript for interactivity
   - No external dependencies

### Comparison Algorithm

```python
# Pseudo-code
for each byte position i in max(file1_size, file2_size):
    byte1 = file1[i] if i < file1_size else None
    byte2 = file2[i] if i < file2_size else None
    
    if byte1 != byte2:
        mark_as_difference(i)

similarity = (1 - differences/max_size) * 100
```

### Hex Dump Format

```
Offset    Hex Bytes (8 + 8)                         ASCII
00000000  48 65 6C 6C 6F 20 57 6F  72 6C 64 21 0A 54 68 69  |Hello World!.Thi|
00000010  73 20 69 73 20 61 20 74  65 73 74 20 66 69 6C 65  |s is a test file|
```

- **Offset**: 8-digit hexadecimal address
- **Hex Bytes**: 16 bytes per line (8+8 with gap)
- **ASCII**: Printable characters or '.'

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Template Not Found

**Error:**
```
⚠ Warning: Template file 'template_report.html' not found.
Creating default template...
```

**Solution:** The tool auto-creates the template. No action needed.

#### 2. Cannot Compare File with Folder

**Error:**
```
❌ Error: Cannot compare file with folder
```

**Solution:** Ensure both paths are files OR both are folders.

#### 3. Permission Denied

**Error:**
```
Error reading /path/to/file: Permission denied
```

**Solution:** Check file permissions:
```bash
chmod +r file1.bin file2.bin
```

#### 4. Out of Memory (Large Files)

**Issue:** Comparing very large files (GB+) uses lots of RAM

**Solution:** Reduce `--max-bytes`:
```bash
python BIN_Eye_Comparator.py large1.dat large2.dat --max-bytes 1024
```

#### 5. No Common Files Found

**Output:**
```
❌ No common files found!
```

**Solution:** 
- Check folder paths
- Verify file extensions filter
- Check recursive setting

### Platform-Specific Issues

#### Windows

**Issue:** ANSI colors not working

**Solution:** 
- Use Windows Terminal or ConEmu
- Or redirect to HTML: `--html`

#### Linux/Mac

**Issue:** Permission denied on script

**Solution:**
```bash
chmod +x BIN_Eye_Comparator.py
```

---

## 📝 Examples Gallery

### Example 1: Simple File Comparison
```bash
python BIN_Eye_Comparator.py old_version.dll new_version.dll
```

### Example 2: Detailed File Analysis
```bash
python BIN_Eye_Comparator.py firmware_v1.bin firmware_v2.bin \
  --side-by-side \
  --html \
  --max-bytes 2048 \
  --html-output firmware_analysis.html
```

### Example 3: Folder Comparison with Filter
```bash
python BIN_Eye_Comparator.py project_backup_2024-01-01 project_current \
  --extensions .py .js .json \
  --html \
  --html-output project_diff.html
```

### Example 4: Non-Recursive Comparison
```bash
python BIN_Eye_Comparator.py config_old config_new \
  --no-recursive \
  --extensions .conf .cfg
```

### Example 5: Large Folder Analysis
```bash
python BIN_Eye_Comparator.py /data/archive1 /data/archive2 \
  --max-bytes 512 \
  --html \
  --html-output archive_comparison_$(date +%Y%m%d).html
```

### Example 6: Custom Template
```bash
python BIN_Eye_Comparator.py builds/v1 builds/v2 \
  --html \
  --template company_template.html \
  --html-output build_comparison.html
```

---

## 🔄 Integration Examples

### Shell Script
```bash
#!/bin/bash
# Automated backup verification script

ORIGINAL="/data/production"
BACKUP="/backup/production"
REPORT="backup_verification_$(date +%Y%m%d_%H%M%S).html"

python BIN_Eye_Comparator.py "$ORIGINAL" "$BACKUP" \
  --html \
  --html-output "$REPORT"

if [ $? -eq 0 ]; then
    echo "Comparison complete. Report: $REPORT"
    # Email report
    mail -s "Backup Verification" admin@company.com < "$REPORT"
else
    echo "Comparison failed!"
    exit 1
fi
```

### Python Script
```python
import subprocess
import sys

def compare_files(file1, file2):
    """Wrapper function for binary comparison"""
    result = subprocess.run([
        'python', 'BIN_Eye_Comparator.py',
        file1, file2,
        '--html',
        '--html-output', f'comparison_{file1}_{file2}.html'
    ], capture_output=True, text=True)
    
    return result.returncode == 0

# Usage
if compare_files('file1.bin', 'file2.bin'):
    print("Files compared successfully")
else:
    print("Comparison failed")
```

### CI/CD Pipeline (GitHub Actions)
```yaml
name: Binary Comparison

on: [push, pull_request]

jobs:
  compare:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Compare builds
        run: |
          python BIN_Eye_Comparator.py \
            expected_output/ \
            actual_output/ \
            --html \
            --html-output comparison_report.html
      
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: comparison-report
          path: comparison_report.html
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to functions
- Include examples in commit messages
- Update README for new features

---

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/bin-eye-comparison/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/bin-eye-comparison/discussions)
- **Email**: support@example.com

---

## 🎓 FAQ

### Q: Can it compare text files?
**A:** Yes! It works with ANY file type, including text files.

### Q: What's the maximum file size?
**A:** No hard limit, but very large files (GB+) may use significant RAM.

### Q: Can I automate this in scripts?
**A:** Absolutely! It's designed for command-line automation.

### Q: Does it modify the files?
**A:** No, it only reads files. Never modifies them.

### Q: Can I compare across networks?
**A:** Yes, as long as you have read access to both paths.

### Q: Is it safe for production use?
**A:** Yes, it's read-only and thoroughly tested.

---

## 🗺️ Roadmap

- [ ] JSON output format
- [ ] XML output format
- [ ] Diff file generation (like patch files)
- [ ] Progress bar for large operations
- [ ] Parallel processing for folders
- [ ] Checksum verification (MD5, SHA256)
- [ ] Ignore patterns (like .gitignore)
- [ ] Smart binary diff algorithms
- [ ] Web interface
- [ ] Docker container

---

## 📚 Additional Resources

- [Python Documentation](https://docs.python.org/3/)
- [Binary File Formats](https://en.wikipedia.org/wiki/Binary_file)
- [Hexadecimal](https://en.wikipedia.org/wiki/Hexadecimal)

---

## ⭐ Acknowledgments

- Thanks to all contributors
- Inspired by tools like `diff`, `cmp`, and `hexdump`
- Built with Python standard library

---

<div align="center">

**Made with ❤️ for the developer community**

[⬆ Back to Top](#-binary-file-comparison-tool)

</div>
