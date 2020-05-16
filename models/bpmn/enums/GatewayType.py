import enum

class GatewayType(enum.Enum):
    Exclusive = 1
    Inclusive = 2
    EventBased = 3
    Parallel = 4
    EventBasedExclusive = 5
    Complex = 6
    ParallelEvent = 7