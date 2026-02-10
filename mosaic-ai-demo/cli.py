#!/usr/bin/env python3
"""
Databricks Mosaic AI Demo - TUI (Text User Interface)
Interactive bash-style command-line interface
"""

import os
import sys
from typing import Optional, List, Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich import box
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from model_serving import DatabricksModelServing
from rag_pipeline import RAGPipeline
from agent_framework import AgentFramework

# Load environment variables
load_dotenv()


class MosaicAICLI:
    """TUI application for Databricks Mosaic AI Demo."""
    
    def __init__(self):
        self.console = Console()
        self.session = PromptSession(history=InMemoryHistory())
        self.model_client: Optional[DatabricksModelServing] = None
        self.rag_pipeline: Optional[RAGPipeline] = None
        self.agent_framework: Optional[AgentFramework] = None
        self.current_model = "databricks-llama-3-1-8b-instruct"
        self.initialized = False
    
    def initialize(self):
        """Initialize the components."""
        try:
            self.console.print("[yellow]Initializing Databricks Mosaic AI components...[/yellow]")
            
            # Check environment
            if not os.getenv("DATABRICKS_HOST") or not os.getenv("DATABRICKS_TOKEN"):
                self.console.print("[red]Error: DATABRICKS_HOST and DATABRICKS_TOKEN must be set in .env file[/red]")
                return False
            
            # Initialize components
            self.model_client = DatabricksModelServing()
            self.rag_pipeline = RAGPipeline()
            self.agent_framework = AgentFramework()
            
            self.console.print("[green]✓ All components initialized successfully[/green]")
            self.initialized = True
            return True
        except Exception as e:
            self.console.print(f"[red]✗ Initialization failed: {e}[/red]")
            return False
    
    def show_banner(self):
        """Display welcome banner."""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        🤖  Databricks Mosaic AI Demo - TUI Interface         ║
║                                                               ║
║              Explore the Power of Unified AI                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """
        self.console.print(banner, style="bold cyan")
        self.console.print()
    
    def show_help(self):
        """Display help information."""
        help_table = Table(title="Available Commands", box=box.ROUNDED, show_header=True)
        help_table.add_column("Command", style="cyan", no_wrap=True)
        help_table.add_column("Description", style="white")
        
        commands = [
            ("help", "Show this help message"),
            ("menu", "Show main menu"),
            ("query <text>", "Query foundation model"),
            ("rag <question>", "Ask question using RAG pipeline"),
            ("compare <text>", "Compare multiple models"),
            ("trace", "Create and analyze agent traces"),
            ("model <name>", "Switch model (llama8b, llama70b, mixtral)"),
            ("status", "Show current configuration"),
            ("samples", "Show sample queries"),
            ("clear", "Clear screen"),
            ("exit", "Exit the application"),
        ]
        
        for cmd, desc in commands:
            help_table.add_row(cmd, desc)
        
        self.console.print(help_table)
        self.console.print()
    
    def show_menu(self):
        """Display main menu."""
        menu = Table(title="Main Menu", box=box.DOUBLE, show_header=False)
        menu.add_column("Option", style="bold cyan", no_wrap=True)
        menu.add_column("Feature", style="white")
        
        options = [
            ("1", "🤖 Foundation Model APIs - Query LLMs"),
            ("2", "📚 RAG Pipeline - Retrieval-Augmented Generation"),
            ("3", "🔬 Agent Framework - Tracing and Monitoring"),
            ("4", "📊 Compare Models - Side-by-side comparison"),
            ("5", "💡 Sample Queries - Try predefined examples"),
            ("6", "⚙️  Configuration - View/change settings"),
            ("7", "❓ Help - Show all commands"),
            ("0", "🚪 Exit - Quit the application"),
        ]
        
        for opt, feat in options:
            menu.add_row(opt, feat)
        
        self.console.print(menu)
        self.console.print()
    
    def show_status(self):
        """Display current configuration."""
        status_panel = Panel(
            f"""[bold cyan]Current Configuration[/bold cyan]

[yellow]Model:[/yellow] {self.current_model}
[yellow]Host:[/yellow] {os.getenv('DATABRICKS_HOST', 'Not set')}
[yellow]Token:[/yellow] {'✓ Set' if os.getenv('DATABRICKS_TOKEN') else '✗ Not set'}
[yellow]Initialized:[/yellow] {'✓ Yes' if self.initialized else '✗ No'}
            """,
            box=box.ROUNDED,
            border_style="cyan"
        )
        self.console.print(status_panel)
        self.console.print()
    
    def show_samples(self):
        """Display sample queries."""
        samples_table = Table(title="Sample Queries", box=box.ROUNDED, show_header=True)
        samples_table.add_column("#", style="cyan", no_wrap=True)
        samples_table.add_column("Query", style="white")
        samples_table.add_column("Type", style="green")
        
        samples = [
            ("1", "What is Databricks Mosaic AI?", "Model"),
            ("2", "How does Vector Search work?", "RAG"),
            ("3", "Explain Delta Lake benefits", "Model"),
            ("4", "What are Lakeflow pipelines?", "RAG"),
            ("5", "Compare Llama models", "Compare"),
        ]
        
        for num, query, qtype in samples:
            samples_table.add_row(num, query, qtype)
        
        self.console.print(samples_table)
        self.console.print("\n[dim]Use: query <text>, rag <text>, or compare <text>[/dim]\n")
    
    def query_model(self, prompt: str):
        """Query a foundation model."""
        if not self.initialized:
            self.console.print("[red]Error: Components not initialized. Run 'status' to check.[/red]")
            return
        
        self.console.print(f"\n[yellow]Querying {self.current_model}...[/yellow]\n")
        
        try:
            result = self.model_client.query_model(
                prompt=prompt,
                model=self.current_model,
                max_tokens=500,
                temperature=0.7
            )
            
            if result["success"]:
                # Display response
                response_panel = Panel(
                    Markdown(result["response"]),
                    title="[bold cyan]Response[/bold cyan]",
                    border_style="green",
                    box=box.ROUNDED
                )
                self.console.print(response_panel)
                
                # Display metrics
                metrics_table = Table(box=box.SIMPLE, show_header=False)
                metrics_table.add_column("Metric", style="yellow")
                metrics_table.add_column("Value", style="white")
                
                metrics_table.add_row("Total Tokens", str(result["usage"]["total_tokens"]))
                metrics_table.add_row("Prompt Tokens", str(result["usage"]["prompt_tokens"]))
                metrics_table.add_row("Completion Tokens", str(result["usage"]["completion_tokens"]))
                
                # Cost estimation
                input_cost = (result["usage"]["prompt_tokens"] / 1_000_000) * 0.15
                output_cost = (result["usage"]["completion_tokens"] / 1_000_000) * 0.45
                total_cost = input_cost + output_cost
                metrics_table.add_row("Estimated Cost", f"${total_cost:.6f}")
                
                self.console.print("\n", metrics_table, "\n")
            else:
                self.console.print(f"[red]Error: {result['error']}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    def rag_query(self, question: str):
        """Query using RAG pipeline."""
        if not self.initialized:
            self.console.print("[red]Error: Components not initialized.[/red]")
            return
        
        self.console.print(f"\n[yellow]Processing RAG query...[/yellow]\n")
        
        try:
            result = self.rag_pipeline.query(
                question=question,
                num_context_chunks=3,
                model=self.current_model
            )
            
            if result["success"]:
                # Display answer
                answer_panel = Panel(
                    Markdown(result["answer"]),
                    title="[bold cyan]Answer[/bold cyan]",
                    border_style="green",
                    box=box.ROUNDED
                )
                self.console.print(answer_panel)
                
                # Display sources
                sources_table = Table(title="Sources", box=box.SIMPLE, show_header=True)
                sources_table.add_column("Source", style="cyan")
                sources_table.add_column("Page", style="yellow")
                sources_table.add_column("Score", style="green")
                
                for source in result["sources"]:
                    sources_table.add_row(
                        source["source"],
                        str(source["page"]),
                        f"{source['score']:.2f}"
                    )
                
                self.console.print("\n", sources_table, "\n")
                
                # Metrics
                self.console.print(f"[dim]Tokens: {result['usage']['total_tokens']} | Context chunks: {result['context_used']}[/dim]\n")
            else:
                self.console.print(f"[red]Error: {result['error']}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    def compare_models(self, prompt: str):
        """Compare multiple models."""
        if not self.initialized:
            self.console.print("[red]Error: Components not initialized.[/red]")
            return
        
        models = [
            "databricks-llama-3-1-8b-instruct",
            "databricks-llama-3-3-70b-instruct",
        ]
        
        self.console.print(f"\n[yellow]Comparing {len(models)} models...[/yellow]\n")
        
        try:
            results = self.model_client.compare_models(
                prompt=prompt,
                models=models
            )
            
            for idx, result in enumerate(results):
                model_name = models[idx].split("-")[2] + " " + models[idx].split("-")[3]
                
                if result["success"]:
                    panel = Panel(
                        Markdown(result["response"]),
                        title=f"[bold cyan]{model_name.upper()}[/bold cyan]",
                        border_style="green" if idx == 0 else "blue",
                        box=box.ROUNDED
                    )
                    self.console.print(panel)
                    self.console.print(f"[dim]Tokens: {result['usage']['total_tokens']}[/dim]\n")
                else:
                    self.console.print(f"[red]{model_name}: Error - {result['error']}[/red]\n")
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    def create_trace(self):
        """Create and analyze agent trace."""
        if not self.initialized:
            self.console.print("[red]Error: Components not initialized.[/red]")
            return
        
        self.console.print("\n[yellow]Creating sample trace...[/yellow]\n")
        
        # Simulate trace
        query = "What is Databricks Mosaic AI?"
        mock_chunks = [
            {"id": "chunk_1", "score": 0.92, "source": "docs.pdf", "text": "Sample context..."},
            {"id": "chunk_2", "score": 0.87, "source": "docs.pdf", "text": "More context..."},
            {"id": "chunk_3", "score": 0.81, "source": "docs.pdf", "text": "Additional info..."},
        ]
        
        retrieval_trace = self.agent_framework.trace_retrieval(query, mock_chunks, 145.3)
        
        token_count = {"prompt_tokens": 350, "completion_tokens": 120, "total_tokens": 470}
        generation_trace = self.agent_framework.trace_generation(
            query, "context", "Sample answer...", 425.7, token_count
        )
        
        e2e_trace = self.agent_framework.trace_end_to_end(
            query, retrieval_trace, generation_trace, "Sample answer...", 571.0
        )
        
        # Display trace summary
        trace_panel = Panel(
            f"""[bold cyan]Trace Summary[/bold cyan]

[yellow]Trace ID:[/yellow] {e2e_trace['trace_id']}
[yellow]Query:[/yellow] {query}
[yellow]Total Time:[/yellow] {e2e_trace['metrics']['total_time_ms']:.1f} ms
[yellow]Retrieval Time:[/yellow] {e2e_trace['metrics']['retrieval_time_ms']:.1f} ms
[yellow]Generation Time:[/yellow] {e2e_trace['metrics']['generation_time_ms']:.1f} ms
[yellow]Chunks Used:[/yellow] {e2e_trace['metrics']['num_chunks_used']}
[yellow]Total Tokens:[/yellow] {e2e_trace['metrics']['total_tokens']}
[yellow]Avg Retrieval Score:[/yellow] {e2e_trace['quality_indicators']['avg_retrieval_score']:.3f}
[yellow]Latency Category:[/yellow] {e2e_trace['quality_indicators']['latency_category']}
            """,
            box=box.ROUNDED,
            border_style="green"
        )
        self.console.print(trace_panel)
        self.console.print()
    
    def switch_model(self, model_name: str):
        """Switch the current model."""
        model_map = {
            "llama8b": "databricks-llama-3-1-8b-instruct",
            "llama70b": "databricks-llama-3-3-70b-instruct",
            "mixtral": "databricks-mixtral-8x7b-instruct",
        }
        
        if model_name.lower() in model_map:
            self.current_model = model_map[model_name.lower()]
            self.console.print(f"[green]✓ Switched to {self.current_model}[/green]\n")
        else:
            self.console.print(f"[red]Unknown model: {model_name}[/red]")
            self.console.print("[yellow]Available: llama8b, llama70b, mixtral[/yellow]\n")
    
    def process_command(self, command: str):
        """Process user command."""
        if not command:
            return True
        
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd in ["exit", "quit", "q"]:
            return False
        elif cmd == "help":
            self.show_help()
        elif cmd == "menu":
            self.show_menu()
        elif cmd == "status":
            self.show_status()
        elif cmd == "samples":
            self.show_samples()
        elif cmd == "clear":
            os.system('clear' if os.name != 'nt' else 'cls')
            self.show_banner()
        elif cmd == "query":
            if args:
                self.query_model(args)
            else:
                self.console.print("[red]Usage: query <your question>[/red]\n")
        elif cmd == "rag":
            if args:
                self.rag_query(args)
            else:
                self.console.print("[red]Usage: rag <your question>[/red]\n")
        elif cmd == "compare":
            if args:
                self.compare_models(args)
            else:
                self.console.print("[red]Usage: compare <your question>[/red]\n")
        elif cmd == "trace":
            self.create_trace()
        elif cmd == "model":
            if args:
                self.switch_model(args)
            else:
                self.console.print(f"[yellow]Current model: {self.current_model}[/yellow]\n")
        elif cmd.isdigit():
            # Menu selection
            self.handle_menu_selection(int(cmd))
        else:
            self.console.print(f"[red]Unknown command: {cmd}[/red]")
            self.console.print("[yellow]Type 'help' for available commands[/yellow]\n")
        
        return True
    
    def handle_menu_selection(self, option: int):
        """Handle menu selection."""
        if option == 1:
            prompt = self.session.prompt("Enter your question: ")
            if prompt:
                self.query_model(prompt)
        elif option == 2:
            question = self.session.prompt("Enter your question: ")
            if question:
                self.rag_query(question)
        elif option == 3:
            self.create_trace()
        elif option == 4:
            prompt = self.session.prompt("Enter your question: ")
            if prompt:
                self.compare_models(prompt)
        elif option == 5:
            self.show_samples()
        elif option == 6:
            self.show_status()
        elif option == 7:
            self.show_help()
        elif option == 0:
            return False
        else:
            self.console.print("[red]Invalid option[/red]\n")
        
        return True
    
    def run(self):
        """Run the CLI interactive loop."""
        self.show_banner()
        
        if not self.initialize():
            self.console.print("\n[red]Failed to initialize. Please check your .env configuration.[/red]")
            self.console.print("[yellow]Required: DATABRICKS_HOST and DATABRICKS_TOKEN[/yellow]\n")
            return
        
        self.console.print("[dim]Type 'help' for commands or 'menu' for options[/dim]\n")
        
        while True:
            try:
                user_input = self.session.prompt(
                    "[bold green]mosaic-ai>[/bold green] ",
                    default=""
                ).strip()
                
                if not self.process_command(user_input):
                    self.console.print("\n[yellow]Goodbye! 👋[/yellow]\n")
                    break
                    
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Use 'exit' to quit[/yellow]\n")
                continue
            except EOFError:
                self.console.print("\n\n[yellow]Goodbye! 👋[/yellow]\n")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]\n")


def main():
    """Main entry point."""
    cli = MosaicAICLI()
    cli.run()


if __name__ == "__main__":
    main()
