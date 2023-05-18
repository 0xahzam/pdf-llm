# Talk to PDFs 👾🔗

### how to use?

**step 1:** install all dependencies

```
pip install -r requirements.txt
```

**step 2:** grab your openai api key and paste the pdf in the same directory

**step 3:** update these details in details.py and hit save

```
# for example

apikey = "xyz-1010"
title = "Example"
book_url = "test.pdf"
collection_name = "testcollection"
description = "an example"
```

**step 4:** open terminal and run

```
streamlit run app.py
```
