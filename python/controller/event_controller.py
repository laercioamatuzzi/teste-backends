from model.event import Event


class EventController:

    @staticmethod
    def prepare_event_list(events: str) -> dict:
        """
        Organize events by proposal_id and create a Event object per proposal_id
        :param events: list of events, see examples at (test/input/*)
        :return: {"80921e5f-4307-4623-9ddb-5bf826a31dd7": Proposal()}
        """

        events_dict = {}
        event_list = []

        for event in events.split("\n")[1:]:

            event_values = event.split(",")
            proposal_id = event_values[4]

            if proposal_id in events_dict.keys():
                events_dict[proposal_id].events.append(event)

            else:
                events_dict[proposal_id] = Event(pid=proposal_id, events=[event])

        for event in events_dict:
            event_list.append(events_dict[event])

        return event_list
