# Public Olist input data

Original source: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). The original analysis used the [public mirror at pinned commit 41710981b96a59a5399d88c62339ede3c8207e46](https://github.com/meroebeigi/E-Commerce/tree/41710981b96a59a5399d88c62339ede3c8207e46/archive). [source_manifest.json](source_manifest.json) records the eight required files, exact URLs, byte sizes and SHA-256 hashes.

## Prepare inputs

The required CSVs already exist under the repository's legacy `archive/` directory. Copy the eight files below into `data/raw/`; alternatively obtain them from the original dataset source. Create `data/raw/` first if needed.

```text
olist_orders_dataset.csv
olist_customers_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

For example, from the repository root in PowerShell:

```powershell
New-Item -ItemType Directory -Force data/raw
Copy-Item archive/*.csv data/raw/
```

Or in a POSIX shell:

```bash
mkdir -p data/raw
cp archive/*.csv data/raw/
```

The optional geolocation CSV may be copied by these wildcard examples but is not loaded. This analysis uses destination/origin states, not precise distances. Run `python run_pipeline.py --stage quality`, then the stages in the [root README](../README.md#reproduce).

The quality stage computes actual input hashes into `output/source_checksums.csv`; computing hashes alone is not manifest verification. Run `python scripts/validate_repository.py` to compare the checked-in source files to the manifest. When quality outputs exist, that check also compares the working-input checksum table and validates financial/status reconciliations. On Windows, Git may convert LF source files to CRLF: the checker first tests exact bytes, then permits only CRLF-to-LF normalization against the pinned manifest and reports every normalized file. The checksum table still records the actual working-file bytes.

## Tracked data and privacy

Existing `archive/` and `archive.zip` are retained source mirrors. New CSV/ZIP working copies under `data/raw/` and detailed CSV/SQLite outputs under `output/` are ignored by Git. The aggregate `powerbi/dashboard_data.csv` is intentionally tracked for report refresh; it contains month/state summaries and no customer/order identifiers.

Follow the original dataset's license and attribution requirements for redistribution. The public project contains no proprietary company records or recommendations. See [project status](../docs/project_status.md) for the delivered dashboard scope and [metric definitions](../docs/metric_dictionary.md) for eligible populations.
