# 🎯 Odoo Website Sequence Optimizer

Automatically optimize your Odoo eCommerce product display order based on completeness and sales performance.

This Python utility analyzes all products in your Odoo instance and intelligently assigns `website_sequence` values, prioritizing products that are active, published, have complete eCommerce information (categories, images, descriptions), and demonstrate strong sales performance.

**Status**: Production Ready | **Python**: 3.7+ | **Version**: 1.0.0

---

## Table of Contents

- [Features](#features)
- [Why Use This Tool](#why-use-this-tool)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Output & Reports](#output--reports)
- [Troubleshooting](#troubleshooting)
- [Author](#author)

---

## Features

- ✅ **Intelligent 4-Tier Priority System**: Organizes products by status (Active+Published, Active Only, Published Only, Inactive)
- ✅ **eCommerce Readiness Criteria**: Evaluates public categories, product images, and website descriptions
- ✅ **Sales Performance Tie-breaker**: Uses real sales data to prioritize products within the same tier
- ✅ **Dry-Run Mode**: Preview all changes without applying them to your Odoo instance
- ✅ **Two-Phase Updates**: Safe mechanism that avoids duplicate sequence number conflicts
- ✅ **Comprehensive Logging**: Detailed file logging and timestamped JSON reports
- ✅ **Batch Processing**: Efficiently handles large databases with thousands of products
- ✅ **Progress Indicators**: Real-time feedback with emojis and detailed statistics

---

## Why Use This Tool

### The Problem
Many Odoo instances have products ordered randomly or by ID, meaning incomplete or inactive products may appear before ready-to-sell products with complete information.

### The Solution
This optimizer ensures your best products - those that are active, published, have attractive images, complete descriptions, appropriate categories, and good sales history - appear first on your website.

### Benefits
- 📈 **Higher Click-Through Rates**: High-quality products appear first
- 🎯 **Better SEO**: Consistent, quality-based ordering
- ⚡ **Automatic Handling**: Optimizes ALL products, not just published ones
- 📊 **Data-Driven Decisions**: Uses real sales metrics to prioritize

---

## Prerequisites

### System Requirements
- **Python 3.7 or higher** installed on your system
- **pip** (Python package manager)
- Access to create and edit `.env` file

### Odoo Instance Requirements
- **Odoo v14+** (or any version compatible with XML-RPC API)
- **User account** with write permissions on `product.template`
- **API Key authentication** enabled and generated
- Access to the following product fields:
  - `website_sequence` (field to optimize)
  - `website_published` (publication status)
  - `active` (active/inactive status)
  - `public_categ_ids` (eCommerce categories)
  - `image_1920` (product image)
  - `website_description` (website description)
  - `sales_count` (sales counter)

### Network Requirements
- Outbound HTTPS access to your Odoo instance
- Stable internet connection (especially for large databases)

---

## Installation

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd "Secuencia sitio web"

# Or manually download and extract files
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python website_sequence_optimizer.py --help
```

You should see the help message with available options.

---

## Configuration

### Generate Odoo API Key

1. Log in to your Odoo instance as administrator
2. Navigate to **Settings > Users & Companies > Users**
3. Select your user account
4. Scroll to the **"Access Tokens"** section
5. Click **"New Token"**
6. Enter a description (e.g., "Sequence Optimizer")
7. **Copy the token value** (only shown once)

### Create .env File

Create a file named `.env` in the project directory with the following content:

```env
ODOO_URL=https://your-instance.odoo.com
ODOO_DB=your_database_name
ODOO_USER=your_username
ODOO_API_KEY=your_api_key
```

**Replace the values**:
- `ODOO_URL`: Full URL of your Odoo instance (include `https://`)
- `ODOO_DB`: Exact name of your database
- `ODOO_USER`: Your username or email
- `ODOO_API_KEY`: The token you generated in the previous step

### Important Security Notes

- ⚠️ **NEVER** commit the `.env` file to version control (Git)
- ⚠️ Keep your API Key secure - regenerate if exposed
- ⚠️ Verify URL format includes the protocol (`https://`)
- ✅ The `.gitignore` file is already configured to protect `.env`

---

## Usage

### Basic Usage

```bash
python website_sequence_optimizer.py
```

This will run the complete optimization and apply changes to your Odoo instance.

### Dry-Run Mode

```bash
python website_sequence_optimizer.py --dry-run
```

Preview all changes without applying them. **Always recommended for first run.**

### Verbose Mode

```bash
python website_sequence_optimizer.py --verbose
```

Display extended logging with detailed eCommerce readiness metrics.

### Recommended Combination (First Run)

```bash
python website_sequence_optimizer.py --dry-run --verbose
```

This allows you to see exactly what changes will be made before applying them.

### Command-Line Options

| Option | Short Form | Description |
|--------|------------|-------------|
| `--dry-run` | - | Preview changes without applying them to Odoo |
| `--verbose` | `-v` | Enable detailed logging with eCommerce metrics |

### Recommended Workflow

```bash
# 1. First time: preview with verbose
python website_sequence_optimizer.py --dry-run --verbose

# 2. Review the output and generated JSON report

# 3. If everything looks good, run to apply changes
python website_sequence_optimizer.py --verbose

# 4. Verify some products in Odoo to confirm
```

---

## How It Works

### Processing Flow

```
1. Connect to Odoo with API Key authentication
   ↓
2. Fetch ALL products (active and inactive) with pagination
   ↓
3. Calculate priority score for each product
   ↓
4. Sort products by score (highest to lowest)
   ↓
5. Assign incremental sequences (1, 2, 3, ...)
   ↓
6. Apply updates in two phases to avoid conflicts
   ↓
7. Generate JSON report and update log file
```

### Priority Scoring Algorithm

The optimizer calculates a score for each product based on multiple criteria:

#### Base Score (by Status)

| Status | Base Score | Priority | Icon |
|--------|-----------|----------|------|
| **Active + Published** | 10,000,000 | Highest (1st) | 🟢 |
| **Active Only** | 1,000,000 | 2nd | 🟡 |
| **Published Only** | 100,000 | 3rd | 🔵 |
| **Inactive + Unpublished** | 0 | Lowest (4th) | ⚪ |

#### eCommerce Readiness Bonuses

For active or published products, additional points are added:

- ✅ **Has public categories** (`public_categ_ids`): **+100,000 points**
- ✅ **Has image** (`image_1920`): **+10,000 points**
- ✅ **Has web description** (`website_description`): **+1,000 points**

#### Sales Performance Tie-breaker

For active products, the sales counter is added directly:

- 📊 **Sales**: **+1 point per unit sold**
- Uses the `sales_count` field to break ties within the same priority tier

### Example Calculation

```
Product A: Active + Published + Categories + Image + Description + 50 sales
Score = 10,000,000 + 100,000 + 10,000 + 1,000 + 50 = 10,111,050
→ website_sequence = 1 (first position)

Product B: Active + Published + Categories + Image + 20 sales
Score = 10,000,000 + 100,000 + 10,000 + 20 = 10,110,020
→ website_sequence = 2 (second position)

Product C: Active Only + Categories + 100 sales
Score = 1,000,000 + 100,000 + 100 = 1,100,100
→ website_sequence = 3 (third position)

Product D: Inactive + Unpublished
Score = 0
→ website_sequence = [last] (lowest priority)
```

### Why Two-Phase Updates?

To avoid duplicate sequence conflicts during mass update:

- **Phase 1**: Moves all products to temporary high sequences (e.g., 50000+)
- **Phase 2**: Sets final optimized sequences (1, 2, 3, ...)

This approach prevents uniqueness constraint errors and ensures clean updates.

---

## Output & Reports

### Log File

**Filename**: `website_sequence_optimization.log`

- Contains timestamped entries of all operations
- **Append-only mode**: Previous runs are preserved
- Useful for audit trail and debugging
- Includes: connection, data fetching, calculations, updates, errors

**Example Log Entries**:
```
[2025-11-26 14:30:45] INFO: 🚀 Starting website sequence optimization...
[2025-11-26 14:30:46] INFO: 🔗 Connecting to Odoo...
[2025-11-26 14:30:47] INFO: ✅ Connected successfully to Odoo as user ID: 2
[2025-11-26 14:30:47] INFO: ✅ Server version: 16.0
[2025-11-26 14:30:48] INFO: 📋 Fetching ALL products (active and inactive)...
[2025-11-26 14:30:50] INFO: 📊 Total products in database: 31,312
```

### JSON Report

**Filename**: `website_sequence_report_YYYYMMDD_HHMMSS.json`

Contains detailed optimization results with the following fields:

- `timestamp`: ISO date and time of execution
- `total_products_analyzed`: Total number of products processed
- `dry_run`: Boolean indicating if it was a test run
- `updates`: Array with all sequence changes per product
  - For each product: `id`, `name`, `current_sequence`, `new_sequence`, `criteria_met`, `score`, `active`, `published`
- `log`: Complete execution log

### Console Output

During execution you'll see:

- **Progress indicators** with real-time emojis
- **Summary statistics**:
  - Total products in database
  - Breakdown by status (Active+Published, Active Only, Published Only, Inactive)
  - Products with categories, images, descriptions
  - Total products to update
  - Products with sequence changes
- **Product preview** (in verbose mode):
  - Top 10 highest priority products
  - Sequence changes (before → after)
  - Criteria met (X/3)
  - Status indicators with emojis
- **Warnings or errors** encountered during processing

---

## Troubleshooting

### Common Issues

#### 1. "Missing environment variables: ODOO_URL, ODOO_DB, ODOO_USER, ODOO_API_KEY"

**Cause**: `.env` file not found or incomplete

**Solution**:
- Verify that the `.env` file exists in the project directory
- Ensure it contains all 4 required variables
- Check that there are no spaces around the `=` sign
- File must be named exactly `.env` (not `.env.txt`)

#### 2. "Authentication failed. Check your API key and credentials."

**Cause**: Invalid API key, username, or database name

**Solution**:
- Regenerate your API key in Odoo (Settings > Users > your user > Access Tokens)
- Verify username/email is correct
- Confirm database name is exact (case-sensitive)
- Ensure URL includes `https://` and the correct domain
- **Note**: Password authentication is NOT supported; you must use API Key

#### 3. "User does not have write permissions on product.template"

**Cause**: Odoo user account lacks write access to products

**Solution**:
- Ask Odoo admin to grant "Product Manager" or higher role to your user
- Or create a dedicated admin user with full permissions
- Verify user is not restricted to specific companies/warehouses

#### 4. Script Hangs or Times Out

**Cause**: Large product dataset or slow network connection

**Solution**:
- Script handles batches of 500 products automatically
- For large databases (10,000+ products), execution can take 10-30 minutes
- Check your internet connection speed
- Includes 0.5-second delay between batches by design (gentle on server)
- If it persists, consider running during off-peak hours

#### 5. "Phase 1 failed for product X: ..."

**Cause**: Temporary sequence update failed for specific product

**Solution**:
- Check Odoo server status
- Verify product hasn't been deleted
- Look for conflicting rules/constraints on `website_sequence` field
- Try running again later
- Review full error message in log file

#### 6. Some Products Not Getting Optimized

**Cause**: Products might have readonly `website_sequence` field, missing fields, or constraints

**Solution**:
- Check product configuration in Odoo
- Verify field customizations don't restrict updates
- Look for records that failed in error logs
- Can investigate specific products in Odoo UI

### General Debugging

1. Run with `--verbose` flag for detailed output
2. Check log file: `website_sequence_optimization.log`
3. Check JSON report for specific product details
4. Run with `--dry-run` first to see what would change
5. Verify credentials in `.env` file

### Getting Help

If you need additional assistance:
- Include complete error messages and relevant log entries
- Share console output and JSON report (sanitize sensitive info)
- Describe your Odoo version and database size
- Provide steps to reproduce the issue
- Contact: **gomex1994@gmail.com**

---

## Author

```
Developed by: Álvaro Gómez
Contact: gomex1994@gmail.com
Version: 1.0.0
Date: November 2025
```

---

**Note**: For bug reports, feature requests, or contributions, please contact **gomex1994@gmail.com**
