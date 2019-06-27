
from tap_ringcentral.streams.contacts import ContactsStream
from tap_ringcentral.streams.call_log import CallLogStream
from tap_ringcentral.streams.company_call_log import CompanyCallLogStream
from tap_ringcentral.streams.messages import MessageStream

# This is disabled because RingCentral's permission model
# does not permit a user to fetch Meetings for other
# RingCentral users. It should be re-enabled RingCentral makes
# these resources accessible in its API
#
#from tap_ringcentral.streams.meetings import MeetingStream


AVAILABLE_STREAMS = [
    ContactsStream,
    CallLogStream,
    CompanyCallLogStream,
    MessageStream,
    #MeetingStream,
]

__all__ = [
    'ContactsStream',
    'CallLogStream',
    'CompanyCallLogStream',
    'MessageStream',
    #'MeetingStream',
]
