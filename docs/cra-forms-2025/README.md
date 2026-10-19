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

## Fourth batch (2026-10-19)
Downloaded on Umar's machine through headless Chrome from `/formspubs/pbg/<code>/<code>-25e.(txt|pdf)`;
sha256 checked against the download. Only Schedules 12 and 15 and T2222 publish a .txt; the rest are
PDF only (their .txt URL 404s), so quotes from them carry "(confirmed DATE from the PDF; no .txt
published)".

| File | Form | sha256 |
|---|---|---|
| t2042-25e.pdf | T2042, Statement of Farming Activities (PDF only) | 0223f8a766b06beb93a6e94282ffcd84c2265444b2992c35efc34185233b2597 |
| t2121-25e.pdf | T2121, Statement of Fishing Activities (PDF only) | 6667327bdd83502f826ac247e62fbc32e054b909160f1a540780a7773033381b |
| 5000-s15-25e.txt | Schedule 15, FHSA Contributions, Transfers and Activities | 6031f31255b0d406a41f59b92d99b95eb039ea11c5ca2683742d8d7d3ecd1f8f |
| t929-24e.pdf | T929, Disability Supports Deduction, **2024 edition** (no 2025 edition; PDF only) | 89b8dd2eff41f7887e0a880f7415cf079519a7313a8032bf2f074a187466f9a5 |
| t1-m-25e.pdf | T1-M, Moving Expenses Deduction (PDF only) | d33ce87b0ea135a4145aae7df824f6e5745f7bd03b6193b2958131a170d6a2fd |
| t1223-25e.pdf | T1223, Clergy Residence Deduction (PDF only) | ae7177e65c4dabaab6a05affde0aa0768d3872cafb670f6e32c1afd41c73a6c1 |
| t777-25e.pdf | T777, Statement of Employment Expenses (PDF only) | 99e767b0c8a2a841f66f516e28b5f9fe631d6dbd4db6eaae36cb7c82b93f1204 |
| t2048-25e.pdf | T2048, Capital Gains Deduction for Qualifying Business Transfers or Qualifying Cooperative Conversions (PDF only) | 75f4790ffb5e8b1dfcda6af0a68bff4fbe7852f149fbdcb5660b2c1f6ecc3734 |
| t657-25e.pdf | T657, Calculation of Capital Gains Deduction (PDF only) | 5ad7c7a95a4bcf24ecb909db8f1e24ed3f8707c4fab4c7987e149850f900d240 |
| t2222-25e.txt | T2222, Northern Residents Deductions | aedc9f64a7f8857415c9a8d18a20e0dc860601a88510a4b9710158816245ff53 |
| rc381-25e.pdf | RC381, Inter-Provincial Calculation for CPP and QPP Contributions and Overpayments (PDF only) | 3c472af23df02adc22f976d34cfca733e0d702e094f4f5f0335248d41c50fa9b |
| t2038-ind-25e.pdf | T2038(IND), Investment Tax Credit (Individuals) (PDF only; CRA's path is `t2038-ind`) | 782d8ade84f7b79f4f73624a992ea3668ee008b168d3ad0579ffd3d01db8b48d |
| t1172-25e.pdf | T1172, Additional Tax on Accumulated Income Payments from RESPs (PDF only) | 0985388e35ca1b70d6a92d0764d36b39b9754d9c8403cbb75426805ec4b052ef |
| rc359-25e.pdf | RC359, Tax on Excess Employees Profit Sharing Plan Amounts (PDF only) | 9561b6c3fb12904a01741515f32977cf23225de2e980d7091dc89bb275cb3ed5 |
| 5000-s12-25e.txt | Schedule 12, Multigenerational Home Renovation Tax Credit | 05a0a91988a533eb82f9222eb4133418dafdcdce51091b4e4dbdade376544b75 |
| t2043-25e.pdf | T2043, Return of Fuel Charge Proceeds to Farmers Tax Credit (PDF only) | 6f445e20f97ce7b7ba4204480b98342ee922a976069e3575464b5146f7f70e36 |
| t2204-25e.pdf | T2204, Employee Overpayment of Employment Insurance Premiums (PDF only) | 5b34eff9998812738dc116272db8cd20add88b84a3fde7532f580cd1fd11f987 |

Not saved, because CRA publishes no 2024 or 2025 file:
- **T1229**, Statement of Resource Expenses and Depletion Allowance: CRA's page links only
  `t1229-23e.pdf`; the 2024 and 2025 .txt and .pdf URLs 404.
- **T777S**, Statement of Employment Expenses for Working at Home Due to COVID-19: archived by CRA;
  the latest edition is 2022.
- **Line 25000 calculation chart** (other payments deduction over $93,454): an HTML table only, at
  https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/deductions-credits-expenses/line-25000-other-payments-deduction.html.
  The first part of the calculation is in the Federal Worksheet, `5000-d1-25e.txt`.
