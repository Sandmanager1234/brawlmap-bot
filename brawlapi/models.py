

class Event:
    start_time: str
    end_time: str
    slot_id: int
    map_id: int
    map_name: str
    mode: str

    @classmethod
    def from_json(cls, json_data: dict) -> "Event":
        self : Event = cls()
        self.start_time = json_data.get('startTime')
        self.end_time = json_data.get('endTime')
        self.slot_id = json_data.get('slotId')
        event = json_data.get('event')
        self.map_id = event.get('id')
        self.mode = event.get('mode')
        self.map_name = event.get('map')