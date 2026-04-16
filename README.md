This project is an **end-to-end invoice** processing system that extracts data from invoices, validates it against purchase orders, and sends it to SAP.


The system  flow:

       Upload Invoice → Extract Data → Structure JSON → Validate → Send to SAP

We use Unstructured to process invoices
 
   Extracts text and layout elements (not structured JSON directly)
   Produces raw document elements like text blocks and tables.

   Unstructured **does not** return clean JSON.

So we :
Convert extracted text into **structured JSON**
Extract meaningful fields like:
line items
base amount
total amount
