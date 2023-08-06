# pdflayoutxt

pdflayoutxt is a Python library for extracting text from searchable pdf's (Non Scanned) and it make sures the extracted text is in the same layout as the document.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install pdflayoutxt
```

## Usage

```python
# import the library
import pdflayoutxt

# creates an object of pdfextracter
pdfobj=pdflayoutxt.pdfextracter()

# returns a list, each index being the text extracted from that index page. 
# In simple terms no_of_pages_in_document=len(list_returned)
pdf_path="./abc.pdf"
text=pdfobj.get_pdf_text(pdf_path=pdf_path)

# output
print(text)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)