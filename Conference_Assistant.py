import os

# Bibliothèque standard pour interagir avec le système d'exploitation, utilisée pour gérer les variables d'environnement.
import django
# from fastmcp import FastMCP
from mcp.server.fastmcp import FastMCP
# Importation de la classe FastMCP depuis le module fastmcp, utilisée pour créer un serveur MCP rapide.
from asgiref.sync import sync_to_async

# Importation de sync_to_async pour convertir des fonctions synchrones en asynchrones, compatible avec les ORM Django.
# Initialize Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GestionConference3AI.settings")
django.setup()
# Importation des modèles Django après initialisation pour éviter des erreurs de configuration.
from ConferenceApp.models import Conference  # noqa: E402
from SessionApp.models import Session  # noqa: E402

# from SessionApp.models import Session

# Create an MCP server
mcp = FastMCP(name="Conference Assistant")


# Lancement
# Décorateur pour définir un outil MCP exécutable de manière asynchrone, rendant cette fonction accessible via le serveur MCP.
@mcp.tool()
async def list_conferences() -> str:
    """List all available conferences."""


    # Ce décorateur permet d'appeler des méthodes synchrones de l'ORM Django dans un contexte asynchrone, évitant les blocages.
    @sync_to_async
    def _get_conferences():
        # Fonction interne synchrone pour récupérer la liste des conférences depuis la base de données.
        return list(Conference.objects.all())


    conferences = await _get_conferences()
    # Appel asynchrone à la fonction interne pour obtenir les conférences, en attendant le résultat.
    if not conferences:
        return "No conferences found."
    return "\n".join([f"- {c.name} ({c.start_date} to {c.end_date})" for c in conferences])
# Construit une chaîne formatée avec le nom et les dates de chaque conférence, séparées par des sauts de ligne
@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Get details of a specific conference by name."""
    @sync_to_async
    def _get_conference():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"
    conference= await _get_conference()
    if conference == "MULTIPLE":
        return f"Multiple conferences found matching '{name}'. Please be more specific."
    if not conference:
        return f"Conference '{name}' not found."
    return (f"Name: {conference.name}\n"f"Theme: {conference.get_theme_display()}\n"f"Location: {conference.location}\n"f"Dates: {conference.start_date} to{conference.end_date}\n"f"Description: {conference.description}")
@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """List sessions for a specific conference."""
    @sync_to_async
    def _get_sessions():
        try:
            conference=Conference.objects.get(name__icontains=conference_name)
            return list(conference.sessions.all()), conference
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None
    result, conference= await _get_sessions()
    if result == "MULTIPLE":
        return f"Multiple conferences found matching'{conference_name}'. Please be more specific."
    if conference is None:
        return f"Conference '{conference_name}' not found."
    sessions = result
    if not sessions:
        return f"No sessions found for conference'{conference.name}'."
    session_list= []
    for s in sessions: 
        session_list.append(
            f"- {s.title} ({s.start_time} - {s.end_time}) in{s.room}\n"
            f" Topic: {s.topic}"
            )
    return "\n".join(session_list)
@mcp.tool()
async def conferences_by_theme(theme_code: str) -> str:
    """
    Liste les conférences d'un thème donné.
    Exemple de theme_code : 'IA', 'SE', 'SC', 'IT' (les codes de ton modèle).
    """

    @sync_to_async
    def _get_conferences():
        # theme__iexact = insensible à la casse
        return list(Conference.objects.filter(theme__iexact=theme_code))

    conferences = await _get_conferences()

    if not conferences:
        return f"No conferences found with theme '{theme_code}'."

    lignes = [f"Conferences with theme '{theme_code}':"]
    for c in conferences:
        lignes.append(
            f"- {c.name} in {c.location} "
            f"({c.start_date} to {c.end_date})"
        )

    return "\n".join(lignes)


def e(theme_code: str) -> str:
    """Alias synchrone pour lister les conférences d'un thème.
    Utilise l'ORM Django directement (doit être importé après django.setup()).
    """
    qs = Conference.objects.filter(theme__iexact=theme_code)
    if not qs:
        return f"No conferences found with theme '{theme_code}'."
    lines = [f"Conferences with theme '{theme_code}':"]
    for c in qs:
        lines.append(f"- {c.name} in {c.location} ({c.start_date} to {c.end_date})")
    return "\n".join(lines)

if __name__ == "__main__":
    mcp.run(transport="stdio")
