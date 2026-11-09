# AIMLZG557 Assignment 2: Group 109

The `submission/` folder holds exactly what goes into the final ZIP: the group's Question 1 notebook and
one Question 2 PDF per member. When all five PDFs are in, zip the folder's contents and submit
through the portal.

## Submission status

| Member | BITS ID | File in `submission/` | Status |
|:--|:--|:--|:--|
| Group (Question 1) | | `Question1_Group109.ipynb` | Added, outputs saved in every cell that prints |
| Stuti Srivastava | 2025AG05747 | `2025AG05747.pdf` | Pending |
| Chirag Bhatnagar | 2025AG05066 | `2025AG05066.pdf` | Added |
| Aditya Saraswat | 2025AG05058 | `2025AG05058.pdf` | Pending |
| Vanshika Sangal | 2025AG05381 | `2025AG05381.pdf` | Pending |
| Neelam Devi | 2025AG05908 | `2025AG05908.pdf` | Added |

The ZIP must hold **6 files**: 1 notebook and 5 PDFs. A member whose PDF is missing gets no Question 2
marks, so everyone should check the ZIP before it is uploaded.

## Add your Question 2 PDF

Question 2 is individual work: write your own.

1. Name your PDF with your BITS ID only, for example `2025AG05747.pdf`.
2. On GitHub, open the `submission` folder, then choose **Add file → Upload files** and upload your PDF.
3. Choose **Create a new branch for this commit and start a pull request**, and title it
   `Add Q2 PDF - <your BITS ID>`.
4. In the same pull request, change your row above from **Pending** to **Added**.

Only add your own PDF. Don't change the notebook or anyone else's file.

## Build the ZIP

Once all five PDFs are merged, pull the latest `main` and run this in PowerShell from the repository folder:

```powershell
Compress-Archive -Path submission\* -DestinationPath Group109_Assignment2.zip -Force
```

Open the ZIP and confirm it has the 6 files, then submit it through the portal. Email submissions are
not accepted.

## Other files

- `change.md`: what was changed in the Question 1 notebook during review, and why.
- `q2/`: Chirag's working files for Question 2: the Word source, the Python knowledge base
  (`change_approval_kb.py`) and the screenshots used in the PDF.
