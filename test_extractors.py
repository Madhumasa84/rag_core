
from src.extractors import extract_text
import os

def test_all_formats():
    """Test all supported file formats"""
    
    # Create test_files directory if it doesn't exist
    if not os.path.exists("test_files"):
        os.makedirs("test_files")
        print("Created test_files directory")
    
    # Create sample files if they don't exist
    create_sample_files()
    
    test_files = [
        "test_files/sample.txt",
        "test_files/sample.html",
        # "test_files/sample.pptx",  # Uncomment if you have a PPTX file
    ]
    
    print("TESTING EXTRACTORS")
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            print(f"\n File not found: {file_path}")
            continue
            
        print(f"\n Testing: {file_path}")
        print("-" * 40)
        
        try:
            text = extract_text(file_path)
            print(f" Extracted {len(text)} characters")
            # Show first 200 characters, replacing newlines with spaces
            preview = text[:200].replace('\n', ' ').replace('\r', '')
            print(f" Preview: {preview}...")
        except Exception as e:
            print(f" Error: {e}")

def create_sample_files():
    """Create sample test files if they don't exist"""
    
    # Create sample TXT
    txt_path = "test_files/sample.txt"
    if not os.path.exists(txt_path):
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("""This is a sample text file.
It contains multiple lines of text.
This is for testing the text extractor.
The quick brown fox jumps over the lazy dog.
Line five of the sample text file.""")
        print(" Created sample.txt")
    
    # Create sample HTML
    html_path = "test_files/sample.html"
    if not os.path.exists(html_path):
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Sample HTML Document</title>
    <style>
        body { font-family: Arial; }
        .hidden { display: none; }
    </style>
    <script>
        console.log("This script should be removed");
    </script>
</head>
<body>
    <h1>Welcome to Sample HTML</h1>
    <p>This is a paragraph in the HTML file.</p>
    <p>Another paragraph with <b>bold text</b> and <i>italic text</i>.</p>
    <div class="content">
        <h2>Section 1</h2>
        <p>This content should be extracted.</p>
        <ul>
            <li>List item 1</li>
            <li>List item 2</li>
        </ul>
    </div>
    <!-- This comment should be ignored -->
    <footer>Footer text - should be extracted</footer>
</body>
</html>""")
        print(" Created sample.html")

if __name__ == "__main__":
    test_all_formats()