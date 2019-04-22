
from tap_ringcentral.streams.contacts import ContactsStream
from tap_ringcentral.streams.call_log import CallLogStream
from tap_ringcentral.streams.messages import MessageStream
from tap_ringcentral.streams.meetings import MeetingStream

AVAILABLE_STREAMS = [
    ContactsStream,
    CallLogStream,
    MessageStream,
    MeetingStream,
]

__all__ = [
    'ContactsStream',
    'CallLogStream',
    'MessageStream',
    'MeetingStream',
]
