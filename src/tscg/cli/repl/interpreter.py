"""
TSCG REPL Interpreter

Author: Echopraxium with the collaboration of Claude AI
"""

import sys
from pathlib import Path
from typing import Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from .context import ReplContext
from ..core.models import ASFIDScore, REVOIScore

console = Console()


class TSCGRepl:
    """TSCG Interactive REPL"""
    
    VERSION = "0.1.0"
    
    def __init__(self):
        self.context = ReplContext()
        self.session = PromptSession(
            history=FileHistory('.tscg_history'),
            auto_suggest=AutoSuggestFromHistory(),
        )
        self.running = True
    
    def run(self):
        """Main REPL loop"""
        self._print_welcome()
        
        while self.running:
            try:
                text = self.session.prompt('>>> ')
                
                if not text.strip():
                    continue
                
                # Add to history
                self.context.add_to_history(text)
                
                # Execute command
                self._execute(text.strip())
                
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
        
        self._print_goodbye()
    
    def _print_welcome(self):
        """Print welcome message"""
        welcome = f"""[bold cyan]TSCG v{self.VERSION} Interactive Shell[/bold cyan]
        
[dim]Transdisciplinary System Construction Game
Business Logic Engine Prototype[/dim]

Type [bold]'help'[/bold] for commands, [bold]'exit'[/bold] to quit
"""
        console.print(Panel(welcome, box=box.DOUBLE, border_style="cyan"))
    
    def _print_goodbye(self):
        """Print goodbye message"""
        console.print("\n[cyan]Goodbye![/cyan]")
    
    def _execute(self, command: str):
        """Execute a REPL command"""
        # Parse command
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Route to handler
        if cmd in ['exit', 'quit']:
            self.running = False
        elif cmd == 'help':
            self._cmd_help(args)
        elif cmd == 'load':
            self._cmd_load(args)
        elif cmd == 'show':
            self._cmd_show(args)
        elif cmd == 'export':
            self._cmd_export(args)
        elif cmd == 'sparql':
            self._cmd_sparql(args)
        elif cmd == 'context':
            self._cmd_context()
        elif cmd == 'clear':
            console.clear()
        elif cmd == 'metrics':
            self._cmd_metrics(args)
        else:
            console.print(f"[yellow]Unknown command: {cmd}[/yellow]")
            console.print("Type 'help' for available commands")
    
    def _cmd_help(self, args: str):
        """Show help information"""
        if not args:
            # General help
            table = Table(title="TSCG REPL Commands", box=box.ROUNDED)
            table.add_column("Command", style="cyan")
            table.add_column("Description", style="white")
            
            table.add_row("load <file>", "Load an ontology (JSON-LD)")
            table.add_row("show <what>", "Display entities (ontologies, metaconcepts)")
            table.add_row("export <file>", "Export current ontology to Turtle")
            table.add_row("sparql <query>", "Execute SPARQL query")
            table.add_row("metrics orthogonality", "Compute orthogonality metrics")
            table.add_row("context", "Show session context")
            table.add_row("clear", "Clear screen")
            table.add_row("exit/quit", "Exit REPL")
            
            console.print(table)
        else:
            # Specific command help
            console.print(f"[yellow]Detailed help not yet implemented for: {args}[/yellow]")
    
    def _cmd_load(self, filepath: str):
        """Load an ontology file"""
        if not filepath:
            console.print("[red]Usage: load <filepath>[/red]")
            return
        
        try:
            # Check if it's a project file
            project_path = Path(f"/mnt/project/{filepath}")
            if project_path.exists():
                filepath = str(project_path)
            
            graph = self.context.load_ontology(filepath)
            ontology_name = Path(filepath).stem
            
            console.print(f"[green]✓[/green] Loaded: {ontology_name}")
            console.print(f"  Triples: {len(graph)}")
            console.print(f"  Active ontology: {self.context.get_current_ontology_name()}")
            
        except Exception as e:
            console.print(f"[red]Failed to load {filepath}: {e}[/red]")
    
    def _cmd_show(self, what: str):
        """Show various entities"""
        if not what:
            console.print("[red]Usage: show <ontologies|metaconcepts>[/red]")
            return
        
        what = what.lower()
        
        if what == "ontologies":
            loaded = self.context.list_loaded_ontologies()
            
            if not loaded:
                console.print("[yellow]No ontologies loaded[/yellow]")
                return
            
            table = Table(title="Loaded Ontologies", box=box.ROUNDED)
            table.add_column("Name", style="cyan")
            table.add_column("Layer", style="magenta")
            table.add_column("Triples", style="green")
            table.add_column("Active", style="yellow")
            
            for name in loaded:
                metadata = self.context.loader.metadata.get(name)
                is_active = "✓" if name == self.context.current_ontology else ""
                
                table.add_row(
                    name,
                    metadata.layer if metadata else "?",
                    str(metadata.triple_count) if metadata else "?",
                    is_active
                )
            
            console.print(table)
        
        elif what == "metaconcepts":
            concepts = self.context.loader.get_metaconcepts()
            
            if not concepts:
                console.print("[yellow]No metaconcepts found in loaded ontologies[/yellow]")
                return
            
            table = Table(title="Metaconcepts", box=box.ROUNDED)
            table.add_column("Label", style="cyan")
            table.add_column("Layer", style="magenta")
            table.add_column("URI", style="dim")
            
            for concept in concepts[:20]:  # Limit to first 20
                table.add_row(
                    concept.label,
                    concept.layer,
                    concept.uri
                )
            
            if len(concepts) > 20:
                console.print(f"[dim]... and {len(concepts) - 20} more[/dim]")
            
            console.print(table)
        
        else:
            console.print(f"[yellow]Unknown show target: {what}[/yellow]")
    
    def _cmd_export(self, args: str):
        """Export current ontology to Turtle"""
        if not args:
            console.print("[red]Usage: export <output_file.ttl>[/red]")
            return
        
        if not self.context.current_graph:
            console.print("[red]No ontology loaded[/red]")
            return
        
        try:
            result = self.context.turtle_exporter.export(
                self.context.current_graph,
                args
            )
            
            if result.success:
                console.print(f"[green]✓[/green] {result.message}")
            else:
                console.print(f"[red]✗[/red] {result.message}")
        
        except Exception as e:
            console.print(f"[red]Export failed: {e}[/red]")
    
    def _cmd_sparql(self, query: str):
        """Execute SPARQL query"""
        if not query:
            console.print("[red]Usage: sparql <query>[/red]")
            return
        
        if not self.context.current_graph:
            console.print("[red]No ontology loaded[/red]")
            return
        
        try:
            result = self.context.execute_sparql(query)
            
            if result.row_count == 0:
                console.print("[yellow]No results found[/yellow]")
                return
            
            # Display results in table
            table = Table(title=f"Results ({result.row_count} rows)", box=box.ROUNDED)
            
            for var in result.vars:
                table.add_column(var, style="cyan")
            
            for binding in result.bindings[:50]:  # Limit to 50 rows
                table.add_row(*[binding.get(v, "") for v in result.vars])
            
            if result.row_count > 50:
                console.print(f"[dim]... and {result.row_count - 50} more rows[/dim]")
            
            console.print(table)
        
        except Exception as e:
            console.print(f"[red]Query failed: {e}[/red]")
    
    def _cmd_context(self):
        """Show session context"""
        stats = self.context.get_stats()
        
        info = f"""[bold]Session Context[/bold]

Loaded ontologies: {stats['loaded_ontologies']}
Active ontology: {stats['current_ontology'] or '[dim]none[/dim]'}
Triples in active: {stats['triple_count']}
Variables defined: {stats['variables']}
Command history: {stats['history_length']} commands
"""
        console.print(Panel(info, box=box.ROUNDED, border_style="blue"))
    
    def _cmd_metrics(self, args: str):
        """Compute metrics"""
        parts = args.split(maxsplit=1)
        if not parts:
            console.print("[red]Usage: metrics <orthogonality|...>[/red]")
            return
        
        metric_type = parts[0].lower()
        
        if metric_type == "orthogonality":
            self._metrics_orthogonality()
        else:
            console.print(f"[yellow]Unknown metric type: {metric_type}[/yellow]")
    
    def _metrics_orthogonality(self):
        """Compute orthogonality metrics (demo)"""
        # Demo with sample ASFID scores
        console.print("[cyan]Computing orthogonality for sample ASFID scores...[/cyan]\n")
        
        sample_scores = {
            "A": 0.95,
            "S": 0.88,
            "F": 0.92,
            "I": 0.85,
            "D": 0.90
        }
        
        analyzer = self.context.ortho_analyzer
        report = analyzer.analyze_scores(sample_scores)
        
        # Display matrix
        console.print("[bold]Orthogonality Matrix (cosine similarity):[/bold]")
        
        table = Table(box=box.SIMPLE)
        table.add_column("", style="cyan")
        for label in report.labels:
            table.add_column(label, style="cyan")
        
        for i, label_i in enumerate(report.labels):
            row = [label_i]
            for j in range(len(report.labels)):
                val = report.matrix[i, j]
                row.append(f"{val:.2f}")
            table.add_row(*row)
        
        console.print(table)
        console.print()
        console.print(report)


def main():
    """Entry point for REPL"""
    repl = TSCGRepl()
    repl.run()


if __name__ == "__main__":
    main()
