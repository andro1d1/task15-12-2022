from amocrm.v2 import tokens, Event, filters, Tag
from datetime import datetime, timedelta, date

class AmoCrm:

    def __init__(self):

        tokens.default_token_manager(
            client_id="xxx-xxx-xxxx-xxxx-xxxxxxx", # Data for integration
            client_secret="xxxx",
            subdomain="subdomain",
            redirect_url="https://xxxx/xx",
            storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
        )
        tokens.default_token_manager.init(code="..very long code...", skip_error=True)

    def filter_entity_type(self, entity_type: str) -> list:
        """
        Return a list of events for a given entity type
        """
        return list(Event.objects.filter(filters=[filters.SingleListFilter("entity_type")(entity_type), ]))

    def filter_date(self) -> list:
        """
        Return a list of events for a given time, 12 hours
        """
        now = datetime.utcnow()
        return list(Event.objects.filter(filters=[filters.DateRangeFilter("created_at")(now-timedelta(hours=12), now)]))
