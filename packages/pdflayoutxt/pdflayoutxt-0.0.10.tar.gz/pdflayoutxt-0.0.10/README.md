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
# In simple terms no_of_pages_in_document==len(list_returned)
pdf_path="./abc.pdf"
text=pdfobj.get_pdf_text(pdf_path=pdf_path)

# output
print(text)
```

| Method | Description |
|--------|-------------|
|`.get_pdf_text(pdf_path,pdf_password="",pages=[],left_most_x=0,left_most_y=0,right_most_x=1,right_most_y=1)`| Returns a list of list, of texts, present in each of the page in the document.`pdf_password` argument takes a string input,if pdf is encrypted with password, the password needs to be passed to this argument. `Pages` argument takes a list of pages or int (single page)  from where the text needs to be extracted, if text from all pages are required the default parameter will take care. `left_most_x` this parameter defines the starting point of text extraction on x axis (width). Its value lies between [0,1], like if we need .25 percent of right side of page (width) then we will pass .75 as argument. `left_most_y` this parameter defines the starting point of text extraction on y axis (height). Its value lies between [0,1], like if we need .25 percent of text from bottom side of page  (height) then we will pass .75 as argument. `right_most_x` this parameter defines the end point of text extraction on x axis (width). Its value lies between [0,1]. `right_most_y` this parameter defines the end point of text extraction on y axis (height). Its value lies between [0,1]. These parameters `right_most_y`,`left_most_x`,`right_most_x`,`left_most_y` are set to default for extracting text from complete page without cropping, if the text needs to be extracted from a particular area of page, these parameters become handy.|

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)