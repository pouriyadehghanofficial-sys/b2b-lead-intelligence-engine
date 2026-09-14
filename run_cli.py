#!/usr/bin/env python
"""Main entry point for CLI"""

import sys
import argparse
import logging
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.pipeline import LeadDiscoveryPipeline
from app.export.excel_export import ExcelExporter
from app.export.json_export import JSONExporter
from app.export.csv_export import CSVExporter
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="B2B Lead Intelligence Engine - Find and validate business leads"
    )
    
    parser.add_argument(
        "--industry",
        required=True,
        help="Industry/sector (Persian or English)"
    )
    parser.add_argument(
        "--location",
        required=True,
        help="Province/city (Persian or English)"
    )
    parser.add_argument(
        "--product",
        default=None,
        help="Target product/solution"
    )
    parser.add_argument(
        "--roles",
        nargs="*",
        default=[],
        help="Target job roles"
    )
    parser.add_argument(
        "--quantity",
        type=int,
        default=100,
        help="Target number of leads (default: 100)"
    )
    parser.add_argument(
        "--queries",
        type=int,
        default=20,
        help="Max search queries (default: 20)"
    )
    parser.add_argument(
        "--output",
        default="./leads",
        help="Output file path without extension (default: ./leads)"
    )
    parser.add_argument(
        "--format",
        choices=["xlsx", "json", "csv", "all"],
        default="xlsx",
        help="Export format (default: xlsx)"
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("B2B Lead Intelligence Engine")
    logger.info("=" * 60)
    logger.info(f"Industry: {args.industry}")
    logger.info(f"Location: {args.location}")
    logger.info(f"Target: {args.quantity} leads")
    logger.info("=" * 60)
    
    try:
        # Initialize pipeline
        pipeline = LeadDiscoveryPipeline()
        
        # Run discovery
        logger.info("Starting lead discovery...")
        leads = pipeline.discover(
            industry=args.industry,
            location=args.location,
            product=args.product,
            target_roles=args.roles or None,
            quantity=args.quantity,
            max_queries=args.queries,
        )
        
        logger.info(f"\nDiscovery complete! Found {len(leads)} leads.\n")
        
        # Export results
        export_results(leads, args.output, args.format)
        
        logger.info("\n" + "=" * 60)
        logger.info("Process completed successfully!")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error(f"\nFatal error: {str(e)}", exc_info=True)
        return 1


def export_results(leads, output_path, format_type):
    """Export results to file(s)"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type in ["xlsx", "all"]:
        logger.info(f"Exporting to Excel...")
        excel_path = f"{output_path}_{timestamp}.xlsx"
        exporter = ExcelExporter()
        exporter.export(leads, excel_path)
        logger.info(f"✓ Excel: {excel_path}")
    
    if format_type in ["json", "all"]:
        logger.info(f"Exporting to JSON...")
        json_path = f"{output_path}_{timestamp}.json"
        exporter = JSONExporter()
        exporter.export(leads, json_path)
        logger.info(f"✓ JSON: {json_path}")
    
    if format_type in ["csv", "all"]:
        logger.info(f"Exporting to CSV...")
        csv_path = f"{output_path}_{timestamp}.csv"
        exporter = CSVExporter()
        exporter.export(leads, csv_path)
        logger.info(f"✓ CSV: {csv_path}")


if __name__ == "__main__":
    sys.exit(main())
