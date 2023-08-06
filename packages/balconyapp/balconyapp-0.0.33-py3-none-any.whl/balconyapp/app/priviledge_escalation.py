from balcony import BaseBalconyApp, BalconyAWS, get_rich_console
from typer.main import Typer
import typer
from typing import Optional
import jmespath
import random
import time
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.panel import Panel



console = get_rich_console()

class PriviledgeEscalationPreventer(BaseBalconyApp,
        author="og", 
        app_name="apply-priviledge-escalation-preventer", 
        description="",
        tags=('iam', 'priviledge-escalation', 'security')
    ):
    
    def __init__(self, *args, **kwargs) -> None:
        pass
      
    def get_data(self, *args, **kwargs) -> dict:
        service=kwargs.get('service')
        balcony = BalconyAWS()
        service_node = balcony.get_service(service)
        return {
            'read_only_function_count':'read_only_function_count',
            'resource_nodes': 'generated_resource_nodes'
        } 
       
    def get_cli_app(self, *args, **kwargs) -> typer.main.Typer:
        app = typer.Typer(no_args_is_help=True)
        

        @app.callback(invoke_without_command=True)
        def _command(
            service: str = typer.Argument(None, show_default=False,help='AWS Service Name'),
        ):
            balcony = BalconyAWS()
            available_services = balcony.get_available_service_node_names()
            selected_service = random.choice(available_services)

                    
        return app
                
    


