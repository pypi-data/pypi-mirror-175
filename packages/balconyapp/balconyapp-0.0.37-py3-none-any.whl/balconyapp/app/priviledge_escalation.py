from balcony import BaseBalconyApp, BalconyAWS, get_rich_console
from typer.main import Typer
import typer
import jmespath
import random
import time
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from typing import List, Set, Dict, Tuple, Optional, Union



console = get_rich_console()


app = typer.Typer(no_args_is_help=True)


@app.callback(invoke_without_command=True)
def _command(
    patterns: Optional[List[str]] = typer.Option(None, "--pattern", '-p', show_default=False, help='UNIX pattern matching for generated parameters. Should be quoted. e.g. (-p "*prod-*")'),

):
    available_services = balcony.get_available_service_node_names()
    balcony = BalconyAWS()
    iam_service = balcony.get_service('iam')

    iam_reader = iam_service.get_service_reader()
    roles = iam_reader.read_operation('Role', 'GetRole', match_patterns=patterns)
    # get roles
    console.print(roles)
    
    
class PriviledgeEscalationPreventer(BaseBalconyApp,
        author="og", 
        app_name="apply-priviledge-escalation-preventer", 
        description="",
        tags=('iam', 'priviledge-escalation', 'security')
    ):
    
    def __init__(self, *args, **kwargs) -> None:
        pass
      
    def get_data(self, *args, **kwargs) -> dict:
        balcony = BalconyAWS()
        iam_service = balcony.get_service('iam')
        return {
            'read_only_function_count':'read_only_function_count',
            'resource_nodes': 'generated_resource_nodes'
        } 
       
    def get_cli_app(self, *args, **kwargs) -> typer.main.Typer:
        return app
                
    


"""
select some roles to start with
for each role:
    create a policy for PrvEsc-PermissionBoundary, 
    put-role-permissions-boundary

+ tf like plan and apply logic


"""