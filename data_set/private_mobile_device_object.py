class PrivateMobileDeviceObject:
    timestamp_start: int = -1
    timestamp_stop: int = -1
    id_user: int = -1
    x: float = -1
    y: float = -1

    def take_sort_value(self):
        return self.timestamp_start
