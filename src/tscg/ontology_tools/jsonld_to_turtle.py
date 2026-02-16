#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TSCG JSON-LD to OWL Turtle Converter
====================================

Converts all .jsonld files to .ttl (OWL Turtle format) in ontology/ and system-models/ directories.

Author: Echopraxium with the collaboration of Claude AI
Date: 2026-02-15
Version: 1.0.0
License: MIT

Usage:
    python jsonld_to_turtle.py [--dry-run] [--output-dir OUTPUT]
    
Options:
    --dry-run       : Show what would be converted without actually converting
    --output-dir    : Specify different output directory (default: same as input)
    --verbose       : Show detailed conversion logs
    --skip-errors   : Continue on conversion errors instead of stopping
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime

try:
    from rdflib import Graph
    from rdflib.exceptions import ParserError
except ImportError:
    print("ERROR: rdflib not found. Install with: pip install rdflib")
    sys.exit(1)


class JSONLDToTurtleConverter:
    """Main converter class handling JSON-LD to Turtle conversion"""
    
    def __init__(self, root_dir: Path, output_dir: Path = None, 
                 dry_run: bool = False, skip_errors: bool = False):
        """
        Initialize converter
        
        Args:
            root_dir: Root directory of TSCG project
            output_dir: Output directory (None = same as input)
            dry_run: If True, only simulate conversion
            skip_errors: If True, continue on errors
        """
        self.root_dir = Path(root_dir).resolve()
        
        # Validate root directory has required folders
        if not self._validate_root_dir():
            self._auto_detect_root()
        
        self.output_dir = Path(output_dir).resolve() if output_dir else None
        self.dry_run = dry_run
        self.skip_errors = skip_errors
        
        # Target directories to scan
        self.target_dirs = [
            self.root_dir / "ontology",
            self.root_dir / "system-models"
        ]
        
        # Statistics
        self.stats = {
            'found': 0,
            'converted': 0,
            'failed': 0,
            'skipped': 0
        }
        
        # Error log
        self.errors: List[Tuple[Path, str]] = []
        
        # Setup logging
        self._setup_logging()
    
    def _validate_root_dir(self) -> bool:
        """Check if root directory contains ontology/ and system-models/"""
        ontology_exists = (self.root_dir / "ontology").exists()
        system_models_exists = (self.root_dir / "system-models").exists()
        return ontology_exists or system_models_exists
    
    def _auto_detect_root(self):
        """Auto-detect TSCG root by searching parent directories"""
        current = Path.cwd()
        max_levels = 5  # Don't search more than 5 levels up
        
        for _ in range(max_levels):
            if (current / "ontology").exists() or (current / "system-models").exists():
                self.root_dir = current
                return
            current = current.parent
        
        # If not found, keep the original root_dir and warn user
        pass
    
    def _setup_logging(self):
        """Configure logging"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(
                    self.root_dir / f'conversion_{datetime.now():%Y%m%d_%H%M%S}.log',
                    encoding='utf-8'
                )
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def find_jsonld_files(self) -> List[Path]:
        """
        Recursively find all .jsonld files in target directories
        
        Returns:
            List of Path objects to .jsonld files
        """
        jsonld_files = []
        
        for target_dir in self.target_dirs:
            if not target_dir.exists():
                self.logger.warning(f"Directory not found: {target_dir}")
                continue
            
            # Recursive glob for .jsonld files
            pattern = "**/*.jsonld"
            for file_path in target_dir.glob(pattern):
                if file_path.is_file():
                    jsonld_files.append(file_path)
                    self.logger.debug(f"Found: {file_path.relative_to(self.root_dir)}")
        
        return sorted(jsonld_files)
    
    def convert_file(self, input_path: Path) -> bool:
        """
        Convert a single JSON-LD file to Turtle
        
        Args:
            input_path: Path to .jsonld file
            
        Returns:
            True if conversion succeeded, False otherwise
        """
        try:
            # Determine output path
            if self.output_dir:
                # Preserve relative structure in output directory
                rel_path = input_path.relative_to(self.root_dir)
                output_path = self.output_dir / rel_path.with_suffix('.ttl')
            else:
                # Same directory as input
                output_path = input_path.with_suffix('.ttl')
            
            # Create output directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if self.dry_run:
                self.logger.info(f"[DRY-RUN] Would convert: {input_path.name} → {output_path.name}")
                return True
            
            # Load JSON-LD
            self.logger.info(f"Converting: {input_path.relative_to(self.root_dir)}")
            g = Graph()
            
            # Parse with explicit UTF-8 encoding
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
                g.parse(data=content, format='json-ld')
            
            # Serialize to Turtle with UTF-8 encoding
            turtle_data = g.serialize(format='turtle', encoding='utf-8')
            
            # Write output file
            with open(output_path, 'wb') as f:
                f.write(turtle_data)
            
            self.logger.info(f"  ✓ Created: {output_path.relative_to(self.root_dir)}")
            return True
            
        except ParserError as e:
            error_msg = f"RDF parsing error: {str(e)}"
            self.logger.error(f"  ✗ {input_path.name}: {error_msg}")
            self.errors.append((input_path, error_msg))
            return False
            
        except UnicodeDecodeError as e:
            error_msg = f"UTF-8 encoding error: {str(e)}"
            self.logger.error(f"  ✗ {input_path.name}: {error_msg}")
            self.errors.append((input_path, error_msg))
            return False
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(f"  ✗ {input_path.name}: {error_msg}")
            self.errors.append((input_path, error_msg))
            return False
    
    def run(self) -> Dict:
        """
        Execute conversion of all found JSON-LD files
        
        Returns:
            Dictionary with conversion statistics
        """
        self.logger.info("="*70)
        self.logger.info("TSCG JSON-LD to OWL Turtle Converter v1.0.0")
        self.logger.info("="*70)
        self.logger.info(f"Root directory: {self.root_dir}")
        self.logger.info(f"Target directories: {', '.join([d.name for d in self.target_dirs])}")
        if self.output_dir:
            self.logger.info(f"Output directory: {self.output_dir}")
        if self.dry_run:
            self.logger.info("MODE: DRY-RUN (no files will be modified)")
        self.logger.info("")
        
        # Find all JSON-LD files
        self.logger.info("Scanning for .jsonld files...")
        jsonld_files = self.find_jsonld_files()
        self.stats['found'] = len(jsonld_files)
        
        if not jsonld_files:
            self.logger.warning("No .jsonld files found!")
            return self.stats
        
        self.logger.info(f"Found {len(jsonld_files)} .jsonld files")
        self.logger.info("")
        
        # Convert each file
        self.logger.info("Starting conversion...")
        self.logger.info("-"*70)
        
        for i, file_path in enumerate(jsonld_files, 1):
            self.logger.info(f"[{i}/{len(jsonld_files)}] Processing...")
            
            success = self.convert_file(file_path)
            
            if success:
                self.stats['converted'] += 1
            else:
                self.stats['failed'] += 1
                if not self.skip_errors:
                    self.logger.error("Stopping due to conversion error (use --skip-errors to continue)")
                    break
            
            self.logger.info("")
        
        # Print summary
        self._print_summary()
        
        return self.stats
    
    def _print_summary(self):
        """Print conversion summary"""
        self.logger.info("="*70)
        self.logger.info("CONVERSION SUMMARY")
        self.logger.info("="*70)
        self.logger.info(f"Files found:     {self.stats['found']}")
        self.logger.info(f"Files converted: {self.stats['converted']}")
        self.logger.info(f"Files failed:    {self.stats['failed']}")
        self.logger.info(f"Files skipped:   {self.stats['skipped']}")
        
        if self.errors:
            self.logger.info("")
            self.logger.info("ERRORS ENCOUNTERED:")
            self.logger.info("-"*70)
            for file_path, error_msg in self.errors:
                self.logger.info(f"  {file_path.name}")
                self.logger.info(f"    → {error_msg}")
        
        self.logger.info("="*70)
        
        if self.dry_run:
            self.logger.info("DRY-RUN completed. No files were modified.")
        elif self.stats['failed'] == 0:
            self.logger.info("✓ All files converted successfully!")
        else:
            self.logger.info(f"⚠ Conversion completed with {self.stats['failed']} errors")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Convert TSCG JSON-LD ontologies to OWL Turtle format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert all files (creates .ttl alongside .jsonld)
  python jsonld_to_turtle.py
  
  # Dry-run to preview what would be converted
  python jsonld_to_turtle.py --dry-run
  
  # Convert to separate output directory
  python jsonld_to_turtle.py --output-dir /path/to/turtle-output
  
  # Continue on errors
  python jsonld_to_turtle.py --skip-errors
  
  # Verbose logging
  python jsonld_to_turtle.py --verbose
        """
    )
    
    parser.add_argument(
        '--root-dir',
        type=Path,
        default=Path.cwd().parent.parent.parent,  # Assumes script in src/tscg/ontology_tools
        help='Root directory of TSCG project (default: auto-detect from script location)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=None,
        help='Output directory (default: same as input files)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be converted without actually converting'
    )
    
    parser.add_argument(
        '--skip-errors',
        action='store_true',
        help='Continue conversion even if errors occur'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Adjust logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create converter and run
    converter = JSONLDToTurtleConverter(
        root_dir=args.root_dir,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
        skip_errors=args.skip_errors
    )
    
    stats = converter.run()
    
    # Exit with appropriate code
    if stats['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
