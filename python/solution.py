from controller.event_controller import EventController


class Solution:

    @staticmethod
    def process_messages(messages):

        result_list = []
        events = EventController.prepare_event_list(events=messages)
        for event in events:
            event.prepare()
            result = event.validate()
            if result != "":
                result_list.append(result)

        return ",".join(result_list)
