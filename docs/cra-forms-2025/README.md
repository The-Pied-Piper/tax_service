# CRA 2025 e-text forms (raw)

Downloaded unmodified with curl from `https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/<code>/<code>-25e.txt`
on Umar's machine on 2026-10-19 (cloud containers cannot reach canada.ca), then copied here.
sha256 checked against the download. Files are UTF-8 with BOM and CRLF line ends.

| File | Form |
|---|---|
| 5000-d1-25e.txt | Federal Worksheet |
| 5000-s2-25e.txt | Schedule 2 |
| 5000-s3-25e.txt | Schedule 3, Capital Gains or Losses |
| 5000-s5-25e.txt | Schedule 5, Amounts for Spouse and Dependants |
| t776-25e.txt | T776, Statement of Real Estate Rentals |
| 5006-r-25e.txt | T1 return, Ontario edition |
| 5006-c-25e.txt | Form ON428, Ontario Tax |
| 5006-a-25e.txt | Schedule ON428-A, LIFT credit |
| 5006-d-25e.txt | Worksheet ON428 |
| 5006-tc-25e.txt | Form ON479, Ontario Credits |
| 5006-tca-25e.txt | Schedule ON479-A, CARE credit |
| 5006-d1-25e.txt | Worksheet ON479 |
| 5006-tg-25e.txt | ON-BEN |
| 5006-s11-25e.txt | Schedule ON(S11) |
| 5000-g-25e.txt | General Income Tax and Benefit Guide 2025 (from `/formspubs/pub/5000-g/`, not `/pbg/`; the `/pbg/` URL 404s). sha256 d1da5d3d…68d8b7b1 |

No 2025 .txt exists for Schedule 1 (archived), T2209, T2091(IND), T2125 or T1A (PDF only), nor for
guides T4036 Rental Income and T4037 Capital Gains (HTML and PDF online; e-text only by mail order).
The General Guide's line 25300 section has no conversion chart; it says the claim depends on the
inclusion rates and refers to T4037.

## PDFs (no .txt published)
Downloaded unmodified with curl on Umar's machine on 2026-10-19, then copied here; sha256 checked
against the download. Forms are under `/formspubs/pbg/<code>/`, guides under `/formspubs/pub/<code>/`.
Umar accepted PDF quotes where CRA publishes no .txt (2026-10-19). Quotes on tickets were checked
against `pdftotext` output (plain and `-layout`).

| File | Form | sha256 |
|---|---|---|
| t2209-25e.pdf | T2209, Federal Foreign Tax Credits | 2a0f1cd37fdec2885e7231f3dff4976508825ea1b867dbfe8300933356abf539 |
| t2091ind-25e.pdf | T2091(IND), Principal Residence designation | 86199bfccd4a6c70e6522165b78d0cece30dbff21655e990a814c0d1c03e83e7 |
| t2125-25e.pdf | T2125, Business or Professional Activities | fae75091753cb1810404c00aaa3f2c1a91cfae942b73bace7e6b884f24a08738 |
| t1a-25e.pdf | T1A, Request for Loss Carryback | cfe11515c55863047eca93ba464523c5808592aa2d885a02323ce0aaf75c6059 |
| t4036-25e.pdf | Guide T4036, Rental Income | f34bf23a4b97e3fd11f1eb21d27bd5aeff3f1aefac3aa22128c9dd136e6f408c |
| t4037-25e.pdf | Guide T4037, Capital Gains | 8687687cabce3f26945c8f66581cb1167e1e149eb257d1ae1bb6d0958996139c |

| t1436-25e.pdf | T1436, Capital Gains Worksheet (line 25300 Chart A) | 3aec70975894e81e41f313219d8770a905ee0421992b36c175f529fc9265d07a |
| t4002-25e.pdf | Guide T4002, Self-employed Business Income (CCA rates; `/pub/`) | 8efc96434bfaab1beabe95b48d8cb3c764a6b2292e9865cb9aaeac938673453f |
| t2091ind-ws-23e.pdf | T2091(IND)-WS, Principal Residence Worksheet, **2023 edition** (CRA's current one; no 2024 or 2025 PDF) | bc9832b119d031595f5b34c86aad0afcf3be03340f36bc3bea9484a54757f649 |
| t2203-25e.pdf | T2203, Provincial and Territorial Taxes for Multiple Jurisdictions | a78d849d0dfe286e7b9750acf8bfccc494c9e59ae3e1d9415c64e379c8d7c48d |

The last four were downloaded 2026-10-19 on Umar's machine through headless Chrome (canada.ca drops
curl there too); none has a .txt (every .txt URL 404s).

## Third batch (2026-10-19)
Downloaded on Umar's machine through headless Chrome from `/formspubs/pbg/<code>/<code>-25e.(txt|pdf)`,
then copied here; sha256 checked against the download. The .txt files start with a UTF-8 BOM. The four
PDFs are here because their .txt URL 404s.

| File | Form | sha256 |
|---|---|---|
| 5006-s2-25e.txt | Schedule ON(S2), Provincial Amounts Transferred from your Spouse or Common-Law Partner | 6e68314aba25b10c337cde973e32f3c42191e6f8875d1278b0c6b87ea7ea605d |
| 5000-s8-25e.txt | Schedule 8, Canada Pension Plan Contributions and Overpayment | db859d06606fd7a13c7c2875ab5299d4780d37d8a28ffe77b9f0650d0ef988d2 |
| 5000-s9-25e.txt | Schedule 9, Donations and Gifts | 86988baa6d4a6918d202ec7beb167e57c9ae42136bbf2ca19125aada2b26cb06 |
| 5000-s11-25e.txt | Schedule 11, Federal Tuition Amount and Canada Training Credit | 8e9fae56e6168830d44ff97690a77c11bc0afb5ffcb65528e2a44b0eb2115393 |
| 5000-s13-25e.txt | Schedule 13, EI Premiums on Self-Employment and Other Eligible Earnings | f172ddfc8011e1ad59e171e427edf30320bf4ef9ae2e9486dbd1770476e6901c |
| t691-25e.pdf | T691, Alternative Minimum Tax (PDF only) | 7949e42864bd0d428b24af56bf3b4e23d7d1b277cf945abed1e099add1ddb7ea |
| t1206-25e.pdf | T1206, Tax on Split Income (PDF only) | 896a42d5be2fb7f36dd2d14a3744c60c1488ca12dffda9d219dfbbf9b9498061 |
| t2036-25e.pdf | T2036, Provincial or Territorial Foreign Tax Credit (PDF only) | 9eafaa97b1bb012fc75944affa32ef9345961b4ac73426cf3c1b8571f10c3770 |
| t1221-25e.pdf | T1221, Ontario Focused Flow-Through Share Resource Expenses (Individuals) (PDF only) | 73eb8d8558d604e199f6de042f4eac458c300e181f59a8bba24f7b121b538789 |
