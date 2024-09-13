# import all the views to satisfy Connexion's MethodView resolver
# otherwise connexion will throw "TypeError: 'module' object is not callable"
from .AbilitiesView import AbilitiesView
from .AssetsView import AssetsView
from .ResourcesView import ResourcesView
from .ConfigView import ConfigView
from .DownloadsView import DownloadsView
from .UsersView import UsersView
from .PersonasView import PersonasView
from .RagIndexingView import RagIndexingView
from .MessagesView import MessagesView
from .ConversationsView import ConversationsView
from .VoicesFacesView import VoicesFacesView