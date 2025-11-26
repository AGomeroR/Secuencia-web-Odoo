#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Website Sequence Optimizer for Odoo
Optimizes product website_sequence based on eCommerce readiness and sales performance

Priority criteria (lower sequence = higher priority):
1. Products with public_categ_ids, image_1920, and website_description
2. Within same priority level, sort by sales performance (descending)

Usage:
    python website_sequence_optimizer.py                # Run optimization
    python website_sequence_optimizer.py --dry-run      # Preview changes only
    python website_sequence_optimizer.py --verbose      # Detailed logging
"""

import xmlrpc.client
import os
import sys
import argparse
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Odoo configuration from .env
ODOO_URL = os.getenv('ODOO_URL')
ODOO_DATABASE = os.getenv('ODOO_DB')
ODOO_USERNAME = os.getenv('ODOO_USER')
ODOO_API_KEY = os.getenv('ODOO_API_KEY')

# Configuration
BATCH_SIZE = 50  # Number of products to update per batch
LOG_FILE = "website_sequence_optimization.log"

class WebsiteSequenceOptimizer:
    def __init__(self, dry_run=False, verbose=False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.url = None
        self.db = None
        self.username = None
        self.api_key = None
        self.uid = None
        self.models = None
        self.common = None
        self.optimization_log = []
        
    def log(self, message, level="INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        
        print(log_entry)
        self.optimization_log.append(log_entry)
        
        # Write to log file
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Warning: Could not write to log file: {e}")
    
    def connect(self):
        """Establish connection to Odoo using API key authentication"""
        self.log("🔗 Connecting to Odoo...")
        
        # Validate configuration
        if not all([ODOO_URL, ODOO_DATABASE, ODOO_USERNAME, ODOO_API_KEY]):
            missing = []
            if not ODOO_URL: missing.append("ODOO_URL")
            if not ODOO_DATABASE: missing.append("ODOO_DB")
            if not ODOO_USERNAME: missing.append("ODOO_USER")
            if not ODOO_API_KEY: missing.append("ODOO_API_KEY")
            
            raise Exception(f"Missing environment variables: {', '.join(missing)}")
        
        self.url = ODOO_URL
        self.db = ODOO_DATABASE
        self.username = ODOO_USERNAME
        self.api_key = ODOO_API_KEY
        
        try:
            # Connect to Odoo
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
            
            # Authenticate with API key
            self.uid = self.common.authenticate(self.db, self.username, self.api_key, {})
            
            if not self.uid:
                raise Exception("Authentication failed. Check your API key and credentials.")
            
            self.log(f"✅ Connected successfully to Odoo as user ID: {self.uid}")
            
            # Test the connection with a simple call
            try:
                version_info = self.common.version()
                self.log(f"✅ Server version: {version_info.get('server_version', 'Unknown')}")
            except Exception as test_error:
                self.log(f"⚠️ Warning: Connection test failed: {test_error}")
            
            # Verify permissions
            access_rights = self.models.execute_kw(
                self.db, self.uid, self.api_key,
                'product.template', 'check_access_rights',
                ['write'], {'raise_exception': False}
            )
            
            if not access_rights:
                raise Exception("User does not have write permissions on product.template")
            
            self.log("✅ Write permissions verified")
            return True
            
        except Exception as e:
            self.log(f"❌ Connection error: {e}", "ERROR")
            return False
    
    def fetch_all_products(self):
        """Fetch ALL products (active and inactive) with pagination to handle large datasets"""
        self.log("📋 Fetching ALL products (active and inactive)...")
        
        try:
            # Fields needed for optimization
            fields = [
                'id', 'name', 'website_sequence', 'website_published', 'active',
                'public_categ_ids', 'image_1920', 'website_description',
                'sales_count', 'sale_ok'
            ]
            
            # First, count total products
            total_count = self.models.execute_kw(
                self.db, self.uid, self.api_key,
                'product.template', 'search_count',
                [[]]  # Empty domain = count all products
            )
            
            self.log(f"📊 Total products in database: {total_count}")
            
            # Fetch products in batches to avoid server timeout
            batch_size = 500  # Smaller batches to avoid 502 errors
            all_products = []
            
            for offset in range(0, total_count, batch_size):
                batch_num = offset // batch_size + 1
                total_batches = (total_count + batch_size - 1) // batch_size
                
                self.log(f"📦 Fetching batch {batch_num}/{total_batches} (products {offset+1}-{min(offset+batch_size, total_count)})")
                
                try:
                    batch_products = self.models.execute_kw(
                        self.db, self.uid, self.api_key,
                        'product.template', 'search_read',
                        [[]],  # Empty domain = get all products
                        {
                            'fields': fields,
                            'limit': batch_size,
                            'offset': offset
                        }
                    )
                    
                    all_products.extend(batch_products)
                    self.log(f"   ✅ Fetched {len(batch_products)} products")
                    
                    # Small delay between batches to be gentle on the server
                    if batch_num < total_batches:
                        import time
                        time.sleep(0.5)
                        
                except Exception as batch_error:
                    self.log(f"   ❌ Error fetching batch {batch_num}: {batch_error}", "ERROR")
                    # Continue with other batches
                    continue
            
            self.log(f"✅ Successfully fetched {len(all_products)} total products")
            
            if self.verbose and all_products:
                # Statistics breakdown
                active_count = sum(1 for p in all_products if p.get('active'))
                published_count = sum(1 for p in all_products if p.get('website_published'))
                with_categories = sum(1 for p in all_products if p.get('public_categ_ids'))
                with_images = sum(1 for p in all_products if p.get('image_1920'))
                with_descriptions = sum(1 for p in all_products if p.get('website_description') and str(p['website_description']).strip())
                
                self.log(f"📊 Active products: {active_count}")
                self.log(f"📊 Website published products: {published_count}")
                self.log(f"📊 Products with eCommerce categories: {with_categories}")
                self.log(f"📊 Products with images: {with_images}")
                self.log(f"📊 Products with descriptions: {with_descriptions}")
            
            return all_products
            
        except Exception as e:
            self.log(f"❌ Error fetching products: {e}", "ERROR")
            self.log("💡 Try running again - this might be a temporary server issue")
            return []
    
    def calculate_priority_score(self, product):
        """Calculate priority score for a product (higher score = higher priority = lower sequence)"""
        score = 0
        criteria_met = 0
        
        # Base score for active and published products
        base_score = 0
        
        # Highest priority: Active AND published products
        if product.get('active') and product.get('website_published'):
            base_score = 10000000  # 10M base score
        
        # Medium priority: Active but not published
        elif product.get('active') and not product.get('website_published'):
            base_score = 1000000   # 1M base score
            
        # Lower priority: Published but not active
        elif not product.get('active') and product.get('website_published'):
            base_score = 100000    # 100K base score
            
        # Lowest priority: Neither active nor published
        else:
            base_score = 0         # No base score
        
        score = base_score
        
        # eCommerce readiness criteria (only for active/published products)
        if product.get('active') or product.get('website_published'):
            if product.get('public_categ_ids'):
                score += 100000
                criteria_met += 1
                
            if product.get('image_1920'):
                score += 10000
                criteria_met += 1
                
            if product.get('website_description') and str(product['website_description']).strip():
                score += 1000
                criteria_met += 1
        
        # Sales performance (only for active products)
        if product.get('active'):
            sales_count = product.get('sales_count', 0) or 0
            score += sales_count
        
        return score, criteria_met
    
    def optimize_sequences(self, products):
        """Calculate optimized website sequences for products"""
        self.log("🎯 Calculating optimized sequences...")
        
        # Calculate scores for all products
        product_scores = []
        for product in products:
            score, criteria_met = self.calculate_priority_score(product)
            product_scores.append({
                'product': product,
                'score': score,
                'criteria_met': criteria_met,
                'current_sequence': product.get('website_sequence', 0)
            })
        
        # Sort by score (highest first) - these get lowest sequence numbers
        product_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Assign new sequences to ALL products to ensure proper ordering
        all_updates = []
        priority_groups = {3: [], 2: [], 1: [], 0: []}
        status_groups = {'active_published': [], 'active_only': [], 'published_only': [], 'inactive': []}
        changes_count = 0
        
        for index, item in enumerate(product_scores, 1):
            new_sequence = index
            current_sequence = item['current_sequence']
            criteria_met = item['criteria_met']
            product = item['product']
            
            # Group by criteria met for reporting
            priority_groups[criteria_met].append(item)
            
            # Group by status for reporting
            if product.get('active') and product.get('website_published'):
                status_groups['active_published'].append(item)
            elif product.get('active'):
                status_groups['active_only'].append(item)
            elif product.get('website_published'):
                status_groups['published_only'].append(item)
            else:
                status_groups['inactive'].append(item)
            
            # Track if this is actually a change
            if new_sequence != current_sequence:
                changes_count += 1
            
            # Add ALL products to updates list (we need to reassign all sequences)
            all_updates.append({
                'id': product['id'],
                'name': product['name'],
                'current_sequence': current_sequence,
                'new_sequence': new_sequence,
                'criteria_met': criteria_met,
                'score': item['score'],
                'is_change': new_sequence != current_sequence,
                'active': product.get('active'),
                'published': product.get('website_published')
            })
        
        # Log optimization results
        self.log(f"🎯 Optimization complete:")
        self.log(f"   📊 Priority by status:")
        self.log(f"      - {len(status_groups['active_published'])} Active + Published products (highest priority)")
        self.log(f"      - {len(status_groups['active_only'])} Active only products")
        self.log(f"      - {len(status_groups['published_only'])} Published only products")
        self.log(f"      - {len(status_groups['inactive'])} Inactive products (lowest priority)")
        
        self.log(f"   📊 eCommerce readiness:")
        for criteria_count in [3, 2, 1, 0]:
            count = len(priority_groups[criteria_count])
            if count > 0:
                self.log(f"      - {count} products with {criteria_count}/3 eCommerce criteria")
        
        self.log(f"📝 Total products to update: {len(all_updates)}")
        self.log(f"📝 Products with sequence changes: {changes_count}")
        
        if self.verbose and all_updates:
            self.log("📋 Preview of top priority products:")
            for update in all_updates[:10]:  # Show first 10
                change_indicator = "🔄" if update['is_change'] else "✓"
                status = ""
                if update['active'] and update['published']:
                    status = "🟢"  # Active + Published
                elif update['active']:
                    status = "🟡"  # Active only
                elif update['published']:
                    status = "🔵"  # Published only
                else:
                    status = "⚪"  # Inactive
                
                self.log(f"   {change_indicator} {status} {update['name']}: {update['current_sequence']} → {update['new_sequence']} ({update['criteria_met']}/3 criteria)")
            if len(all_updates) > 10:
                self.log(f"   ... and {len(all_updates) - 10} more")
            
            self.log("   Legend: 🟢=Active+Published, 🟡=Active only, 🔵=Published only, ⚪=Inactive")
        
        return all_updates
    
    def apply_updates(self, updates):
        """Apply sequence updates to Odoo avoiding conflicts"""
        if not updates:
            self.log("ℹ️ No updates needed")
            return True
        
        if self.dry_run:
            self.log(f"🔍 DRY RUN: Would update {len(updates)} products")
            return True
        
        self.log(f"🔄 Applying {len(updates)} sequence updates...")
        
        # Strategy: Use a two-phase update to avoid conflicts
        # Phase 1: Move all products to temporary high sequences
        # Phase 2: Set final sequences
        
        successful_updates = 0
        failed_updates = 0
        
        # Find the highest current sequence to use as temporary base
        max_sequence = max([u['current_sequence'] for u in updates] + [u['new_sequence'] for u in updates])
        temp_base = max_sequence + 10000  # Start temporary sequences well above current max
        
        self.log(f"🔄 Phase 1: Moving products to temporary sequences (starting at {temp_base})")
        
        # Phase 1: Move all products that need updating to temporary sequences
        for i, update in enumerate(updates):
            temp_sequence = temp_base + i
            try:
                self.models.execute_kw(
                    self.db, self.uid, self.api_key,
                    'product.template', 'write',
                    [update['id'], {'website_sequence': temp_sequence}]
                )
                update['temp_sequence'] = temp_sequence
                
                if self.verbose:
                    self.log(f"   🔄 {update['name']}: {update['current_sequence']} → temp {temp_sequence}")
                    
            except Exception as e:
                failed_updates += 1
                self.log(f"   ❌ Phase 1 failed for {update['name']}: {e}", "ERROR")
                continue
        
        self.log(f"🔄 Phase 2: Setting final optimized sequences")
        
        # Phase 2: Set final sequences (now no conflicts possible)
        for update in updates:
            if 'temp_sequence' not in update:
                continue  # Skip if Phase 1 failed for this product
                
            try:
                self.models.execute_kw(
                    self.db, self.uid, self.api_key,
                    'product.template', 'write',
                    [update['id'], {'website_sequence': update['new_sequence']}]
                )
                successful_updates += 1
                
                if self.verbose:
                    self.log(f"   ✅ {update['name']}: temp {update['temp_sequence']} → final {update['new_sequence']}")
                    
            except Exception as e:
                failed_updates += 1
                self.log(f"   ❌ Phase 2 failed for {update['name']}: {e}", "ERROR")

        self.log(f"📊 Update results: {successful_updates} successful, {failed_updates} failed")
        return failed_updates == 0
    
    def save_optimization_report(self, updates):
        """Save detailed optimization report to JSON file"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_products_analyzed': len(updates) if updates else 0,
            'dry_run': self.dry_run,
            'updates': updates or [],
            'log': self.optimization_log
        }
        
        report_file = f"website_sequence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            self.log(f"📄 Optimization report saved: {report_file}")
        except Exception as e:
            self.log(f"⚠️ Could not save report: {e}", "WARNING")
    
    def run_optimization(self):
        """Main optimization workflow"""
        self.log("🚀 Starting website sequence optimization...")
        
        try:
            # Connect to Odoo
            if not self.connect():
                return False
            
            # Fetch products
            products = self.fetch_all_products()
            if not products:
                self.log("ℹ️ No products found or error fetching products")
                return False
            
            # Calculate optimized sequences
            updates = self.optimize_sequences(products)
            
            # Apply updates
            success = self.apply_updates(updates)
            
            # Save report
            self.save_optimization_report(updates)
            
            if self.dry_run:
                self.log("🔍 DRY RUN completed - no changes made")
            else:
                self.log("🎉 Website sequence optimization completed")
            
            return success
            
        except Exception as e:
            self.log(f"❌ Optimization failed: {e}", "ERROR")
            return False

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Optimize Odoo product website sequences based on eCommerce readiness',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python website_sequence_optimizer.py                # Run optimization
  python website_sequence_optimizer.py --dry-run      # Preview changes only
  python website_sequence_optimizer.py --verbose      # Detailed logging
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without applying them'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()

def main():
    """Main function"""
    args = parse_arguments()
    
    print("🎯 Odoo Website Sequence Optimizer")
    print("=" * 50)
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
    
    # Verify environment variables
    missing_vars = []
    for var in ['ODOO_URL', 'ODOO_DB', 'ODOO_USER', 'ODOO_API_KEY']:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\n💡 Check your .env file configuration")
        sys.exit(1)
    
    # Run optimization
    optimizer = WebsiteSequenceOptimizer(dry_run=args.dry_run, verbose=args.verbose)
    success = optimizer.run_optimization()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()